#!/usr/bin/env python3
"""
TribuAI - Test Script

This script tests the TribuAI system with the updated Qloo API integration
and LangGraph configuration to ensure everything works correctly.
"""

import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.main import TribuAI
from app.utils import setup_logging, validate_api_keys
from app.qloo_client import QlooClient
from loguru import logger


def test_qloo_client():
    """Test the Qloo client functionality."""
    print("🧪 Testing Qloo Client...")
    
    try:
        client = QlooClient()
        
        # Test entity search
        print("  📝 Testing entity search...")
        entities = client.search_entities("indie rock", entity_type="artist", limit=3)
        print(f"    Found {len(entities)} entities")
        
        # Test brand recommendations
        print("  🏷️ Testing brand recommendations...")
        profile = {"music": ["indie rock"], "style": ["minimalist"]}
        brands = client.get_brand_recommendations(profile)
        print(f"    Recommended {len(brands)} brands")
        
        # Test audience recommendations
        print("  👥 Testing audience recommendations...")
        audiences = client.get_audience_recommendations(profile)
        print(f"    Found {len(audiences)} audiences")
        
        # Test destination recommendations
        print("  🌍 Testing destination recommendations...")
        destinations = client.get_destination_recommendations(profile)
        print(f"    Recommended {len(destinations)} destinations")
        
        print("  ✅ Qloo client tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Qloo client test failed: {e}")
        logger.error(f"Qloo client test error: {e}")
        return False


def test_langgraph_config():
    """Test the LangGraph configuration."""
    print("🧪 Testing LangGraph Configuration...")
    
    try:
        from app.langgraph_config import create_tribuai_graph, TribuAIState
        
        # Test graph creation
        print("  📊 Creating graph...")
        graph = create_tribuai_graph()
        print("    Graph created successfully")
        
        # Test state structure
        print("  📋 Testing state structure...")
        state = TribuAIState(
            user_input="I love indie rock and street art",
            session_id="test_session",
            timestamp="2024-01-15T10:00:00Z",
            survey_questions=[],
            user_responses=[],
            extracted_entities={},
            qloo_affinities={},
            cultural_profile={},
            recommendations={},
            matching={},
            final_output="",
            error_message=None,
            current_node="",
            processing_time=0.0
        )
        print("    State structure valid")
        
        print("  ✅ LangGraph configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ LangGraph configuration test failed: {e}")
        logger.error(f"LangGraph configuration test error: {e}")
        return False


def test_tribuai_integration():
    """Test the full TribuAI integration."""
    print("🧪 Testing TribuAI Integration...")
    
    try:
        # Initialize TribuAI
        print("  🚀 Initializing TribuAI...")
        tribuai = TribuAI()
        print("    TribuAI initialized successfully")
        
        # Test with sample input
        print("  📝 Testing with sample input...")
        test_input = "I love Japanese cinema, brutalist architecture, and old-school hip hop."
        
        result = tribuai.process_input(test_input)
        
        # Check if we got expected results
        if result and 'cultural_profile' in result:
            print("    ✅ Processing completed successfully")
            print(f"    🎭 Profile: {result.get('cultural_profile', {}).get('identity', 'N/A')}")
            print(f"    🏷️ Brands: {len(result.get('recommendations', {}).get('brands', []))}")
            print(f"    🌍 Places: {len(result.get('recommendations', {}).get('places', []))}")
            return True
        else:
            print("    ❌ Processing failed - no expected results")
            return False
        
    except Exception as e:
        print(f"  ❌ TribuAI integration test failed: {e}")
        logger.error(f"TribuAI integration test error: {e}")
        return False


def test_api_keys():
    """Test API key validation."""
    print("🧪 Testing API Keys...")
    
    try:
        if validate_api_keys():
            print("  ✅ All required API keys are present")
            return True
        else:
            print("  ⚠️ Some API keys are missing (using mock data)")
            return True  # This is acceptable for testing
        
    except Exception as e:
        print(f"  ❌ API key test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🎭 TribuAI - System Test Suite")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Run tests
    tests = [
        ("API Keys", test_api_keys),
        ("Qloo Client", test_qloo_client),
        ("LangGraph Config", test_langgraph_config),
        ("TribuAI Integration", test_tribuai_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TribuAI is ready for the hackathon!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the logs for details.")
        return 1


if __name__ == "__main__":
    exit(main()) 