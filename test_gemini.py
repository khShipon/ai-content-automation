#!/usr/bin/env python3
"""
Test script for the new Gemini Flash Lite 2.5 model
"""

import logging
from content_generator import ContentGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_gemini_content_generation():
    """Test content generation with the new Gemini model"""
    print("🧪 Testing Gemini Flash Lite 2.5 Content Generation...")
    
    try:
        generator = ContentGenerator()
        
        # Test with a few different topics
        test_topics = [
            "Present Simple Tense",
            "Bangla Food Culture", 
            "Technology in Education",
            "Daily Routines"
        ]
        
        for topic in test_topics:
            print(f"\n📝 Generating content for: {topic}")
            content = generator.generate_content(topic)
            print(f"✅ Generated content ({len(content)} characters):")
            print(f"   {content}")
            print("-" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return False

def main():
    """Run Gemini test"""
    print("🚀 Testing AI Content Generation with Gemini Flash Lite 2.5\n")
    
    if test_gemini_content_generation():
        print("\n🎉 Gemini Flash Lite 2.5 is working perfectly!")
        print("✅ Your AI Content Automation Agent is ready!")
    else:
        print("\n❌ There was an issue with content generation.")
    
    return 0

if __name__ == "__main__":
    exit(main())
