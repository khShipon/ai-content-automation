#!/usr/bin/env python3
"""
Helper script to create Google Cloud Service Account for GitHub Actions
This script helps you create the necessary service account credentials
"""

import json
import os

def create_service_account_guide():
    """Guide for creating service account"""
    print("🔧 Google Cloud Service Account Setup Guide")
    print("=" * 60)
    print()
    
    print("📋 Step-by-Step Instructions:")
    print()
    
    print("1. 🌐 Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    print()
    
    print("2. 📁 Select your project (or create a new one)")
    print("   - Project name: 'AI Content Automation'")
    print()
    
    print("3. 🔑 Navigate to IAM & Admin → Service Accounts:")
    print("   https://console.cloud.google.com/iam-admin/serviceaccounts")
    print()
    
    print("4. ➕ Click 'CREATE SERVICE ACCOUNT'")
    print("   - Service account name: 'github-actions-automation'")
    print("   - Service account ID: 'github-actions-automation'")
    print("   - Description: 'Service account for GitHub Actions automation'")
    print("   - Click 'CREATE AND CONTINUE'")
    print()
    
    print("5. 🔐 Grant permissions:")
    print("   Add these roles:")
    print("   - Google Drive API")
    print("   - Google Docs API")
    print("   - Or use 'Editor' role for simplicity")
    print("   - Click 'CONTINUE'")
    print()
    
    print("6. 🔑 Create and download key:")
    print("   - Click 'CREATE KEY'")
    print("   - Select 'JSON' format")
    print("   - Click 'CREATE'")
    print("   - Save the downloaded JSON file securely")
    print()
    
    print("7. 🚀 Enable required APIs:")
    print("   Go to APIs & Services → Library and enable:")
    print("   - Google Docs API")
    print("   - Google Drive API")
    print()
    
    print("✅ After downloading the JSON file, use it as GOOGLE_CREDENTIALS secret in GitHub!")
    print()

def validate_service_account_json():
    """Validate service account JSON format"""
    print("🔍 Service Account JSON Validator")
    print("=" * 40)
    
    file_path = input("📁 Enter path to your service account JSON file: ").strip()
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return False
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        required_fields = [
            'type', 'project_id', 'private_key_id', 'private_key',
            'client_email', 'client_id', 'auth_uri', 'token_uri'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        if data.get('type') != 'service_account':
            print("❌ Invalid type. Must be 'service_account'")
            return False
        
        print("✅ Service account JSON is valid!")
        print(f"📧 Service account email: {data['client_email']}")
        print(f"🆔 Project ID: {data['project_id']}")
        
        print("\n📋 Copy this JSON content to GitHub Secrets as 'GOOGLE_CREDENTIALS':")
        print("-" * 60)
        print(json.dumps(data, indent=2))
        print("-" * 60)
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Google Cloud Service Account Helper")
    print("=" * 50)
    print()
    
    while True:
        print("Choose an option:")
        print("1. 📖 Show service account creation guide")
        print("2. 🔍 Validate service account JSON file")
        print("3. 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            create_service_account_guide()
        elif choice == '2':
            validate_service_account_json()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
