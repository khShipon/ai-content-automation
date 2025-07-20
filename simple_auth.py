#!/usr/bin/env python3
"""
Simple Google Authentication that works with Desktop applications
"""

import os
import logging
import pickle
import webbrowser
from urllib.parse import urlparse, parse_qs
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

def simple_authentication():
    """Simple authentication method for desktop apps"""
    print("🔐 Simple Google Authentication")
    print("=" * 50)
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        return False
    
    try:
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        print("📋 Manual Authentication Steps:")
        print("1. I'll generate an authorization URL")
        print("2. Copy the URL and open it in your browser")
        print("3. Complete the Google sign-in and authorization")
        print("4. You'll be redirected to a page that may show an error")
        print("5. Copy the ENTIRE URL from your browser's address bar")
        print("6. Paste it back here")
        print()
        
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            prompt='consent',
            access_type='offline',
            include_granted_scopes='true'
        )
        
        print("🔗 STEP 1: Copy this URL and open it in your browser:")
        print("-" * 60)
        print(auth_url)
        print("-" * 60)
        print()
        
        # Try to open browser automatically
        try:
            webbrowser.open(auth_url)
            print("✅ Browser opened automatically")
        except:
            print("⚠️ Could not open browser automatically - please copy the URL manually")
        
        print()
        print("🔗 STEP 2: After completing authorization in the browser:")
        print("   - You might see an error page or 'localhost refused to connect'")
        print("   - That's OK! Just copy the ENTIRE URL from your browser's address bar")
        print("   - The URL should start with 'http://localhost' and contain 'code='")
        print()
        
        # Get the redirect URL from user
        redirect_url = input("📋 Paste the complete redirect URL here: ").strip()
        
        if not redirect_url:
            print("❌ No URL provided")
            return False
        
        # Extract authorization code from URL
        try:
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'code' not in query_params:
                print("❌ No authorization code found in URL")
                print("Make sure you copied the complete URL that contains 'code='")
                return False
            
            auth_code = query_params['code'][0]
            print(f"✅ Authorization code extracted: {auth_code[:20]}...")
            
        except Exception as e:
            print(f"❌ Error parsing URL: {e}")
            return False
        
        # Exchange code for credentials
        print("🔄 Exchanging authorization code for credentials...")
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        if not creds:
            print("❌ Failed to get credentials")
            return False
        
        print("✅ Credentials obtained successfully!")
        
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
        return False

def main():
    """Main function"""
    print("🚀 Simple Google Authentication Setup")
    print("=" * 50)
    
    # Check for existing tokens
    if os.path.exists(DOCS_TOKEN_FILE) and os.path.exists(DRIVE_TOKEN_FILE):
        try:
            with open(DOCS_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            
            if creds and creds.valid:
                print("✅ Valid authentication already exists!")
                print("🚀 You can run 'python main.py' directly!")
                return 0
        except:
            pass
    
    print("🔐 Setting up new authentication...")
    
    if simple_authentication():
        return 0
    else:
        print("\n❌ Authentication failed. Please try again.")
        return 1

if __name__ == "__main__":
    exit(main())
