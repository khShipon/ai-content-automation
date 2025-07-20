#!/usr/bin/env python3
"""
Web-based Google Authentication that works with the configured OAuth client
"""

import os
import logging
import pickle
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Scopes for both Google Docs and Drive
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

CREDENTIALS_FILE = 'credentials.json'
DOCS_TOKEN_FILE = 'token.pickle'
DRIVE_TOKEN_FILE = 'token_drive.pickle'

def check_credentials_file():
    """Check if credentials file exists and is valid"""
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        return False
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_data = json.load(f)
        
        # Check if it's a web application
        if 'web' in creds_data:
            print("✅ Web application credentials detected")
            redirect_uris = creds_data['web'].get('redirect_uris', [])
            print(f"✅ Configured redirect URIs: {redirect_uris}")
            return True
        elif 'installed' in creds_data:
            print("⚠️ Desktop application credentials detected")
            print("   This might cause redirect URI issues")
            return True
        else:
            print("❌ Invalid credentials file format")
            return False
            
    except Exception as e:
        print(f"❌ Error reading credentials file: {e}")
        return False

def web_authentication():
    """Web-based authentication using local server"""
    print("🔐 Web-based Google Authentication")
    print("=" * 50)
    
    if not check_credentials_file():
        return False
    
    try:
        # Create the flow with explicit redirect URI
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, 
            SCOPES,
            redirect_uri='http://localhost:8080/'
        )
        
        print("📋 Authentication Steps:")
        print("1. A local web server will start on port 8080")
        print("2. Your browser will open automatically")
        print("3. Complete the Google sign-in and authorization")
        print("4. You'll be redirected back to localhost")
        print("5. The authentication will complete automatically")
        print()
        print("🚀 Starting authentication server...")
        
        # Run the OAuth flow with local server
        creds = flow.run_local_server(
            port=8080,
            prompt='consent',
            authorization_prompt_message='Please visit this URL to authorize the application: {url}',
            success_message='Authentication successful! You can close this window.',
            open_browser=True
        )
        
        if not creds:
            print("❌ Authentication failed - no credentials received")
            return False
        
        print("✅ Authentication successful!")
        
        # Save credentials
        print("💾 Saving authentication tokens...")
        
        with open(DOCS_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Docs token saved")
        
        with open(DRIVE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Drive token saved")
        
        # Test services
        print("\n🧪 Testing Google Services...")
        
        try:
            docs_service = build('docs', 'v1', credentials=creds)
            print("✅ Google Docs service working")
            
            drive_service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive service working")
            
            print("\n🎉 Authentication Setup Complete!")
            print("=" * 50)
            print("✅ Your AI Content Automation Agent is now fully configured!")
            print("🚀 Run 'python main.py' to start creating and uploading content!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing services: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure port 8080 is not in use")
        print("2. Check your firewall settings")
        print("3. Ensure your OAuth client has the correct redirect URIs")
        return False

def check_existing_tokens():
    """Check if we already have valid tokens"""
    if os.path.exists(DOCS_TOKEN_FILE) and os.path.exists(DRIVE_TOKEN_FILE):
        try:
            with open(DOCS_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            
            if creds and creds.valid:
                print("✅ Valid authentication tokens already exist!")
                print("🚀 You can run 'python main.py' directly!")
                return True
            elif creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired tokens...")
                creds.refresh(Request())
                
                # Save refreshed tokens
                with open(DOCS_TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                with open(DRIVE_TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                
                print("✅ Tokens refreshed successfully!")
                return True
        except Exception as e:
            print(f"⚠️ Error checking tokens: {e}")
    
    return False

def main():
    """Main function"""
    print("🚀 Google Web Authentication Setup")
    print("=" * 50)
    
    # Check for existing valid tokens
    if check_existing_tokens():
        return 0
    
    print("\n🔐 Setting up new authentication...")
    
    if web_authentication():
        return 0
    else:
        print("\n❌ Authentication failed.")
        print("\n💡 Alternative: Try changing your OAuth client type to 'Desktop application'")
        print("   in Google Cloud Console if the web flow doesn't work.")
        return 1

if __name__ == "__main__":
    exit(main())
