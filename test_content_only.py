#!/usr/bin/env python3
"""
Test script to show generated content without Google services
"""

import logging
import datetime
from content_generator import ContentGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Test content generation and show the output"""
    print("🚀 AI Content Automation Agent - Content Generation Test\n")
    
    try:
        # Step 1: Generate content
        generator = ContentGenerator()
        topic = generator.get_random_topic()
        content = generator.generate_content(topic)
        
        # Step 2: Show what would be created
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        doc_title = f"{today} - {topic}"
        
        print("=" * 80)
        print(f"📄 Document Title: {doc_title}")
        print("=" * 80)
        print(f"📝 Generated Content:\n")
        print(content)
        print("=" * 80)
        print(f"✅ Content successfully generated for topic: {topic}")
        print(f"📊 Content length: {len(content)} characters")
        print(f"📅 Document would be created with title: {doc_title}")
        print("\n🔧 Next step: Complete Google authentication to enable automatic document creation and upload.")
        
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
