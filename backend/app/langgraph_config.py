"""
TribuAI - LangGraph Configuration

This module defines the LangGraph workflow for TribuAI using best practices from the official documentation.
Features include proper state management, streaming support, and robust error handling.
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
    
    # Metadata
    current_node: str
    processing_time: float
    error_message: Optional[str]
    profile_complete: bool # Added for profile completion tracking


class NodeType(str, Enum):
    """Enum for node types to ensure consistency."""
    LLM_PARSER = "llm_parser"
    PROFILE_GENERATOR = "profile_generator"
    RECOMMENDATIONS = "recommendations"
    OPTIONAL_MATCH = "optional_match"
    END = "end"


# --- New: Helper to check missing fields ---
def get_missing_fields(entities: Dict[str, Any]) -> List[str]:
    required = ["music", "art", "fashion", "values", "places", "audiences"]
    return [field for field in required if not entities.get(field)]

# --- New: Nodes to ask for each missing field ---
def ask_for_field_node(field: str):
    def node(state: TribuAIState) -> TribuAIState:
        # Only ask if profile is not complete
        if state.get("profile_complete"):
            return state
        msg = f"Could you tell me about your favorite {field.replace('_', ' ')}?"
        state["current_node"] = f"ask_{field}"
        state["system_message"] = msg
        state["assistant_message"] = msg
        return state
    return node

# --- Register ask nodes for each field ---
ask_nodes = {}
for field in ["music", "art", "fashion", "values", "places", "audiences"]:
    ask_nodes[field] = ask_for_field_node(field)


def create_tribuai_graph() -> StateGraph:
    """
    Create and configure the TribuAI LangGraph workflow with best practices.
    
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
    
    # Add only essential nodes
    workflow.add_node(NodeType.LLM_PARSER, llm_parser_node)
    for field, node_fn in ask_nodes.items():
        workflow.add_node(f"ask_{field}", node_fn)
    workflow.add_node(NodeType.PROFILE_GENERATOR, profile_generator_node)
    workflow.add_node(NodeType.RECOMMENDATIONS, recommendations_node)
    workflow.add_node(NodeType.OPTIONAL_MATCH, optional_match_node)
    
    # Define the simplified flow
    workflow.set_entry_point(NodeType.LLM_PARSER)
    
    # Add edges with simplified flow
    def missing_field_edge(state: TribuAIState):
        entities = state.get("extracted_entities", {})
        missing = get_missing_fields(entities)
        if missing:
            return f"ask_{missing[0]}"
        return NodeType.PROFILE_GENERATOR
    workflow.add_conditional_edges(NodeType.LLM_PARSER, missing_field_edge)
    # After each ask node, go back to parser
    for field in ask_nodes:
        workflow.add_edge(f"ask_{field}", NodeType.LLM_PARSER)
    # After profile, recommendations, match, end
    workflow.add_edge(NodeType.PROFILE_GENERATOR, NodeType.RECOMMENDATIONS)
    workflow.add_edge(NodeType.RECOMMENDATIONS, NodeType.OPTIONAL_MATCH)
    workflow.add_edge(NodeType.OPTIONAL_MATCH, END)
    
    # Compile the graph without memory for now
    return workflow.compile(checkpointer=None)


