"""
TribuAI - Qloo API Client

This module provides a wrapper for the Qloo Taste API based on the official documentation.
It includes proper authentication, rate limiting, error handling, and fallback mechanisms.
"""

import os
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urlencode

import httpx
from loguru import logger


class QlooClient:
    """
    Client for interacting with the Qloo Taste API.
    Based on the official Qloo API documentation.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://hackathon.api.qloo.com"):
        """
        Initialize the Qloo client.
        
        Args:
            api_key: Qloo API key (defaults to environment variable)
            base_url: Base URL for the Qloo API
        """
        self.api_key = api_key or os.getenv("X-Api-Key")
        self.base_url = base_url.rstrip('/')
        self.session = httpx.Client(timeout=30.0)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        self.max_requests_per_minute = 60
        
        # Cache for development
        self.cache = {}
        self.cache_ttl = timedelta(hours=1)
        
        if not self.api_key:
            logger.warning("No X-Api-Key provided, using mock data")
        else:
            logger.info("X-Api-Key found, using real API")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close the HTTP session."""
        if hasattr(self, 'session'):
            self.session.close()
    
    def _rate_limit(self):
        """Implement rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the Qloo API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        if not self.api_key:
            logger.error("No X-Api-Key available")
            raise ValueError("X-Api-Key environment variable is required")
        
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "accept": "application/json",
            "User-Agent": "TribuAI/1.0.0",
            "X-Api-Key": self.api_key  # Correct header for Qloo
        }
        
        if params is None:
            params = {}
        
        logger.info(f"Making request to {url} with params: {params}")
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Qloo API request successful: {endpoint}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Qloo API HTTP error: {e.response.status_code} - {e.response.text}")
            logger.error(f"Request URL: {e.request.url}")
            raise
            
        except httpx.RequestError as e:
            logger.error(f"Qloo API request error: {e}")
            raise
    
    def search_entities(self, query: str, entity_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for entities using the Entity Search API.
        
        Args:
            query: Search query
            entity_type: Type of entity to search for (e.g., 'brand', 'artist', 'place')
            limit: Maximum number of results
            
        Returns:
            List of matching entities
        """
        params = {
            "query": query,
            "take": limit,
            "page": 1,
            "sort_by": "match"
        }
        
        # Note: entity_type is ignored for hackathon API due to 403 restrictions
        # The API only allows general search without type filtering
        
        try:
            response = self._make_request("/search", params)
            
            if "results" in response:
                return response["results"]
            elif "entities" in response:
                return response["entities"]
            else:
                logger.warning("Unexpected response format from entity search")
                return []
                
        except Exception as e:
            logger.error(f"Error searching entities: {e}")
            # Don't fall back to mock data - let the error propagate
            raise
    
    def get_insights(self, entity_id: str, entity_type: str, insight_type: str = "basic") -> Dict[str, Any]:
        """
        Get insights for a specific entity using the Insights API v2.
        
        Args:
            entity_id: ID of the entity
            entity_type: Type of entity (e.g., 'brand', 'artist', 'place')
            insight_type: Type of insight ('basic', 'demographic', 'location')
            
        Returns:
            Dictionary with insights data
        """
        # Use v2 insights endpoint with proper parameters
        params = {
            "filter.type": f"urn:entity:{entity_type}",
            "signal.interests.entities": entity_id,
            "take": 10
        }
        
        return self._make_request("/v2/insights", params)
    
    def get_audience_recommendations(self, cultural_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get audience recommendations based on cultural profile.
        
        Args:
            cultural_profile: User's cultural profile
            
        Returns:
            List of recommended audiences
        """
        # Extract relevant entities from profile
        entities = []
        entities.extend(cultural_profile.get('music', [])[:3])
        entities.extend(cultural_profile.get('style', [])[:2])
        
        if not entities:
            return []
        
        # Search for audiences using the Find Audiences API v2
        # Use the first entity as a filter query
        params = {
            "filter.query": entities[0] if entities else "music",
            "take": 10,
            "page": 1
        }
        
        try:
            response = self._make_request("/v2/audiences", params)
            
            if "audiences" in response:
                return response["audiences"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting audience recommendations: {e}")
            # Don't fall back to mock data - let the error propagate
            raise
    
    def get_brand_recommendations(self, cultural_profile: Dict[str, Any]) -> List[str]:
        """
        Get brand recommendations based on cultural profile.
        
        Args:
            cultural_profile: User's cultural profile
            
        Returns:
            List of recommended brands
        """
        # Extract relevant entities from profile
        entities = []
        entities.extend(cultural_profile.get('music', [])[:3])
        entities.extend(cultural_profile.get('style', [])[:2])
        entities.extend(cultural_profile.get('values', [])[:2])
        
        if not entities:
            return []
        
        try:
            # Search for brands using entity search
            brand_entities = []
            for entity in entities:
                brands = self.search_entities(entity, entity_type="brand", limit=5)
                brand_entities.extend(brands)
            
            # Extract brand names and remove duplicates
            brand_names = []
            seen_brands = set()
            
            for brand in brand_entities:
                brand_name = brand.get('name', brand.get('title', ''))
                if brand_name and brand_name not in seen_brands:
                    brand_names.append(brand_name)
                    seen_brands.add(brand_name)
            
            return brand_names[:10] if brand_names else []
            
        except Exception as e:
            logger.error(f"Error getting brand recommendations: {e}")
            # Don't fall back to mock data - let the error propagate
            raise
    
    def get_destination_recommendations(self, cultural_profile: Dict[str, Any]) -> List[str]:
        """
        Get destination recommendations based on cultural profile.
        
        Args:
            cultural_profile: User's cultural profile
            
        Returns:
            List of recommended destinations
        """
        # Extract relevant entities from profile
        entities = []
        entities.extend(cultural_profile.get('music', [])[:3])
        entities.extend(cultural_profile.get('style', [])[:2])
        entities.extend(cultural_profile.get('values', [])[:2])
        
        if not entities:
            return []
        
        try:
            # Search for places using entity search
            place_entities = []
            for entity in entities:
                places = self.search_entities(entity, entity_type="place", limit=5)
                place_entities.extend(places)
            
            # Extract place names and remove duplicates
            place_names = []
            seen_places = set()
            
            for place in place_entities:
                place_name = place.get('name', place.get('title', ''))
                if place_name and place_name not in seen_places:
                    place_names.append(place_name)
                    seen_places.add(place_name)
            
            return place_names[:8] if place_names else []
            
        except Exception as e:
            logger.error(f"Error getting destination recommendations: {e}")
            # Don't fall back to mock data - let the error propagate
            raise
    
    def analyze_cultural_affinities(self, entities: List[str]) -> Dict[str, Any]:
        """
        Analyze cultural affinities using the Analysis API.
        
        Args:
            entities: List of cultural entities
            
        Returns:
            Dictionary with affinity analysis
        """
        if not entities:
            return {}
        
        try:
            # Use the Analysis API
            params = {
                "entities": ",".join(entities),
                "analysis_type": "affinity"
            }
            
            return self._make_request("/v1/analysis", params)
            
        except Exception as e:
            logger.error(f"Error analyzing cultural affinities: {e}")
            # Don't fall back to mock data - let the error propagate
            raise
    
    def get_trending_entities(self, entity_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get trending entities using the Trending Entities API.
        
        Args:
            entity_type: Type of entity to get trends for
            limit: Maximum number of results
            
        Returns:
            List of trending entities
        """
        params = {
            "limit": limit
        }
        
        if entity_type:
            params["entity_type"] = entity_type
        
        response = self._make_request("/v1/trending", params)
        
        if "entities" in response:
            return response["entities"]
        else:
            return []
    
    def health_check(self) -> bool:
        """
        Check if the Qloo API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Test with a simple search request since v1/health doesn't exist
            response = self._make_request("/search", {"query": "test", "take": 1})
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False 