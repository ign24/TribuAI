"""
TribuAI - Main Application Entry Point

This module contains the main execution logic for TribuAI, including:
- LangGraph runner initialization
- CLI and demo modes
- Logging configuration
- Error handling and graceful shutdown
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
from loguru import logger

from app.langgraph_config import create_tribuai_graph
from app.utils import setup_logging, load_mock_data
from app.qloo_client import QlooClient


class TribuAI:
    """
    Main TribuAI application class that orchestrates the cultural intelligence engine.
    """
    
    def __init__(self):
        """Initialize TribuAI with configuration and dependencies."""
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        setup_logging()
        
        # Initialize components
        self.graph = create_tribuai_graph()
        self.qloo_client = QlooClient()
        
        logger.info("TribuAI initialized successfully")
    
    def run_interactive(self) -> None:
        """
        Run TribuAI in interactive CLI mode.
        """
        logger.info("Starting TribuAI in interactive mode")
        
        print("\n" + "="*50)
        print("🎭 Welcome to TribuAI - Cultural Intelligence Engine")
        print("="*50)
        print("Tell us about your cultural tastes and we'll discover your tribe!")
        print("Type 'quit' to exit, 'help' for commands\n")
        
        while True:
            try:
                user_input = input("🤔 What defines your cultural identity? (music, art, places, etc.): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thanks for exploring with TribuAI!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if not user_input:
                    print("Please provide some input about your cultural preferences.")
                    continue
                
                # Process the input through the graph
                result = self.process_input(user_input)
                self._display_results(result)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ An error occurred: {e}")
    
    def run_demo(self) -> Dict[str, Any]:
        """
        Run TribuAI in demo mode with mock data.
        
        Args:
            mock_input: Optional mock input to use instead of default
            
        Returns:
            Dictionary containing the demo results
        """
        logger.info("Starting TribuAI in demo mode")
        
        print(f"\n🧪 Demo Input: {user_input}")
        print("-" * 50)
        
        result = self.process_input(user_input)
        self._display_results(result)
        
        return result
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through the LangGraph pipeline.
        
        Args:
            user_input: User's cultural preferences description
            
        Returns:
            Dictionary containing the processed results
        """
        try:
            # Prepare input for the graph with proper state structure
            graph_input = {
                "user_input": user_input,
                "session_id": f"session_{hash(user_input) % 10000}",
                "timestamp": datetime.now().isoformat(),
                "combined_input": "",
                "extracted_entities": {},
                "cultural_profile": {},
                "recommendations": {},
                "matching": {},
                "current_node": "",
                "processing_time": 0.0,
                "error_message": None
            }
            
            logger.info(f"Processing input for session {graph_input['session_id']}")
            
            # Run the graph with streaming support
            result = self.graph.invoke(graph_input)
            
            logger.info(f"Successfully processed input, completed {result.get('current_node', 'unknown')} node")
            return result
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            raise
    
    def _display_results(self, result: Dict[str, Any]) -> None:
        """
        Display the results in a formatted way.
        
        Args:
            result: The result dictionary from the graph
        """
        print("\n" + "="*50)
        print("🎯 Your Cultural Profile Results")
        print("="*50)
        
        # Display profile information
        if "profile" in result:
            profile = result["profile"]
            print(f"👤 Cultural Identity: {profile.get('identity', 'N/A')}")
            print(f"🎵 Music Affinities: {', '.join(profile.get('music', []))}")
            print(f"🎨 Style Preferences: {', '.join(profile.get('style', []))}")
            print(f"🌍 Destinations: {', '.join(profile.get('destinations', []))}")
        
        # Display recommendations
        if "recommendations" in result:
            recs = result["recommendations"]
            print(f"\n💡 Brand Recommendations: {', '.join(recs.get('brands', []))}")
            print(f"🏙️ Places to Explore: {', '.join(recs.get('places', []))}")
            print(f"👥 Your Tribe: {', '.join(recs.get('audiences', []))}")
        
        # Display matching if available
        if "matching" in result:
            match = result["matching"]
            if match.get("suggested_match"):
                print(f"\n🤝 Suggested Match: {match['suggested_match']}")
        
        print("\n" + "="*50)
    
    def _show_help(self) -> None:
        """Display help information."""
        print("\n📖 TribuAI Commands:")
        print("  - Just type your cultural preferences!")
        print("  - 'help' - Show this help")
        print("  - 'quit' or 'exit' - Exit the application")
        print()


def main():
    """
    Main entry point for TribuAI application.
    """
    try:
        # Initialize TribuAI
        tribuai = TribuAI()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "demo":
                tribuai.run_demo()
            elif sys.argv[1] == "interactive":
                tribuai.run_interactive()
            else:
                print("Usage: python main.py [demo|interactive]")
                print("  demo - Run with mock data")
                print("  interactive - Run in CLI mode")
        else:
            # Default to interactive mode
            tribuai.run_interactive()
            
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 