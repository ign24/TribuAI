"""
TribuAI - LLM Parser Chain

This module contains the LangChain chain for parsing user responses and extracting
structured cultural entities, preferences, and signals.
"""

import json
from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from loguru import logger


def create_parser_chain():
    """
    Create the LLM parser chain for extracting cultural entities.
    
    Returns:
        Configured LangChain chain
    """
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,  # Higher temperature for more creative extraction
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create the prompt template
    prompt = PromptTemplate(
        input_variables=["input_text"],
        template="""
You are TribuAI's cultural intelligence parser. Your task is to extract structured cultural entities and signals from user responses about their cultural preferences.

## User Input:
{input_text}

## Instructions:
Analyze the user's cultural preferences and extract the following for each relevant entity or interest:

- name: The canonical name of the entity or interest
- type: One of Qloo's types (artist, brand, place, destination, book, movie, podcast, tv_show, video_game, tag, audience)
- tags: List of relevant tags or keywords (genres, styles, attributes, etc.)
- context: (Optional) Disambiguating details (city, country, year, etc.)

If you can infer a relevant audience (group of people with shared tastes), include it as an entity of type "audience".

## Output Format:
Return a JSON object with this structure:
{{
  "entities": [
    {{"name": "...", "type": "...", "tags": ["..."], "context": "..."}},
    ...
  ]
}}

## Example:
If user says "I love Japanese cinema, brutalist architecture, and old-school hip hop, and I feel at home in Berlin":
{{
  "entities": [
    {{"name": "Japanese Cinema", "type": "movie", "tags": ["cinema", "Japan", "film"], "context": ""}},
    {{"name": "Brutalist Architecture", "type": "tag", "tags": ["architecture", "minimalism"], "context": ""}},
    {{"name": "Old-school Hip Hop", "type": "artist", "tags": ["hip hop", "music genre"], "context": ""}},
    {{"name": "Berlin", "type": "place", "tags": ["city", "Europe"], "context": "Germany"}},
    {{"name": "Indie Music Fans", "type": "audience", "tags": ["music", "indie"], "context": ""}}
  ]
}}

Return only the JSON object, no additional text.
"""
    )
    
    # Output parser expects a dict with an 'entities' key
    def parse_entities(output: str):
        # If output is an object with .content, extract the string
        if hasattr(output, 'content'):
            output = output.content
        print("LLM RAW OUTPUT (content):", output)
        logger.info(f"LLM RAW OUTPUT (content): {output}")
        try:
            data = json.loads(output)
            if "entities" in data and isinstance(data["entities"], list):
                return data
            else:
                return {"entities": []}
        except Exception:
            return {"entities": []}
    
    # Create the chain
    chain = prompt | llm | parse_entities
    
    return chain


def parse_user_responses(user_input: str, survey_responses: List[str]) -> Dict[str, Any]:
    """
    Parse user responses and extract cultural entities.
    
    Args:
        user_input: Original user input
        survey_responses: List of user responses to survey questions
        
    Returns:
        Dictionary with extracted cultural entities (with 'entities' key)
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
        
        logger.info(f"Successfully parsed user responses, extracted {len(result.get('entities', []))} entities")
        
        return result
        
    except Exception as e:
        logger.error(f"Error parsing user responses: {e}")
        
        # Fallback to basic extraction
        return {
            "entities": [
                {"name": "indie", "type": "artist", "tags": [], "context": ""},
                {"name": "minimalist", "type": "art", "tags": [], "context": ""},
                {"name": "urban", "type": "place", "tags": [], "context": ""},
                {"name": "casual", "type": "brand", "tags": [], "context": ""},
                {"name": "creativity", "type": "tag", "tags": [], "context": ""},
                {"name": "young professionals", "type": "audience", "tags": [], "context": ""}
            ]
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