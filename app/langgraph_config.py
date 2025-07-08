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
    
    # Survey data
    survey_questions: List[str]
    user_responses: List[str]
    
    # Processing data
    combined_input: str  # For LLM processing
    extracted_entities: Dict[str, Any]
    qloo_affinities: Dict[str, Any]
    cultural_profile: Dict[str, Any]
    recommendations: Dict[str, Any]
    matching: Dict[str, Any]
    
    # Output data
    final_output: str
    error_message: Optional[str]
    
    # Metadata
    current_node: str
    processing_time: float


class NodeType(str, Enum):
    """Enum for node types to ensure consistency."""
    INTRO = "intro"
    SURVEY = "survey"
    LLM_PARSER = "llm_parser"
    QLOO_AFFINITY = "qloo_affinity"
    PROFILE_GENERATOR = "profile_generator"
    RECOMMENDATIONS = "recommendations"
    OPTIONAL_MATCH = "optional_match"
    END = "end"


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
    
    # Add nodes with proper error handling
    workflow.add_node(NodeType.INTRO, intro_node)
    workflow.add_node(NodeType.SURVEY, survey_node)
    workflow.add_node(NodeType.LLM_PARSER, llm_parser_node)
    workflow.add_node(NodeType.QLOO_AFFINITY, qloo_affinity_node)
    workflow.add_node(NodeType.PROFILE_GENERATOR, profile_generator_node)
    workflow.add_node(NodeType.RECOMMENDATIONS, recommendations_node)
    workflow.add_node(NodeType.OPTIONAL_MATCH, optional_match_node)
    workflow.add_node(NodeType.END, end_node)
    
    # Define the flow with conditional routing
    workflow.set_entry_point(NodeType.INTRO)
    
    # Add edges with conditional logic
    workflow.add_edge(NodeType.INTRO, NodeType.SURVEY)
    workflow.add_edge(NodeType.SURVEY, NodeType.LLM_PARSER)
    workflow.add_edge(NodeType.LLM_PARSER, NodeType.QLOO_AFFINITY)
    workflow.add_edge(NodeType.QLOO_AFFINITY, NodeType.PROFILE_GENERATOR)
    workflow.add_edge(NodeType.PROFILE_GENERATOR, NodeType.RECOMMENDATIONS)
    workflow.add_edge(NodeType.RECOMMENDATIONS, NodeType.OPTIONAL_MATCH)
    workflow.add_edge(NodeType.OPTIONAL_MATCH, NodeType.END)
    workflow.add_edge(NodeType.END, END)
    
    # Remove error handling edges to avoid concurrent update conflicts
    # Error handling will be done within each node instead
    
    # Compile the graph without memory for now
    return workflow.compile(checkpointer=None)


def intro_node(state: TribuAIState) -> TribuAIState:
    """
    Introduction node - explains TribuAI and sets up the experience.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running intro node for session {state.get('session_id', 'unknown')}")
        
        # Update state with current node
        state["current_node"] = NodeType.INTRO
        state["timestamp"] = datetime.now().isoformat()
        
        intro_message = """
        🎭 Welcome to TribuAI - Your Cultural Intelligence Engine!
        
        I'm here to understand your cultural identity and connect you with brands, 
        communities, and experiences that resonate with who you truly are.
        
        Let's start by exploring your cultural preferences. I'll ask you a few 
        questions about your tastes in music, art, fashion, places, and more.
        
        Ready to discover your tribe? Let's begin!
        """
        
        print(intro_message)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in intro node: {e}")
        state["error_message"] = f"Error in intro: {str(e)}"
        return state


def survey_node(state: TribuAIState) -> TribuAIState:
    """
    Survey node - generates and asks cultural questions using LLM.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with survey questions
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running survey node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.SURVEY
        
        # Generate survey questions based on user input
        # For now, use predefined questions (in production, this would be LLM-generated)
        state["survey_questions"] = [
            "What music genres or artists define your taste?",
            "What visual arts, films, or aesthetic styles appeal to you?",
            "What places, cities, or travel experiences resonate with you?",
            "What fashion styles or brands reflect your identity?",
            "What social causes or values are important to you?"
        ]
        
        # Simulate user responses (in production, this would be interactive)
        state["user_responses"] = [
            "I love indie rock, alternative, and electronic music",
            "I'm drawn to minimalist art, Japanese cinema, and brutalist architecture",
            "I feel at home in creative cities like Berlin, Tokyo, and Portland",
            "I prefer sustainable, minimalist fashion with streetwear elements",
            "I care about environmental sustainability and creative expression"
        ]
        
        print("📝 Cultural Survey Questions:")
        for i, question in enumerate(state["survey_questions"], 1):
            print(f"{i}. {question}")
            print(f"   Response: {state['user_responses'][i-1]}")
            print()
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in survey node: {e}")
        state["error_message"] = f"Error in survey: {str(e)}"
        return state


