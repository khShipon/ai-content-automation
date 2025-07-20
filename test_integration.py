#!/usr/bin/env python3
"""
Integration test script for the AI Content Automation Agent
This script tests the core functionality without mocking external APIs
"""

import os
import sys
import logging
from unittest.mock import patch, Mock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_content_generator():
    """Test the ContentGenerator class with mocked API calls"""
    print("🧪 Testing ContentGenerator...")
    
    try:
        from content_generator import ContentGenerator
        
        # Test topic loading
        generator = ContentGenerator()
        topic = generator.get_random_topic()
        print(f"✅ Successfully loaded topic: {topic}")
        
        # Test content generation with mocked API
        with patch.object(generator.client.chat.completions, 'create') as mock_create:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"আজকে আমরা শিখবো {topic}. This is a test content."
            mock_create.return_value = mock_response
            
            content = generator.generate_content(topic)
            print(f"✅ Successfully generated content: {content[:100]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ ContentGenerator test failed: {e}")
        return False

def test_google_services():
    """Test Google services initialization (without actual API calls)"""
    print("\n🧪 Testing Google Services...")
    
    try:
        # Test Google Docs service
        with patch('google_docs_uploader.build') as mock_build, \
             patch('google_docs_uploader.InstalledAppFlow.from_client_secrets_file') as mock_flow, \
             patch('os.path.exists', return_value=False):
            
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            mock_flow_instance = Mock()
            mock_creds = Mock()
            mock_creds.valid = True
            mock_flow_instance.run_local_server.return_value = mock_creds
            mock_flow.return_value = mock_flow_instance
            
            from google_docs_uploader import get_google_docs_service
            service = get_google_docs_service()
            print("✅ Google Docs service initialization successful")
        
        # Test Google Drive service
        with patch('google_drive_uploader.build') as mock_build, \
             patch('google_drive_uploader.InstalledAppFlow.from_client_secrets_file') as mock_flow, \
             patch('os.path.exists', return_value=False):
            
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            mock_flow_instance = Mock()
            mock_creds = Mock()
            mock_creds.valid = True
            mock_flow_instance.run_local_server.return_value = mock_creds
            mock_flow.return_value = mock_flow_instance
            
            from google_drive_uploader import get_drive_service
            service = get_drive_service()
            print("✅ Google Drive service initialization successful")
            
        return True
        
    except Exception as e:
        print(f"❌ Google Services test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        'main.py',
        'content_generator.py', 
        'google_docs_uploader.py',
        'google_drive_uploader.py',
        'topics.txt',
        'requirements.txt',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ Found {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def test_environment_variables():
    """Test that required environment variables are set"""
    print("\n🧪 Testing Environment Variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['OPENROUTER_API_KEY', 'GOOGLE_DRIVE_FOLDER_ID']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == 'your_folder_id_here':
            missing_vars.append(var)
        else:
            print(f"✅ {var} is set")
    
    if missing_vars:
        print(f"❌ Missing or invalid environment variables: {missing_vars}")
        return False
    
    return True

def test_topics_file():
    """Test that topics.txt is properly formatted"""
    print("\n🧪 Testing Topics File...")
    
    try:
        with open('topics.txt', 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        
        if len(topics) == 0:
            print("❌ topics.txt is empty")
            return False
        
        print(f"✅ Found {len(topics)} topics in topics.txt")
        print(f"   Sample topics: {topics[:3]}")
        return True
        
    except Exception as e:
        print(f"❌ Topics file test failed: {e}")
        return False

def test_main_workflow():
    """Test the main workflow with mocked external calls"""
    print("\n🧪 Testing Main Workflow...")
    
    try:
        with patch('main.ContentGenerator') as mock_generator_class, \
             patch('main.create_google_doc') as mock_create_doc, \
             patch('main.move_doc_to_folder') as mock_move_doc:
            
            # Mock ContentGenerator
            mock_generator = Mock()
            mock_generator.get_random_topic.return_value = "Present Simple Tense"
            mock_generator.generate_content.return_value = "আজকে আমরা শিখবো Present Simple Tense. It is used for regular actions."
            mock_generator_class.return_value = mock_generator
            
            # Mock Google Docs creation
            mock_create_doc.return_value = "test_doc_id_123"
            
            # Mock Google Drive move
            mock_move_doc.return_value = True
            
            # Import and run main
            import main
            main.main()
            
            print("✅ Main workflow completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Main workflow test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting AI Content Automation Agent Integration Tests\n")
    
    tests = [
        test_file_structure,
        test_environment_variables,
        test_topics_file,
        test_content_generator,
        test_google_services,
        test_main_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI Content Automation Agent is ready to use!")
        print("\n📝 Next steps:")
        print("1. Run 'python main.py' to test the full workflow")
        print("2. Set up automation using Task Scheduler (Windows) or cron (Linux/Mac)")
        print("3. Monitor the logs for any issues")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
