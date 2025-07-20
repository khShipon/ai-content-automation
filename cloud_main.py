#!/usr/bin/env python3
"""
Cloud-compatible version of the AI Content Automation Agent
Designed to work with GitHub Actions and service account authentication
"""

import logging
import os
import json
import datetime
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

# Content topics
TOPICS = [
    "Healthy Habits",
    "Technology Trends",
    "Personal Development",
    "Environmental Awareness",
    "Digital Marketing",
    "Remote Work Tips",
    "Financial Planning",
    "Mental Health",
    "Productivity Hacks",
    "Social Media Strategy"
]

class CloudContentGenerator:
    """Cloud-compatible content generator"""
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
    
    def get_random_topic(self):
        """Get a random topic from the list"""
        topic = random.choice(TOPICS)
        logging.info(f"Selected topic: {topic}")
        return topic
    
    def generate_content(self, topic):
        """Generate content using OpenRouter API"""
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create an engaging blog post about "{topic}" in mixed Bangla-English format. 
        
        Requirements:
        - Write 800-1000 words
        - Use both Bangla and English naturally
        - Include practical tips and examples
        - Make it engaging and informative
        - Add relevant headings and subheadings
        - Target audience: Young professionals and students
        
        Topic: {topic}"""
        
        data = {
            "model": "google/gemini-2.5-flash-lite-preview-06-17",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            logging.info(f"Content generated successfully using {data['model']}")
            return content
            
        except Exception as e:
            logging.error(f"Content generation failed: {e}")
            raise

class CloudGoogleServices:
    """Cloud-compatible Google services handler"""
    
    def __init__(self):
        self.credentials = self._get_credentials()
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
    
    def _get_credentials(self):
        """Get Google credentials from service account file"""
        try:
            if os.path.exists(GOOGLE_CREDENTIALS_PATH):
                credentials = service_account.Credentials.from_service_account_file(
                    GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
                )
                logging.info("Using service account credentials")
                return credentials
            else:
                raise FileNotFoundError(f"Credentials file not found: {GOOGLE_CREDENTIALS_PATH}")
        except Exception as e:
            logging.error(f"Failed to load credentials: {e}")
            raise
    
    def create_google_doc(self, title, content):
        """Create a new Google Doc with content"""
        try:
            # Create document
            doc = {
                'title': title
            }
            
            doc = self.docs_service.documents().create(body=doc).execute()
            doc_id = doc.get('documentId')
            
            logging.info(f"Created Google Doc with ID: {doc_id}")
            
            # Insert content
            requests_body = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': content
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests_body}
            ).execute()
            
            logging.info("Content inserted into Google Doc")
            return doc_id
            
        except Exception as e:
            logging.error(f"Failed to create Google Doc: {e}")
            raise
    
    def move_to_drive_folder(self, doc_id, folder_id):
        """Move document to specified Google Drive folder"""
        try:
            if not folder_id or folder_id == 'your_folder_id_here':
                logging.warning("No valid folder ID provided, document will remain in root")
                return
            
            # Get current parents
            file = self.drive_service.files().get(fileId=doc_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            
            # Move to new folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            
            logging.info(f"Moved document {doc_id} to folder {folder_id}")
            
        except Exception as e:
            logging.error(f"Failed to move document to folder: {e}")
            # Don't raise - document creation was successful

def main():
    """Main function for cloud execution"""
    logging.info("🚀 Starting AI Content Automation (Cloud Mode)")
    
    try:
        # Validate environment variables
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        # Initialize services
        generator = CloudContentGenerator()
        google_services = CloudGoogleServices()
        
        # Generate content
        topic = generator.get_random_topic()
        content = generator.generate_content(topic)
        logging.info(f"Generated content for topic: {topic}")
        
        # Create Google Doc
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        doc_title = f"{today} - {topic}"
        doc_id = google_services.create_google_doc(doc_title, content)
        
        # Move to Drive folder
        if GOOGLE_DRIVE_FOLDER_ID:
            google_services.move_to_drive_folder(doc_id, GOOGLE_DRIVE_FOLDER_ID)
            logging.info(f"Document moved to folder: {GOOGLE_DRIVE_FOLDER_ID}")
        
        logging.info("✅ Content automation completed successfully!")
        logging.info(f"📄 Document URL: https://docs.google.com/document/d/{doc_id}/edit")
        
    except Exception as e:
        logging.error(f"❌ Content automation failed: {e}")
        raise

if __name__ == "__main__":
    main()
