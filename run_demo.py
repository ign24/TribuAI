#!/usr/bin/env python3
"""
TribuAI - Demo Runner

This script provides a quick way to test and demonstrate TribuAI functionality.
It can run with mock data, sample inputs, or interactive mode.
"""

import sys
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.main import TribuAI
from app.utils import load_mock_data, setup_logging
from loguru import logger


def run_sample_demo():
    """Run TribuAI with sample inputs from mock data."""
    print("\n" + "="*60)
    print("🎭 TribuAI Demo - Cultural Intelligence Engine")
    print("="*60)
    
    # Load mock data
    mock_data = load_mock_data("data/mock_inputs.json")
    sample_inputs = mock_data.get("sample_inputs", [])
    
    if not sample_inputs:
        print("❌ No sample inputs found in mock data")
        return
    
    # Initialize TribuAI
    try:
        tribuai = TribuAI()
        print("✅ TribuAI initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize TribuAI: {e}")
        return
    
    # Run demo with each sample input
    for i, sample in enumerate(sample_inputs[:3], 1):  # Limit to first 3 samples
        print(f"\n{'='*20} Sample {i} {'='*20}")
        print(f"📝 Input: {sample['input']}")
        print(f"📋 Description: {sample['description']}")
        print(f"🎯 Expected Profile: {sample['expected_profile']}")
        
        try:
            # Process the input
            result = tribuai.process_input(sample['input'])
            
            # Display results
            tribuai._display_results(result)
            
        except Exception as e:
            print(f"❌ Error processing sample {i}: {e}")
            logger.error(f"Demo error for sample {i}: {e}")
    
    print(f"\n{'='*60}")
    print("🎉 Demo completed! TribuAI is ready for the hackathon.")
    print("="*60)


def run_interactive_demo():
    """Run TribuAI in interactive mode."""
    print("\n" + "="*60)
    print("🎭 TribuAI Interactive Demo")
    print("="*60)
    
    try:
        tribuai = TribuAI()
        tribuai.run_interactive()
    except Exception as e:
        print(f"❌ Error in interactive demo: {e}")
        logger.error(f"Interactive demo error: {e}")


def run_single_test(input_text: str):
    """Run TribuAI with a single custom input."""
    print(f"\n🎭 Testing TribuAI with: '{input_text}'")
    print("-" * 50)
    
    try:
        tribuai = TribuAI()
        result = tribuai.process_input(input_text)
        tribuai._display_results(result)
    except Exception as e:
        print(f"❌ Error in test: {e}")
        logger.error(f"Test error: {e}")


def show_help():
    """Display help information."""
    print("\n📖 TribuAI Demo Usage:")
    print("  python run_demo.py                    # Run sample demo")
    print("  python run_demo.py interactive        # Run interactive demo")
    print("  python run_demo.py test 'your input'  # Test with custom input")
    print("  python run_demo.py help               # Show this help")
    print("\n💡 Examples:")
    print("  python run_demo.py test 'I love indie rock and street art'")
    print("  python run_demo.py test 'I enjoy electronic music and coffee culture'")


def main():
    """Main entry point for the demo script."""
    # Setup logging
    setup_logging()
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - run sample demo
        run_sample_demo()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "interactive":
            run_interactive_demo()
        elif sys.argv[1] == "help":
            show_help()
        else:
            print(f"❌ Unknown command: {sys.argv[1]}")
            show_help()
    elif len(sys.argv) == 3 and sys.argv[1] == "test":
        # Test with custom input
        input_text = sys.argv[2]
        run_single_test(input_text)
    else:
        print("❌ Invalid arguments")
        show_help()


if __name__ == "__main__":
    main() 