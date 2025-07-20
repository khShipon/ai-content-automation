#!/usr/bin/env python3
"""
Console Authentication for Google Services
This method works without browser redirects
"""

import os
import logging
import pickle
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

def console_authentication():
    """Console authentication - no browser redirect needed"""
    print("🔐 Google Console Authentication")
    print("=" * 50)
    print("This method doesn't require browser redirects!")
    print()
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        return False
    
    try:
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        print("📋 Follow these steps:")
        print("1. A URL will be displayed below")
        print("2. Copy and paste the URL into your browser")
        print("3. Complete the Google authentication")
        print("4. Copy the authorization code from the browser")
        print("5. Paste the code back here when prompted")
        print()
        print("🚀 Starting authentication...")
        print()
        
        # Get authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent')

        print(f"🔗 Please visit this URL to authorize the application:")
        print(f"{auth_url}")
        print()
        print("📋 After authorization, you'll get an authorization code.")
        print("Copy and paste it below:")

        # Get authorization code from user
        auth_code = input("Enter authorization code: ").strip()

        if not auth_code:
            print("❌ No authorization code provided")
            return False

        # Exchange code for credentials
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        if not creds:
            print("❌ Authentication failed - no credentials received")
            return False
        
        print("\n💾 Saving authentication tokens...")
        
        # Save for Google Docs
        with open(DOCS_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Docs token saved to {DOCS_TOKEN_FILE}")
        
        # Save for Google Drive
        with open(DRIVE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Drive token saved to {DRIVE_TOKEN_FILE}")
        
        # Test the services
        print("\n🧪 Testing Google Services...")
        
        try:
            # Test Google Docs service
            docs_service = build('docs', 'v1', credentials=creds)
            print("✅ Google Docs service initialized successfully")
            
            # Test Google Drive service
            drive_service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive service initialized successfully")
            
            print("\n🎉 Authentication Setup Complete!")
            print("=" * 50)
            print("✅ Your AI Content Automation Agent is now fully configured!")
            print("🚀 You can now run 'python main.py' to start the full workflow!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing services: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you copied the URL correctly")
        print("2. Make sure you copied the authorization code correctly")
        print("3. Check your internet connection")
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
    print("🚀 Google Authentication for AI Content Automation Agent")
    print("=" * 60)
    
    # Check for existing valid tokens
    if check_existing_tokens():
        return 0
    
    print("\n🔐 Setting up new authentication...")
    
    if console_authentication():
        print("\n✅ Setup completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Run 'python main.py' to test the full workflow")
        print("   2. Your agent will now create Google Docs and upload to Drive!")
        return 0
    else:
        print("\n❌ Setup failed. Please try again.")
        return 1

if __name__ == "__main__":
    exit(main())
