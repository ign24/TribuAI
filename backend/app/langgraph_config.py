"""
TribuAI - LangGraph Configuration

This module defines the LangGraph workflow for TribuAI using best practices from the official documentation.
Features include proper state management, streaming support, and robust error handling.
Now includes dynamic recommendations that adapt based on conversation context.
"""

import os
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from datetime import datetime
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from loguru import logger

from qloo_client import QlooClient
from chains.llm_parser_chain import create_parser_chain


class TribuAIState(TypedDict):
    """
    State definition for TribuAI LangGraph workflow.
    Using TypedDict for better type safety and clarity.
    """
    # Input data
    user_input: Annotated[str, "last"]  # Multiple nodes might read this
    session_id: str
    timestamp: str
    
    # Processing data
    combined_input: str  # For LLM processing
    extracted_entities: Dict[str, Any]
    cultural_profile: Dict[str, Any]
    recommendations: Dict[str, Any]
    matching: Dict[str, Any]
    
    # Conversation state for dynamic recommendations
    conversation_history: List[Dict[str, Any]]
    current_context: str
    recommendation_context: str
    
    # Metadata
    current_node: str
    processing_time: float
    error_message: Optional[str]
    profile_complete: bool
    assistant_message: Optional[str]


class NodeType(str, Enum):
    """Enum for node types to ensure consistency."""
    LLM_PARSER = "llm_parser"
    CONVERSATIONAL_LLM = "conversational_llm"
    PROFILE_GENERATOR = "profile_generator"
    DYNAMIC_RECOMMENDATIONS = "dynamic_recommendations"
    OPTIONAL_MATCH = "optional_match"
    END = "end"


# --- Helper to check missing fields ---
def get_missing_fields(entities: Dict[str, Any]) -> List[str]:
    required = ["music", "art", "fashion", "values", "places", "audiences"]
    return [field for field in required if not entities.get(field)]

# --- Nodes to ask for each missing field with dynamic context ---
def ask_for_field_node(field: str):
    def node(state: TribuAIState) -> TribuAIState:
        # Only ask if profile is not complete
        if state.get("profile_complete"):
            return state
        
        # Create contextual question based on what we already know
        context = state.get("current_context", "")
        if context:
            msg = f"Based on your interest in {context}, what kind of {field.replace('_', ' ')} do you love?"
        else:
            msg = f"Could you tell me about your favorite {field.replace('_', ' ')}?"
        
        state["current_node"] = f"ask_{field}"
        state["assistant_message"] = msg
        return state
    return node

# --- Register ask nodes for each field ---
ask_nodes = {}
for field in ["music", "art", "fashion", "values", "places", "audiences"]:
    ask_nodes[field] = ask_for_field_node(field)


# --- Conversational LLM Node ---
def build_profile_summary(profile):
    parts = []
    for field in ["music", "art", "fashion", "values", "places", "audiences"]:
        values = profile.get(field, [])
        if values:
            parts.append(f"{field}: {', '.join(values)}")
    return "; ".join(parts) if parts else "(nothing yet)"

def render_conversational_prompt(profile_summary, conversation_history, profile_complete, missing_fields):
    history_str = "\n".join([
        f"User: {msg.get('user_input', '')}" for msg in conversation_history
    ])
    if not profile_complete:
        return f"""
You are TribuAI, a cultural intelligence engine and expert conversationalist.

Your job is to guide the user through a friendly, engaging conversation to discover their cultural profile.
You must collect the following fields: music, art, fashion, values, places, and audiences.
You already know the following about the user:
{profile_summary}

Here is the conversation so far:
{history_str}

The following fields are still missing: {', '.join(missing_fields)}.

Your task:
- Ask a conversational, context-aware question to elicit information about the next missing field (choose one from the missing list).
- Do NOT ask about fields that are already filled.
- Reference what you already know about the user.
- Avoid repeating yourself.
- Keep the tone warm, curious, and human.
- Vary your questions and connect them to previous answers when possible.

Return only your next message to the user.
"""
    else:
        return """
You are TribuAI, a cultural intelligence engine.

You have collected all required information from the user.
Thank the user warmly and let them know you are preparing their recommendations.
Return only your next message to the user.
"""

def conversational_llm_node(state: TribuAIState) -> TribuAIState:
    profile = state.get("extracted_entities", {})
    conversation_history = state.get("conversation_history", [])
    profile_complete = state.get("profile_complete", False)
    profile_summary = build_profile_summary(profile)
    missing_fields = get_missing_fields(profile)
    prompt = render_conversational_prompt(profile_summary, conversation_history, profile_complete, missing_fields)
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    state["assistant_message"] = response.content.strip()
    state["current_node"] = NodeType.CONVERSATIONAL_LLM
    return state


