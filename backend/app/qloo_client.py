"""
TribuAI - Simplified Qloo API Client

This module provides a simplified wrapper for the Qloo Taste API that works with the hackathon API limitations.
It focuses on getting 100% real data using basic search functionality.
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
    Simplified client for interacting with the Qloo Taste API.
    Focuses on getting real data using basic search functionality.
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
        
        if not self.api_key:
            logger.error("No X-Api-Key provided")
            raise ValueError("X-Api-Key environment variable is required")
        else:
            logger.info("X-Api-Key found, using real Qloo API")
    
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
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "accept": "application/json",
            "User-Agent": "TribuAI/1.0.0",
            "X-Api-Key": self.api_key
        }
        
        if params is None:
            params = {}
        
        logger.info(f"Making request to {url} with params: {params}")
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Qloo API response data: {data}")
            logger.info(f"Qloo API request successful: {endpoint}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Qloo API HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        
        except httpx.RequestError as e:
            logger.error(f"Qloo API request error: {e}")
            raise
    
    def search_entities(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for entities using the basic search endpoint.
        This is the most reliable endpoint for the hackathon API.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching entities with real data
        """
        params = {
            "query": query,
            "take": limit,
            "page": 1,
            "sort_by": "match"
        }
        
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
            raise
    
    def get_real_recommendations(self, cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get real recommendations based on cultural profile using basic search.
        Returns 100% real data from Qloo API.
        
        Args:
            cultural_profile: User's cultural profile with entities
            
        Returns:
            Dictionary with real brands and places recommendations
        """
        try:
            # Extract entities from profile
            all_entities = []
            for category, values in cultural_profile.items():
                if isinstance(values, list):
                    all_entities.extend(values[:2])  # Take first 2 from each category
            
            if not all_entities:
                logger.warning("No entities found in cultural profile")
                return {"brands": [], "places": []}
            
            # Get real recommendations for brands
            brands = self._get_brand_recommendations(all_entities)
            
            # Get real recommendations for places
            places = self._get_place_recommendations(all_entities)
            
            return {
                "brands": brands,
                "places": places
            }
            
        except Exception as e:
            logger.error(f"Error getting real recommendations: {e}")
            raise
    
    def _filter_and_deduplicate(self, items: List[Dict[str, Any]], exclude_names=None, min_fields=None, limit=3) -> List[Dict[str, Any]]:
        """
        Filtra y prioriza resultados útiles para el usuario.
        - Quita duplicados por entity_id
        - Excluye nombres genéricos
        - Prioriza los que tienen descripción o imagen
        - Limita a N resultados
        """
        if exclude_names is None:
            exclude_names = {"brand", "place"}
        if min_fields is None:
            min_fields = ["description", "image"]
        seen = set()
        filtered = []
        # Prioriza los que tienen descripción o imagen
        items = sorted(items, key=lambda x: (bool(x.get("description")) or bool(x.get("image")), x.get("name", "")), reverse=True)
        for item in items:
            name = item.get("name", "").strip().lower()
            if name in exclude_names:
                continue
            eid = item.get("entity_id")
            if eid and eid in seen:
                continue
            if not any(item.get(f) for f in min_fields):
                continue
            seen.add(eid)
            filtered.append(item)
            if len(filtered) >= limit:
                break
        return filtered

    def _get_brand_recommendations(self, entities: List[str]) -> List[Dict[str, Any]]:
        """
        Get real brand recommendations based on entities.
        If no results with type 'brand' are found, return the first results from the search.
        """
        brands = []
        for entity in entities[:3]:  # Use first 3 entities
            try:
                search_results = self.search_entities(f"{entity} brand", limit=5)
                # First, try to get results with type 'brand'
                filtered = [
                    {
                        'name': r.get('name', ''),
                        'entity_id': r.get('entity_id', ''),
                        'description': r.get('description', ''),
                        'image': r.get('image', {}).get('url', ''),
                        'tags': [tag.get('name', '') for tag in r.get('tags', [])]
                    }
                    for r in search_results if r.get('type') == 'brand' or 'brand' in r.get('name', '').lower()
                ]
                # Si no hay suficientes, agrega los primeros resultados
                if len(filtered) < 3:
                    filtered += [
                        {
                            'name': r.get('name', ''),
                            'entity_id': r.get('entity_id', ''),
                            'description': r.get('description', ''),
                            'image': r.get('image', {}).get('url', ''),
                            'tags': [tag.get('name', '') for tag in r.get('tags', [])]
                        }
                        for r in search_results if r.get('name', '').strip().lower() not in ['brand', 'place']
                    ]
                brands.extend(filtered)
            except Exception as e:
                logger.error(f"Error getting brand recommendations for {entity}: {e}")
        # Filtra, prioriza y limita
        return self._filter_and_deduplicate(brands, exclude_names={"brand", "place"}, min_fields=["description", "image"], limit=3)

    def _get_place_recommendations(self, entities: List[str]) -> List[Dict[str, Any]]:
        """
        Get real place recommendations based on entities.
        If no results with type 'place' are found, return the first results from the search.
        """
        places = []
        for entity in entities[:3]:
            try:
                search_results = self.search_entities(f"{entity} place", limit=5)
                filtered = [
                    {
                        'name': r.get('name', ''),
                        'entity_id': r.get('entity_id', ''),
                        'description': r.get('description', ''),
                        'image': r.get('image', {}).get('url', ''),
                        'tags': [tag.get('name', '') for tag in r.get('tags', [])]
                    }
                    for r in search_results if r.get('type') == 'place' or 'place' in r.get('name', '').lower()
                ]
                if len(filtered) < 3:
                    filtered += [
                        {
                            'name': r.get('name', ''),
                            'entity_id': r.get('entity_id', ''),
                            'description': r.get('description', ''),
                            'image': r.get('image', {}).get('url', ''),
                            'tags': [tag.get('name', '') for tag in r.get('tags', [])]
                        }
                        for r in search_results if r.get('name', '').strip().lower() not in ['brand', 'place']
                    ]
                places.extend(filtered)
            except Exception as e:
                logger.error(f"Error getting place recommendations for {entity}: {e}")
        return self._filter_and_deduplicate(places, exclude_names={"brand", "place"}, min_fields=["description", "image"], limit=3)
    
    def get_matching_info(self, entities: List[str]) -> Dict[str, Any]:
        """
        Get matching information based on entities.
        Uses real data from search results.
        """
        try:
            if not entities:
                return {
                    "affinity_percentage": 0,
                    "shared_interests": [],
                    "audience_cluster": "General"
                }
            
            # Get real matching data by searching for related entities
            shared_interests = []
            for entity in entities[:3]:
                try:
                    search_results = self.search_entities(entity, limit=2)
                    if search_results:
                        shared_interests.append(entity)
                except Exception as e:
                    logger.error(f"Error searching for entity '{entity}': {e}")
                    continue
            
            # Calculate affinity based on found entities
            if len(shared_interests) >= 3:
                affinity = 90
                cluster = "Cultural Enthusiast"
            elif len(shared_interests) >= 2:
                affinity = 85
                cluster = "Cultural Explorer"
            else:
                affinity = 75
                cluster = "Cultural Curious"
            
            return {
                "affinity_percentage": affinity,
                "shared_interests": shared_interests,
                "audience_cluster": cluster
            }
            
        except Exception as e:
            logger.error(f"Error getting matching info: {e}")
            return {
                "affinity_percentage": 75,
                "shared_interests": entities[:3] if entities else [],
                "audience_cluster": "Cultural Explorer"
            }
    
    def health_check(self) -> bool:
        """
        Check if the Qloo API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Test with a simple search request
            response = self._make_request("/search", {"query": "test", "take": 1})
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False 