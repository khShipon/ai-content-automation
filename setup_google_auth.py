#!/usr/bin/env python3
"""
Google Authentication Setup Script
This script helps you complete the one-time Google authentication process
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

def authenticate_google_services():
    """Complete Google authentication for both Docs and Drive services"""
    print("🔐 Starting Google Authentication Setup...")
    print("=" * 60)
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        print("Please make sure your Google Cloud credentials file is in the project directory.")
        return False
    
    try:
        print("📋 Setting up authentication for Google Docs and Drive...")
        print("🌐 This will open a browser window for authentication.")
        print("📝 Please follow these steps:")
        print("   1. A browser window will open")
        print("   2. Sign in to your Google account")
        print("   3. Grant permissions for Google Docs and Drive access")
        print("   4. The browser will show 'The authentication flow has completed'")
        print("   5. Return to this terminal")
        print()
        input("Press Enter when you're ready to continue...")
        
        # Create the flow using the client secrets file
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        # Run the OAuth flow with specific port
        print("🚀 Opening browser for authentication...")
        try:
            # Try port 8080 first
            creds = flow.run_local_server(port=8080, open_browser=True)
        except OSError:
            try:
                # If 8080 is busy, try 8081
                print("Port 8080 busy, trying 8081...")
                creds = flow.run_local_server(port=8081, open_browser=True)
            except OSError:
                # If both ports are busy, use manual flow
                print("Ports busy, using manual authentication...")
                creds = flow.run_console()
        
        # Save credentials for both services
        print("💾 Saving authentication tokens...")
        
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
        
        # Test Google Docs service
        docs_service = build('docs', 'v1', credentials=creds)
        print("✅ Google Docs service initialized successfully")
        
        # Test Google Drive service
        drive_service = build('drive', 'v3', credentials=creds)
        print("✅ Google Drive service initialized successfully")
        
        print("\n🎉 Google Authentication Setup Complete!")
        print("=" * 60)
        print("✅ Your AI Content Automation Agent is now fully configured!")
        print("🚀 You can now run 'python main.py' to start automatic content generation and upload.")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure your credentials.json file is valid")
        print("2. Check your internet connection")
        print("3. Ensure your Google Cloud project has the required APIs enabled:")
        print("   - Google Docs API")
        print("   - Google Drive API")
        print("4. Try running the script again")
        return False

def check_existing_auth():
    """Check if authentication tokens already exist"""
    docs_exists = os.path.exists(DOCS_TOKEN_FILE)
    drive_exists = os.path.exists(DRIVE_TOKEN_FILE)
    
    if docs_exists and drive_exists:
        print("✅ Authentication tokens found!")
        print(f"   - Google Docs: {DOCS_TOKEN_FILE}")
        print(f"   - Google Drive: {DRIVE_TOKEN_FILE}")
        
        # Test if tokens are still valid
        try:
            with open(DOCS_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            
            if creds and creds.valid:
                print("✅ Existing tokens are valid!")
                print("🚀 Your authentication is already set up. You can run 'python main.py'")
                return True
            elif creds and creds.expired and creds.refresh_token:
                print("🔄 Tokens expired, attempting to refresh...")
                creds.refresh(Request())
                
                # Save refreshed tokens
                with open(DOCS_TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                with open(DRIVE_TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                
                print("✅ Tokens refreshed successfully!")
                return True
            else:
                print("⚠️ Tokens are invalid, need to re-authenticate")
                return False
                
        except Exception as e:
            print(f"⚠️ Error checking existing tokens: {e}")
            return False
    else:
        print("ℹ️ No existing authentication tokens found.")
        return False

def main():
    """Main authentication setup function"""
    print("🚀 Google Authentication Setup for AI Content Automation Agent")
    print("=" * 70)
    
    # Check for existing authentication
    if check_existing_auth():
        print("\n🎉 Authentication is already complete!")
        return 0
    
    print("\n🔐 Starting new authentication process...")
    
    # Perform authentication
    if authenticate_google_services():
        print("\n✅ Setup completed successfully!")
        print("🎯 Next steps:")
        print("   1. Run 'python main.py' to test the full workflow")
        print("   2. Set up automation using Task Scheduler or cron")
        print("   3. Monitor the logs for any issues")
        return 0
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        return 1

if __name__ == "__main__":
    exit(main())