def create_tribuai_graph() -> StateGraph:
    """
    Create and configure the TribuAI LangGraph workflow with dynamic recommendations.
    
    Returns:
        Configured StateGraph instance with memory and streaming support
    """
    
    # Initialize LLM with streaming support
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True  # Enable streaming for better UX
    )
    
    # Initialize Qloo client
    qloo_client = QlooClient()
    
    # Create the graph with memory support
    workflow = StateGraph(TribuAIState)
    
    # Add memory saver for persistence
    memory = MemorySaver()
    
    # Add nodes
    workflow.add_node(NodeType.LLM_PARSER, llm_parser_node)
    workflow.add_node(NodeType.PROFILE_GENERATOR, profile_generator_node)
    workflow.add_node(NodeType.DYNAMIC_RECOMMENDATIONS, dynamic_recommendations_node)
    workflow.add_node(NodeType.OPTIONAL_MATCH, optional_match_node)
    workflow.add_node(NodeType.CONVERSATIONAL_LLM, conversational_llm_node)
    
    # Define the flow - simplified to avoid loops
    workflow.set_entry_point(NodeType.LLM_PARSER)
    
    # Define la función de ruteo condicional después del parser
    def route_after_parser(state: TribuAIState):
        return NodeType.PROFILE_GENERATOR if state.get("profile_complete", False) else NodeType.CONVERSATIONAL_LLM
    workflow.add_conditional_edges(NodeType.LLM_PARSER, route_after_parser)
    
    # Cuando el perfil está completo, generar recomendaciones después del profile_generator
    workflow.add_edge(NodeType.PROFILE_GENERATOR, NodeType.DYNAMIC_RECOMMENDATIONS)
    workflow.add_edge(NodeType.DYNAMIC_RECOMMENDATIONS, NodeType.OPTIONAL_MATCH)
    workflow.add_edge(NodeType.OPTIONAL_MATCH, END)
    
    # Elimina el ciclo automático: después de conversational_llm_node, el grafo termina y espera nuevo input
    workflow.add_edge(NodeType.CONVERSATIONAL_LLM, END)
    
    # Compile the graph
    return workflow.compile(checkpointer=None)


def llm_parser_node(state: TribuAIState) -> TribuAIState:
    """
    LLM Parser node - extracts structured entities from user input.
    Now includes conversation context for dynamic recommendations.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with extracted entities and context
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running llm_parser node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.LLM_PARSER
        
        # Use user input directly for parsing
        user_input = state.get('user_input', '')
        state["combined_input"] = user_input
        
        # Update conversation history
        conversation_history = state.get("conversation_history", [])
        conversation_history.append({
            "user_input": user_input,
            "timestamp": datetime.now().isoformat()
        })
        state["conversation_history"] = conversation_history
        
        # Extract entities using LLM
        parser_chain = create_parser_chain()
        
        parsed = parser_chain.invoke({"input_text": user_input})
        
        # Map entities to required fields
        entities = parsed.get("entities", [])
        def names_of_type(t):
            return [e["name"] for e in entities if e.get("type") == t]
        
        extracted_entities = {
            "music": names_of_type("artist"),
            "art": names_of_type("art"),
            "places": names_of_type("place") + names_of_type("destination"),
            "fashion": names_of_type("brand"),
            "values": names_of_type("tag"),
            "audiences": names_of_type("audience")
        }
        
        # Accumulate values for each category, avoiding duplicates
        existing_entities = state.get("extracted_entities", {})
        for category, new_values in extracted_entities.items():
            if new_values:
                existing_values = existing_entities.get(category, [])
                combined = list(set(existing_values + new_values))
                existing_entities[category] = combined
        state["extracted_entities"] = existing_entities
        
        # Update current context for dynamic recommendations
        all_entities = []
        for category, values in existing_entities.items():
            if values:
                all_entities.extend(values[:2])  # Take first 2 from each category
        
        if all_entities:
            state["current_context"] = ", ".join(all_entities[:3])  # Show top 3 for context
        
        # Set profile_complete flag
        required = ["music", "art", "fashion", "values", "places", "audiences"]
        state["profile_complete"] = all(len(existing_entities.get(f, [])) > 0 for f in required)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        logger.info(f"Extracted entities: {existing_entities}")
        logger.info(f"Current context: {state.get('current_context', 'None')}")
        
        return state
        
    except Exception as e:
        logger.error(f"Error in llm_parser_node: {e}")
        state["error_message"] = f"Error in llm_parser_node: {str(e)}"
        return state


def profile_generator_node(state: TribuAIState) -> TribuAIState:
    """
    Profile Generator node - creates the user's cultural identity profile.
    Now includes context-aware profile generation.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with cultural profile
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running profile_generator node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.PROFILE_GENERATOR
        
        entities = state.get("extracted_entities", {})
        context = state.get("current_context", "")
        
        # Generate cultural profile with context
        if context:
            profile_description = f"A cultural enthusiast who loves {context}. "
        else:
            profile_description = "A person with diverse cultural interests. "
        
        # Add specific interests
        interests = []
        for category, values in entities.items():
            if values:
                interests.append(f"{category}: {', '.join(values[:2])}")
        
        if interests:
            profile_description += f"Key interests include: {'; '.join(interests)}."
        
        cultural_profile = {
            "identity": "Cultural Explorer",
            "description": profile_description,
            **entities
        }
        
        state["cultural_profile"] = cultural_profile
        
        # Set recommendation context for dynamic recommendations
        state["recommendation_context"] = context if context else "general"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        logger.info(f"Generated cultural profile: {cultural_profile['identity']}")
        
        return state
        
    except Exception as e:
        logger.error(f"Error in profile_generator_node: {e}")
        state["error_message"] = f"Error in profile_generator: {str(e)}"
        return state


