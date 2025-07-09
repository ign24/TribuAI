"""
TribuAI FastAPI Backend

This module provides REST API endpoints for the TribuAI cultural intelligence engine.
It exposes the LangGraph pipeline and Qloo integration through HTTP endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
from loguru import logger

from app.main import TribuAI

# Initialize FastAPI app
app = FastAPI(
    title="TribuAI API",
    description="Cultural Intelligence Engine API",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TribuAI instance
tribuai = None

@app.on_event("startup")
async def startup_event():
    """Initialize TribuAI on startup."""
    global tribuai
    try:
        tribuai = TribuAI()
        logger.info("TribuAI API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize TribuAI: {e}")
        raise

# Pydantic models for API
class ProcessRequest(BaseModel):
    user_input: str

class CulturalProfileRequest(BaseModel):
    music: List[str] = []
    art: List[str] = []
    fashion: List[str] = []
    values: List[str] = []
    places: List[str] = []
    audiences: List[str] = []

class StatusResponse(BaseModel):
    status: str

class HealthResponse(BaseModel):
    status: str

class ApiResponse(BaseModel):
    cultural_profile: Dict[str, Any]
    recommendations: Dict[str, Any]  # brands/places ahora son List[Dict[str, Any]]
    matching: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "TribuAI Cultural Intelligence API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")

@app.get("/status")
async def status_check():
    """Status check endpoint."""
    return StatusResponse(status="running")

@app.post("/api/process")
async def process_input(request: ProcessRequest):
    """
    Process user input through the TribuAI pipeline.
    
    Args:
        request: ProcessRequest containing user input
        
    Returns:
        ApiResponse with cultural profile and recommendations
    """
    if not tribuai:
        raise HTTPException(status_code=503, detail="TribuAI not initialized")
    
    try:
        logger.info(f"Processing input: {request.user_input[:50]}...")
        
        # Process through TribuAI
        result = tribuai.process_input(request.user_input)
        
        # Transform result to API response format
        api_response = transform_result_to_api_format(result)
        
        # Add assistant_message and profile_complete if present
        if "assistant_message" in result:
            api_response = api_response.dict() if hasattr(api_response, 'dict') else dict(api_response)
            api_response["assistant_message"] = result["assistant_message"]
        if "profile_complete" in result:
            api_response["profile_complete"] = result["profile_complete"]

        logger.info("Successfully processed input")
        return api_response
        
    except Exception as e:
        logger.error(f"Error processing input: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/api/process-profile")
async def process_cultural_profile(request: CulturalProfileRequest):
    """
    Process a complete cultural profile from the frontend conversation system.
    
    Args:
        request: CulturalProfileRequest containing the complete cultural profile
        
    Returns:
        ApiResponse with cultural profile and recommendations
    """
    if not tribuai:
        raise HTTPException(status_code=503, detail="TribuAI not initialized")
    
    try:
        logger.info(f"Processing cultural profile with {sum(len(getattr(request, field)) for field in ['music', 'art', 'fashion', 'values', 'places', 'audiences'])} entities")
        
        # Convert profile to user input format for compatibility
        profile_text = []
        for field in ['music', 'art', 'fashion', 'values', 'places', 'audiences']:
            values = getattr(request, field)
            if values:
                profile_text.append(f"{field}: {', '.join(values)}")
        
        user_input = "\n".join(profile_text)
        
        # Process through TribuAI with simplified flow
        result = process_profile_directly(user_input)
        
        # Transform result to API response format
        api_response = transform_result_to_api_format(result)
        
        logger.info("Successfully processed cultural profile")
        return api_response
        
    except Exception as e:
        logger.error(f"Error processing cultural profile: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

def process_profile_directly(user_input: str) -> Dict[str, Any]:
    """
    Process cultural profile directly without iterative questions.
    Uses simplified Qloo client for 100% real data.
    """
    from app.qloo_client import QlooClient
    from loguru import logger
    
    try:
        # Initialize Qloo client
        qloo_client = QlooClient()
        
        # Extract entities from input (simplified)
        entities = extract_entities_simple(user_input)
        
        # Generate cultural profile
        cultural_profile = generate_cultural_profile(entities)
        
        # Get real recommendations from Qloo
        recommendations = qloo_client.get_real_recommendations(entities)
        
        # Get real matching info from Qloo
        all_entities = []
        for category, values in entities.items():
            if isinstance(values, list):
                all_entities.extend(values[:2])
        
        matching = qloo_client.get_matching_info(all_entities)
        
        return {
            "cultural_profile": cultural_profile,
            "recommendations": recommendations,
            "matching": matching
        }
        
    except Exception as e:
        logger.error(f"Error in direct processing: {e}")
        raise

def extract_entities_simple(user_input: str) -> Dict[str, List[str]]:
    """
    Simple entity extraction without LLM parsing.
    """
    entities = {
        "music": [],
        "art": [],
        "fashion": [],
        "values": [],
        "places": [],
        "audiences": []
    }
    
    lines = user_input.split('\n')
    for line in lines:
        if ':' in line:
            category, values = line.split(':', 1)
            category = category.strip().lower()
            if category in entities:
                values_list = [v.strip() for v in values.split(',') if v.strip()]
                entities[category] = values_list
    
    return entities

def generate_cultural_profile(entities: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Generate cultural profile from entities.
    """
    # Create a simple identity based on the most common categories
    music_count = len(entities.get("music", []))
    art_count = len(entities.get("art", []))
    fashion_count = len(entities.get("fashion", []))
    
    if music_count > 0 and art_count > 0:
        identity = "Creative Cultural Explorer"
        description = "Someone who appreciates both music and visual arts, with a keen eye for style and cultural expression."
    elif music_count > 0:
        identity = "Music Enthusiast"
        description = "A passionate music lover with diverse cultural interests."
    elif art_count > 0:
        identity = "Art Aficionado"
        description = "Someone who deeply appreciates visual arts and creative expression."
    else:
        identity = "Cultural Explorer"
        description = "A curious individual exploring various cultural dimensions."
    
    return {
        "identity": identity,
        "description": description,
        "music": entities.get("music", []),
        "style": entities.get("fashion", [])
    }



def transform_result_to_api_format(result: Dict[str, Any]) -> ApiResponse:
    """
    Transform the LangGraph result to the API response format.
    """
    # Extract cultural profile
    cultural_profile = {
        "identity": result.get("cultural_profile", {}).get("identity", "Cultural Explorer"),
        "description": result.get("cultural_profile", {}).get("description", "A unique cultural identity"),
        "music": result.get("cultural_profile", {}).get("music", []),
        "style": result.get("cultural_profile", {}).get("style", [])
    }
    # Extract recommendations (brands/places como lista de dicts enriquecidos)
    recommendations = {
        "brands": result.get("recommendations", {}).get("brands", []),
        "places": result.get("recommendations", {}).get("places", [])
    }
    # Extract matching if available
    matching = None
    if "matching" in result and result["matching"]:
        matching = {
            "affinity_percentage": result["matching"].get("affinity_percentage", 0),
            "shared_interests": result["matching"].get("shared_interests", []),
            "audience_cluster": result["matching"].get("audience_cluster", "")
        }
    return ApiResponse(
        cultural_profile=cultural_profile,
        recommendations=recommendations,
        matching=matching
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 