def llm_parser_node(state: TribuAIState) -> TribuAIState:
    """
    LLM Parser node - extracts structured entities from user input.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with extracted entities
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running llm_parser node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.LLM_PARSER
        
        # Use user input directly for parsing
        user_input = state.get('user_input', '')
        state["combined_input"] = user_input
        
        # Extract entities using LLM
        parser_chain = create_parser_chain()
        
        parsed = parser_chain.invoke({"input_text": user_input})
        
        # Map entities to required fields
        entities = parsed.get("entities", [])
        def names_of_type(t):
            return [e["name"] for e in entities if e.get("type") == t]
        state["extracted_entities"] = {
            "music": names_of_type("artist"),
            "art": names_of_type("art"),
            "places": names_of_type("place") + names_of_type("destination"),
            "fashion": names_of_type("brand"),
            "values": names_of_type("tag"),
            "audiences": names_of_type("audience")
        }
        # Set profile_complete flag
        required = ["music", "art", "fashion", "values", "places", "audiences"]
        state["profile_complete"] = all(len(state["extracted_entities"].get(f, [])) > 0 for f in required)
        logger.info(f"Extracted entities: {state['extracted_entities']}")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in llm_parser_node: {e}")
        state["error_message"] = f"Error in llm_parser: {str(e)}"
        return state


def profile_generator_node(state: TribuAIState) -> TribuAIState:
    """
    Profile Generator node - creates the user's cultural identity profile.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with cultural profile
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running profile_generator node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.PROFILE_GENERATOR
        
        # Use only extracted entities from LLM parser
        extracted_entities = state.get('extracted_entities', {})
        
        state["cultural_profile"] = {
            "identity": f"{extracted_entities.get('music', [''])[0]} enthusiast" if extracted_entities.get('music') else "Cultural Explorer",
            "music": extracted_entities.get("music", []),
            "style": extracted_entities.get("fashion", []),
            "values": extracted_entities.get("values", []),
            "art": extracted_entities.get("art", []),
            "places": extracted_entities.get("places", [])
        }
        
        logger.info(f"Generated cultural profile: {state['cultural_profile']['identity']}")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in profile_generator_node: {e}")
        state["error_message"] = f"Error in profile_generator: {str(e)}"
        return state


def recommendations_node(state: TribuAIState) -> TribuAIState:
    """
    Recommendations node - curates personalized recommendations.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with recommendations
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running recommendations node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.RECOMMENDATIONS
        
        # Generate recommendations based on profile and affinities
        cultural_profile = state.get('cultural_profile', {})
        qloo_client = QlooClient()
        
        # Get brand recommendations
        brands = qloo_client.get_brand_recommendations(cultural_profile)
        
        # Get destination recommendations
        destinations = qloo_client.get_destination_recommendations(cultural_profile)
        
        # Get audience recommendations
        audiences = qloo_client.get_audience_recommendations(cultural_profile)
        
        state["recommendations"] = {
            "brands": brands,
            "places": destinations,
            "audiences": [audience.get('name', '') for audience in audiences],
            "experiences": [
                "Visit minimalist art galleries",
                "Explore sustainable fashion boutiques",
                "Attend indie music festivals",
                "Join creative coworking spaces"
            ]
        }
        
        logger.info(f"Generated {len(brands)} brand recommendations")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in recommendations_node: {e}")
        state["error_message"] = f"Error in recommendations: {str(e)}"
        return state


def optional_match_node(state: TribuAIState) -> TribuAIState:
    """
    Optional Match node - suggests affinity with audience clusters (anonymous matching).
    """
    start_time = datetime.now()
    try:
        logger.info(f"Running optional_match node for session {state.get('session_id', 'unknown')}")
        state["current_node"] = NodeType.OPTIONAL_MATCH
        
        # Obtener intereses del usuario
        user_interests = set()
        profile = state.get("cultural_profile", {})
        user_interests.update(profile.get("music", []))
        user_interests.update(profile.get("style", []))
        user_interests.update(profile.get("values", []))

        # Obtener audiencias de Qloo (clusters)
        audiences = state.get("recommendations", {}).get("audiences", [])
        audience_cluster = audiences[0] if audiences else "Unknown"

        # Simular intereses del cluster (en producción, usar datos reales de Qloo)
        cluster_interests = set(["minimalism", "indie music", "sustainability"])  # TODO: reemplazar por datos reales
        shared_interests = list(user_interests & cluster_interests)
        affinity_percentage = int(100 * len(shared_interests) / max(len(user_interests | cluster_interests), 1))

        state["matching"] = {
            "affinity_percentage": affinity_percentage,
            "shared_interests": shared_interests,
            "audience_cluster": audience_cluster
        }

        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        return state
    except Exception as e:
        logger.error(f"Error in optional_match_node: {e}")
        state["error_message"] = f"Error in optional_match: {str(e)}"
        return state


def error_handler(state: TribuAIState) -> TribuAIState:
    """
    Error handler node for graceful error handling.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with error information
    """
    logger.error(f"Error in node {state.get('current_node', 'unknown')}: {state.get('error_message', 'Unknown error')}")
    
    # Add error information to state
    state["error_message"] = state.get("error_message", "Unknown error occurred")
    state["final_output"] = f"❌ Error: {state['error_message']}"
    
    return state 