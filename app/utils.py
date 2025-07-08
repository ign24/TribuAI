"""
TribuAI - Utility Functions

This module contains utility functions for TribuAI, including:
- Logging setup and configuration
- Data loading and validation
- Helper functions for formatting and processing
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from loguru import logger
import pandas as pd


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration for TribuAI.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with custom format
    logger.add(
        "logs/tribuai.log",
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        backtrace=True,
        diagnose=True
    )
    
    # Add console output
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    logger.info("Logging setup completed")


def load_mock_data(file_path: str) -> Dict[str, Any]:
    """
    Load mock data from JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the mock data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded mock data from {file_path}")
        return data
    except FileNotFoundError:
        logger.warning(f"Mock data file {file_path} not found, using defaults")
        return get_default_mock_data()
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from {file_path}: {e}")
        return get_default_mock_data()


def get_default_mock_data() -> Dict[str, Any]:
    """
    Get default mock data for TribuAI.
    
    Returns:
        Dictionary with default mock data
    """
    return {
        "sample_inputs": [
            "I love Japanese cinema, brutalist architecture, and old-school hip hop.",
            "I'm into indie rock, street art, and sustainable fashion.",
            "I enjoy electronic music, minimalist design, and coffee culture."
        ],
        "sample_profiles": [
            {
                "identity": "Urban Creative Minimalist",
                "music": ["indie", "electronic", "alternative"],
                "style": ["minimalist", "sustainable", "streetwear"],
                "destinations": ["Berlin", "Tokyo", "Portland"],
                "values": ["sustainability", "creativity"]
            }
        ]
    }


def save_results(results: Dict[str, Any], session_id: str) -> str:
    """
    Save TribuAI results to a JSON file.
    
    Args:
        results: Results dictionary to save
        session_id: Session identifier
        
    Returns:
        Path to the saved file
    """
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tribuai_results_{session_id}_{timestamp}.json"
    filepath = results_dir / filename
    
    # Add metadata
    results_with_metadata = {
        "session_id": session_id,
        "timestamp": timestamp,
        "version": "1.0.0",
        "results": results
    }
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results_with_metadata, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Results saved to {filepath}")
    return str(filepath)


def validate_api_keys() -> bool:
    """
    Validate that required API keys are present.
    
    Returns:
        True if all required keys are present, False otherwise
    """
    required_keys = ["OPENAI_API_KEY", "X-Api-Key"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        logger.error(f"Missing required API keys: {', '.join(missing_keys)}")
        print(f"  ⚠️ Some API keys are missing (using mock data)")
        return False
    else:
        logger.info("All required API keys are present")
        return True


def format_cultural_profile(profile: Dict[str, Any]) -> str:
    """
    Format cultural profile for display.
    
    Args:
        profile: Cultural profile dictionary
        
    Returns:
        Formatted string representation
    """
    lines = []
    lines.append(f"🎭 Cultural Identity: {profile.get('identity', 'N/A')}")
    lines.append(f"🎵 Music: {', '.join(profile.get('music', []))}")
    lines.append(f"🎨 Style: {', '.join(profile.get('style', []))}")
    lines.append(f"🌍 Destinations: {', '.join(profile.get('destinations', []))}")
    lines.append(f"💭 Values: {', '.join(profile.get('values', []))}")
    
    return "\n".join(lines)


def format_recommendations(recommendations: Dict[str, Any]) -> str:
    """
    Format recommendations for display.
    
    Args:
        recommendations: Recommendations dictionary
        
    Returns:
        Formatted string representation
    """
    lines = []
    lines.append("💡 Recommendations:")
    lines.append(f"  🏷️ Brands: {', '.join(recommendations.get('brands', []))}")
    lines.append(f"  🏙️ Places: {', '.join(recommendations.get('places', []))}")
    lines.append(f"  👥 Your Tribe: {', '.join(recommendations.get('audiences', []))}")
    
    if 'experiences' in recommendations:
        lines.append(f"  🎯 Experiences:")
        for exp in recommendations.get('experiences', []):
            lines.append(f"    • {exp}")
    
    return "\n".join(lines)


def calculate_similarity(profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
    """
    Calculate similarity between two cultural profiles.
    
    Args:
        profile1: First cultural profile
        profile2: Second cultural profile
        
    Returns:
        Similarity score between 0 and 1
    """
    # Simple similarity calculation based on shared interests
    # In production, this would use more sophisticated algorithms
    
    shared_interests = 0
    total_interests = 0
    
    # Compare music preferences
    music1 = set(profile1.get('music', []))
    music2 = set(profile2.get('music', []))
    shared_interests += len(music1.intersection(music2))
    total_interests += len(music1.union(music2))
    
    # Compare style preferences
    style1 = set(profile1.get('style', []))
    style2 = set(profile2.get('style', []))
    shared_interests += len(style1.intersection(style2))
    total_interests += len(style1.union(style2))
    
    # Compare destinations
    dest1 = set(profile1.get('destinations', []))
    dest2 = set(profile2.get('destinations', []))
    shared_interests += len(dest1.intersection(dest2))
    total_interests += len(dest1.union(dest2))
    
    if total_interests == 0:
        return 0.0
    
    return shared_interests / total_interests


def create_session_id(user_input: str) -> str:
    """
    Create a unique session ID based on user input.
    
    Args:
        user_input: User's input text
        
    Returns:
        Unique session identifier
    """
    import hashlib
    
    # Create hash from user input
    hash_object = hashlib.md5(user_input.encode())
    hash_hex = hash_object.hexdigest()[:8]
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%H%M%S")
    
    return f"session_{hash_hex}_{timestamp}"


def sanitize_input(text: str) -> str:
    """
    Sanitize user input for safe processing.
    
    Args:
        text: Raw user input
        
    Returns:
        Sanitized text
    """
    # Remove potentially harmful characters
    import re
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Limit length
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    return text.strip() 