def llm_parser_node(state: TribuAIState) -> TribuAIState:
    """
    LLM Parser node - extracts structured entities from user responses.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with extracted entities
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running llm_parser node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.LLM_PARSER
        
        # Combine user input and responses for parsing
        combined_input = f"Original input: {state.get('user_input', '')}\n\nSurvey responses:\n"
        for i, response in enumerate(state.get('user_responses', []), 1):
            combined_input += f"Q{i}: {response}\n"
        
        # Store combined input for LLM processing
        state["combined_input"] = combined_input
        
        # Extract entities using LLM
        parser_chain = create_parser_chain()
        
        extracted_data = parser_chain.invoke({
            "input_text": combined_input
        })
        
        state["extracted_entities"] = {
            "music": extracted_data.get("music", []),
            "art": extracted_data.get("art", []),
            "places": extracted_data.get("places", []),
            "fashion": extracted_data.get("fashion", []),
            "values": extracted_data.get("values", []),
            "audiences": extracted_data.get("audiences", [])
        }
        
        logger.info(f"Extracted entities: {state['extracted_entities']}")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in llm_parser_node: {e}")
        # Fallback to basic extraction
        state["extracted_entities"] = {
            "music": ["indie", "electronic", "alternative"],
            "art": ["minimalist", "Japanese cinema", "brutalist"],
            "places": ["Berlin", "Tokyo", "Portland"],
            "fashion": ["minimalist", "sustainable", "streetwear"],
            "values": ["sustainability", "creativity"],
            "audiences": ["creative professionals", "urban millennials"]
        }
        state["error_message"] = f"Error in llm_parser: {str(e)}"
        return state


def qloo_affinity_node(state: TribuAIState) -> TribuAIState:
    """
    Qloo Affinity node - queries Qloo API for cultural affinities.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with Qloo affinities
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running qloo_affinity node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.QLOO_AFFINITY
        
        # Query Qloo API with extracted entities
        qloo_client = QlooClient()
        
        # Get entities for analysis
        entities = []
        extracted_entities = state.get('extracted_entities', {})
        entities.extend(extracted_entities.get('music', [])[:3])
        entities.extend(extracted_entities.get('art', [])[:2])
        entities.extend(extracted_entities.get('fashion', [])[:2])
        
        if entities:
            # Analyze cultural affinities
            analysis = qloo_client.analyze_cultural_affinities(entities)
            state["qloo_affinities"] = analysis
        else:
            # Fallback data
            state["qloo_affinities"] = {
                "brands": ["Generic Brand 1", "Generic Brand 2"],
                "destinations": ["Generic City 1", "Generic City 2"],
                "audiences": ["Generic Audience"],
                "cultural_signals": ["generic_signal"]
            }
        
        logger.info(f"Qloo affinities retrieved: {len(state['qloo_affinities'])} categories")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in qloo_affinity_node: {e}")
        # Fallback data
        state["qloo_affinities"] = {
            "brands": ["Generic Brand 1", "Generic Brand 2"],
            "destinations": ["Generic City 1", "Generic City 2"],
            "audiences": ["Generic Audience"],
            "cultural_signals": ["generic_signal"]
        }
        state["error_message"] = f"Error in qloo_affinity: {str(e)}"
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
        
        # Combine extracted entities and Qloo affinities to create profile
        extracted_entities = state.get('extracted_entities', {})
        qloo_affinities = state.get('qloo_affinities', {})
        
        state["cultural_profile"] = {
            "identity": "Urban Creative Minimalist",
            "music": extracted_entities.get("music", []),
            "style": extracted_entities.get("fashion", []),
            "destinations": qloo_affinities.get("destinations", []),
            "values": extracted_entities.get("values", []),
            "audiences": qloo_affinities.get("audiences", []),
            "cultural_signals": qloo_affinities.get("cultural_signals", [])
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
    Optional Match node - suggests culturally similar profiles.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with matching suggestions
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running optional_match node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.OPTIONAL_MATCH
        
        # For demo purposes, provide a mock match
        # In production, this would query a user profile system
        state["matching"] = {
            "suggested_match": {
                "name": "Sofia",
                "age": 28,
                "location": "Mexico City",
                "cultural_overlap": 85,
                "shared_interests": ["minimalism", "indie music", "sustainability"]
            },
            "match_confidence": 0.85,
            "shared_audiences": state.get('cultural_profile', {}).get('audiences', [])
        }
        
        logger.info(f"Found match with {state['matching']['suggested_match']['name']}")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in optional_match_node: {e}")
        state["error_message"] = f"Error in optional_match: {str(e)}"
        return state


def end_node(state: TribuAIState) -> TribuAIState:
    """
    End node - finalizes the experience and prepares output.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with final output
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Running end node for session {state.get('session_id', 'unknown')}")
        
        state["current_node"] = NodeType.END
        
        # Create final output summary
        session_id = state.get('session_id', 'unknown')
        cultural_profile = state.get('cultural_profile', {})
        recommendations = state.get('recommendations', {})
        matching = state.get('matching', {})
        
        state["final_output"] = f"""
        🎯 Cultural Profile Summary for Session {session_id}
        
        Identity: {cultural_profile.get('identity', 'N/A')}
        Music: {', '.join(cultural_profile.get('music', []))}
        Style: {', '.join(cultural_profile.get('style', []))}
        Destinations: {', '.join(cultural_profile.get('destinations', []))}
        
        Recommendations:
        - Brands: {', '.join(recommendations.get('brands', []))}
        - Places: {', '.join(recommendations.get('places', []))}
        - Your Tribe: {', '.join(recommendations.get('audiences', []))}
        
        Match: {matching.get('suggested_match', {}).get('name', 'N/A')}
        """
        
        logger.info("TribuAI session completed successfully")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        state["processing_time"] = processing_time
        
        return state
        
    except Exception as e:
        logger.error(f"Error in end_node: {e}")
        state["error_message"] = f"Error in end: {str(e)}"
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