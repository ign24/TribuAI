"""
TribuAI - LLM Parser Chain

This module contains the LangChain chain for parsing user responses and extracting
structured cultural entities, preferences, and signals.
"""

import json
from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
import os

from loguru import logger


class CulturalEntities(BaseModel):
    """Pydantic model for structured cultural entities."""
    
    music: List[str] = Field(
        description="List of music genres, artists, or musical preferences mentioned"
    )
    art: List[str] = Field(
        description="List of visual arts, films, design styles, or aesthetic preferences"
    )
    places: List[str] = Field(
        description="List of cities, destinations, or travel preferences mentioned"
    )
    fashion: List[str] = Field(
        description="List of clothing styles, brands, or fashion preferences"
    )
    values: List[str] = Field(
        description="List of social values, causes, or beliefs mentioned"
    )
    audiences: List[str] = Field(
        description="List of cultural audiences, communities, or subcultures identified"
    )


def create_parser_chain():
    """
    Create the LLM parser chain for extracting cultural entities.
    
    Returns:
        Configured LangChain chain
    """
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,  # Low temperature for consistent parsing
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create the prompt template
    prompt = PromptTemplate(
        input_variables=["input_text"],
        template="""
You are TribuAI's cultural intelligence parser. Your task is to extract structured cultural entities from user responses about their cultural preferences.

## User Input:
{input_text}

## Instructions:
Analyze the user's cultural preferences and extract the following entities:

1. **Music**: Genres, artists, musical experiences, or audio culture preferences
2. **Art**: Visual arts, films, design styles, aesthetic movements, or creative preferences  
3. **Places**: Cities, destinations, travel experiences, or location preferences
4. **Fashion**: Clothing styles, brands, aesthetic choices, or style preferences
5. **Values**: Social causes, beliefs, values, or cultural movements they identify with
6. **Audiences**: Cultural communities, subcultures, or social groups they might belong to

## Guidelines:
- Extract specific, concrete entities rather than vague descriptions
- Include both explicit mentions and implied cultural signals
- Normalize and standardize entity names
- Focus on cultural relevance and identity markers
- Limit each category to 3-5 most significant entities

## Output Format:
Return a JSON object with the following structure:
{{
    "music": ["entity1", "entity2", "entity3"],
    "art": ["entity1", "entity2", "entity3"], 
    "places": ["entity1", "entity2", "entity3"],
    "fashion": ["entity1", "entity2", "entity3"],
    "values": ["entity1", "entity2", "entity3"],
    "audiences": ["entity1", "entity2", "entity3"]
}}

Example:
If user says "I love Japanese cinema, brutalist architecture, and old-school hip hop", extract:
{{
    "music": ["old-school hip hop", "hip hop", "rap"],
    "art": ["Japanese cinema", "brutalist architecture", "minimalist design"],
    "places": ["Japan", "urban environments"],
    "fashion": ["streetwear", "minimalist style"],
    "values": ["authenticity", "urban culture"],
    "audiences": ["urban creatives", "hip hop culture", "minimalist enthusiasts"]
}}

Return only the JSON object, no additional text.
"""
    )
    
    # Create output parser
    output_parser = JsonOutputParser(pydantic_object=CulturalEntities)
    
    # Create the chain
    chain = prompt | llm | output_parser
    
    return chain


def parse_user_responses(user_input: str, survey_responses: List[str]) -> Dict[str, Any]:
    """
    Parse user responses and extract cultural entities.
    
    Args:
        user_input: Original user input
        survey_responses: List of user responses to survey questions
        
    Returns:
        Dictionary with extracted cultural entities
    """
    try:
        # Combine all user input for parsing
        combined_input = f"Original input: {user_input}\n\nSurvey responses:\n"
        for i, response in enumerate(survey_responses, 1):
            combined_input += f"Response {i}: {response}\n"
        
        # Create and run the parser chain
        parser_chain = create_parser_chain()
        
        result = parser_chain.invoke({
            "input_text": combined_input
        })
        
        logger.info(f"Successfully parsed user responses, extracted {sum(len(v) for v in result.dict().values())} entities")
        
        return result.dict()
        
    except Exception as e:
        logger.error(f"Error parsing user responses: {e}")
        
        # Fallback to basic extraction
        return {
            "music": ["indie", "alternative", "electronic"],
            "art": ["minimalist", "contemporary", "street art"],
            "places": ["urban", "creative cities", "cultural hubs"],
            "fashion": ["casual", "sustainable", "streetwear"],
            "values": ["creativity", "authenticity", "community"],
            "audiences": ["young professionals", "creative class", "urban millennials"]
        }


def extract_cultural_signals(entities: Dict[str, List[str]]) -> List[str]:
    """
    Extract cultural signals from parsed entities.
    
    Args:
        entities: Dictionary of parsed cultural entities
        
    Returns:
        List of cultural signals
    """
    signals = []
    
    # Extract signals from music preferences
    music = entities.get("music", [])
    if any("hip hop" in m.lower() for m in music):
        signals.append("urban_culture")
    if any("indie" in m.lower() for m in music):
        signals.append("indie_culture")
    if any("electronic" in m.lower() for m in music):
        signals.append("electronic_culture")
    
    # Extract signals from art preferences
    art = entities.get("art", [])
    if any("minimalist" in a.lower() for a in art):
        signals.append("minimalism")
    if any("street" in a.lower() for a in art):
        signals.append("street_culture")
    if any("japanese" in a.lower() for a in art):
        signals.append("japanese_culture")
    
    # Extract signals from fashion preferences
    fashion = entities.get("fashion", [])
    if any("sustainable" in f.lower() for f in fashion):
        signals.append("sustainability")
    if any("streetwear" in f.lower() for f in fashion):
        signals.append("street_fashion")
    
    # Extract signals from values
    values = entities.get("values", [])
    if any("sustainability" in v.lower() for v in values):
        signals.append("environmental_consciousness")
    if any("creativity" in v.lower() for v in values):
        signals.append("creative_expression")
    
    return list(set(signals))  # Remove duplicates


def validate_entities(entities: Dict[str, List[str]]) -> bool:
    """
    Validate extracted entities for quality and completeness.
    
    Args:
        entities: Dictionary of extracted entities
        
    Returns:
        True if entities are valid, False otherwise
    """
    # Check that we have at least some entities
    total_entities = sum(len(entities.get(category, [])) for category in entities)
    if total_entities < 3:
        logger.warning("Too few entities extracted")
        return False
    
    # Check that we have entities from multiple categories
    populated_categories = sum(1 for category in entities.values() if len(category) > 0)
    if populated_categories < 2:
        logger.warning("Entities too concentrated in few categories")
        return False
    
    return True 