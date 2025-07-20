#!/usr/bin/env python3
"""
Component test script for the AI Content Automation Agent
Tests individual components separately
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_content_generation():
    """Test content generation with real API"""
    print("🧪 Testing Content Generation with Real API...")
    
    try:
        from content_generator import ContentGenerator
        
        generator = ContentGenerator()
        
        # Test topic loading
        topic = generator.get_random_topic()
        print(f"✅ Selected topic: {topic}")
        
        # Test content generation
        content = generator.generate_content(topic)
        print(f"✅ Generated content ({len(content)} characters):")
        print(f"   {content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return False

def test_topics_loading():
    """Test topics file loading"""
    print("\n🧪 Testing Topics Loading...")
    
    try:
        with open('topics.txt', 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        
        print(f"✅ Loaded {len(topics)} topics:")
        for i, topic in enumerate(topics, 1):
            print(f"   {i}. {topic}")
        
        return True
        
    except Exception as e:
        print(f"❌ Topics loading failed: {e}")
        return False

def test_environment_setup():
    """Test environment variables"""
    print("\n🧪 Testing Environment Setup...")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    if api_key and api_key.startswith('sk-or-v1-'):
        print("✅ OpenRouter API key is properly set")
    else:
        print("❌ OpenRouter API key is missing or invalid")
        return False
    
    if folder_id and folder_id != 'your_folder_id_here':
        print(f"✅ Google Drive folder ID is set: {folder_id}")
    else:
        print("❌ Google Drive folder ID is missing or invalid")
        return False
    
    # Check credentials file
    if os.path.exists('credentials.json'):
        print("✅ Google credentials file found")
    else:
        print("❌ Google credentials file (credentials.json) not found")
        return False
    
    return True

def test_imports():
    """Test that all modules can be imported"""
    print("\n🧪 Testing Module Imports...")
    
    modules = [
        'content_generator',
        'google_docs_uploader', 
        'google_drive_uploader',
        'main'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ Successfully imported {module}")
        except Exception as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    
    return True

def main():
    """Run component tests"""
    print("🚀 AI Content Automation Agent - Component Tests\n")
    
    tests = [
        test_imports,
        test_environment_setup,
        test_topics_loading,
        test_content_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Component Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All component tests passed!")
        print("\n📝 Your AI Content Automation Agent is working correctly!")
        print("\n🔧 Next Steps:")
        print("1. For first-time Google authentication, run the script interactively:")
        print("   python main.py")
        print("2. Follow the browser authentication prompts")
        print("3. After authentication, the script will work automatically")
        print("4. Set up automation using Task Scheduler or cron")
    else:
        print("⚠️  Some component tests failed. Please fix the issues above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
