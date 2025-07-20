#!/usr/bin/env python3
"""
Manual Google Authentication Setup
This script provides manual authentication when localhost doesn't work
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

def manual_authentication():
    """Manual authentication process when localhost doesn't work"""
    print("🔐 Manual Google Authentication Setup")
    print("=" * 50)
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        return False
    
    try:
        print("📋 Setting up manual authentication...")
        print("\n🔧 IMPORTANT: First, update your Google Cloud settings:")
        print("1. Go to: https://console.cloud.google.com")
        print("2. Select your project: english-with-shipon-9tjj3")
        print("3. Go to 'APIs & Services' → 'Credentials'")
        print("4. Click on your OAuth 2.0 Client ID")
        print("5. In 'Authorized redirect URIs', add these URIs:")
        print("   - http://localhost:8080/")
        print("   - http://localhost:8081/")
        print("   - http://127.0.0.1:8080/")
        print("   - http://127.0.0.1:8081/")
        print("6. Click 'Save'")
        print("7. Wait 5-10 minutes for changes to take effect")
        print()
        
        response = input("Have you updated the redirect URIs? (y/n): ").lower()
        if response != 'y':
            print("Please update the redirect URIs first, then run this script again.")
            return False
        
        print("\n🚀 Starting authentication...")
        
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        # Try different methods
        methods = [
            ("Port 8080", lambda: flow.run_local_server(port=8080, open_browser=True)),
            ("Port 8081", lambda: flow.run_local_server(port=8081, open_browser=True)),
            ("Console mode", lambda: flow.run_console())
        ]
        
        creds = None
        for method_name, method_func in methods:
            try:
                print(f"🔄 Trying {method_name}...")
                creds = method_func()
                print(f"✅ {method_name} successful!")
                break
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
                continue
        
        if not creds:
            print("❌ All authentication methods failed.")
            return False
        
        # Save credentials
        print("💾 Saving authentication tokens...")
        
        with open(DOCS_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Docs token saved")
        
        with open(DRIVE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ Google Drive token saved")
        
        # Test services
        print("\n🧪 Testing services...")
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        print("✅ Both services initialized successfully!")
        
        print("\n🎉 Authentication setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def console_authentication():
    """Console-only authentication (no browser)"""
    print("🔐 Console Authentication (No Browser Required)")
    print("=" * 50)
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        print("📋 Manual authentication steps:")
        print("1. Copy the URL that will be displayed")
        print("2. Open it in your browser")
        print("3. Complete the authentication")
        print("4. Copy the authorization code")
        print("5. Paste it back here")
        print()
        
        creds = flow.run_console()
        
        # Save credentials
        with open(DOCS_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        with open(DRIVE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print("✅ Console authentication successful!")
        return True
        
    except Exception as e:
        print(f"❌ Console authentication failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Google Authentication Troubleshooter")
    print("=" * 50)
    
    print("Choose authentication method:")
    print("1. Manual setup (update redirect URIs first)")
    print("2. Console authentication (no browser redirect)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        return 0 if manual_authentication() else 1
    elif choice == "2":
        return 0 if console_authentication() else 1
    elif choice == "3":
        print("Exiting...")
        return 0
    else:
        print("Invalid choice. Please run the script again.")
        return 1

if __name__ == "__main__":
    exit(main())