def build_combined_profile_narrative(entities):
    """
    Build a narrative string combining all profile fields for contextual recommendations.
    """
    parts = []
    if entities.get("music"):
        parts.append(f"Music: {', '.join(entities['music'])}")
    if entities.get("art"):
        parts.append(f"Art: {', '.join(entities['art'])}")
    if entities.get("fashion"):
        parts.append(f"Fashion: {', '.join(entities['fashion'])}")
    if entities.get("values"):
        parts.append(f"Values: {', '.join(entities['values'])}")
    if entities.get("places"):
        parts.append(f"Places: {', '.join(entities['places'])}")
    if entities.get("audiences"):
        parts.append(f"Audiences: {', '.join(entities['audiences'])}")
    return " | ".join(parts)


def dynamic_recommendations_node(state: TribuAIState) -> TribuAIState:
    """
    Dynamic Recommendations node - generates recommendations based on conversation context.
    Recommendations adapt based on what the user has shared and conversation progress.
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running dynamic_recommendations node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.DYNAMIC_RECOMMENDATIONS
        
        entities = state.get("extracted_entities", {})
        context = state.get("current_context", "general")
        conversation_history = state.get("conversation_history", [])
        profile_complete = state.get("profile_complete", False)
        
        # Initialize Qloo client
        qloo_client = QlooClient()
        
        # Determine recommendation strategy based on conversation progress and available entities
        if not entities or all(len(values) == 0 for values in entities.values()):
            # No entities extracted, show basic recommendations
            logger.info("No entities found - showing basic recommendations")
            recommendations = qloo_client.get_basic_recommendations(context)
            
        elif len(conversation_history) <= 2 or not profile_complete:
            # Early/mid conversation: Show contextual recommendations
            logger.info("Early/mid conversation - showing contextual recommendations")
            recommendations = qloo_client.get_contextual_recommendations(entities, context)
            
        else:
            # Complete profile: Show comprehensive recommendations using combined narrative
            logger.info("Complete profile - showing comprehensive recommendations (combined narrative)")
            profile_narrative = build_combined_profile_narrative(entities)
            recommendations = qloo_client.get_comprehensive_recommendations(profile_narrative)
        
        state["recommendations"] = recommendations
        
        # Generate assistant message with recommendations when profile is complete
        if profile_complete:
            assistant_message = "🎉 Perfect! I've collected all the information I need about your cultural preferences. Check out your personalized recommendations below!"
            
            state["assistant_message"] = assistant_message
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        logger.info(f"Generated dynamic recommendations for context: {context}")
        logger.info(f"Recommendations: {len(recommendations.get('brands', []))} brands, {len(recommendations.get('places', []))} places")
        
        return state
        
    except Exception as e:
        logger.error(f"Error in dynamic_recommendations_node: {e}")
        state["error_message"] = f"Error in dynamic_recommendations: {str(e)}"
        # Return empty recommendations on error
        state["recommendations"] = {"brands": [], "places": []}
        return state


def optional_match_node(state: TribuAIState) -> TribuAIState:
    """
    Optional Match node - generates matching information if profile is complete.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with matching information
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running optional_match node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.OPTIONAL_MATCH
        
        profile_complete = state.get("profile_complete", False)
        
        if not profile_complete:
            # Profile not complete, skip matching
            state["matching"] = None
            return state
        
        entities = state.get("extracted_entities", {})
        
        # Initialize Qloo client
        qloo_client = QlooClient()
        
        # Get all entities for matching
        all_entities = []
        for category, values in entities.items():
            if isinstance(values, list):
                all_entities.extend(values[:2])  # Take first 2 from each category
        
        # Get matching information
        matching = qloo_client.get_matching_info(all_entities)
        
        state["matching"] = matching
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        logger.info(f"Generated matching information for complete profile")
        
        return state
        
    except Exception as e:
        logger.error(f"Error in optional_match_node: {e}")
        state["error_message"] = f"Error in optional_match: {str(e)}"
        return state


def error_handler(state: TribuAIState) -> TribuAIState:
    """
    Error handler for the LangGraph workflow.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with error information
    """
    logger.error(f"Error in LangGraph workflow: {state.get('error_message', 'Unknown error')}")
    
    # Set default values for error state
    if "cultural_profile" not in state:
        state["cultural_profile"] = {
            "identity": "Error",
            "description": "There was an error processing your request."
        }
    
    if "recommendations" not in state:
        state["recommendations"] = {
            "brands": [],
            "places": []
        }
    
    if "matching" not in state:
        state["matching"] = None
    
    return state 