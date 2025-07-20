# 🚀 GitHub Actions Setup Guide - FREE Cloud Automation

This guide will help you set up your AI Content Automation Agent to run automatically on GitHub Actions **completely FREE**!

## 📋 Prerequisites

1. ✅ GitHub account (free)
2. ✅ Your AI agent code (already done!)
3. ✅ Google Cloud service account credentials
4. ✅ OpenRouter API key

## 🛠️ Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New Repository"**
3. **Repository name**: `ai-content-automation`
4. **Set to Public** (required for free GitHub Actions)
5. **Click "Create repository"**

### Step 2: Upload Your Code

1. **Upload all your files** to the GitHub repository:
   ```
   - main.py
   - cloud_main.py
   - content_generator.py
   - google_docs_uploader.py
   - google_drive_uploader.py
   - requirements.txt
   - topics.txt
   - .github/workflows/content-automation.yml
   ```

2. **DO NOT upload** these files (they contain secrets):
   ```
   - credentials.json
   - token.pickle
   - token_drive.pickle
   ```

### Step 3: Create Google Service Account

1. **Go to Google Cloud Console**
2. **Navigate to**: IAM & Admin → Service Accounts
3. **Click "Create Service Account"**
4. **Name**: `github-actions-automation`
5. **Grant roles**:
   - Google Drive API
   - Google Docs API
6. **Create and download JSON key**

### Step 4: Set Up GitHub Secrets

1. **In your GitHub repository**, go to: Settings → Secrets and variables → Actions
2. **Click "New repository secret"** and add these secrets:

#### Secret 1: GOOGLE_CREDENTIALS
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "github-actions-automation@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

#### Secret 2: OPENROUTER_API_KEY
```
your_openrouter_api_key_here
```

#### Secret 3: GOOGLE_DRIVE_FOLDER_ID
```
your_google_drive_folder_id_here
```

### Step 5: Configure Schedule

Edit `.github/workflows/content-automation.yml` to set your preferred schedule:

```yaml
schedule:
  # Choose one of these options:
  - cron: '0 */6 * * *'     # Every 6 hours (4 times/day)
  - cron: '0 9 * * *'       # Daily at 9 AM UTC
  - cron: '0 9 * * 1,3,5'   # Mon, Wed, Fri at 9 AM UTC
  - cron: '0 9,15 * * *'    # Twice daily at 9 AM and 3 PM UTC
```

### Step 6: Test the Setup

1. **Go to Actions tab** in your GitHub repository
2. **Click "AI Content Automation"**
3. **Click "Run workflow"** to test manually
4. **Check the logs** to ensure everything works

## 📊 Usage Limits (FREE Tier)

- ✅ **2,000 minutes/month FREE**
- ✅ **Each run takes ~2-3 minutes**
- ✅ **~400-600 runs per month possible**
- ✅ **Perfect for daily/hourly automation**

## 🔧 Customization Options

### Change Content Topics
Edit the `TOPICS` list in `cloud_main.py`:
```python
TOPICS = [
    "Your Custom Topic 1",
    "Your Custom Topic 2",
    # Add more topics...
]
```

### Modify Schedule
Update the cron expression in `.github/workflows/content-automation.yml`

### Add More Features
- Email notifications on success/failure
- Multiple language support
- Content calendar integration
- Social media posting

## 🚨 Important Notes

1. **Repository must be PUBLIC** for free GitHub Actions
2. **Never commit credentials** to the repository
3. **Use GitHub Secrets** for all sensitive data
4. **Monitor your usage** in the Actions tab

## 🎉 Benefits

- ✅ **100% FREE** (no credit card needed)
- ✅ **Automatic scheduling** with cron jobs
- ✅ **Reliable cloud infrastructure**
- ✅ **Easy monitoring** through GitHub interface
- ✅ **Version control** for your automation code
- ✅ **Manual triggers** when needed

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Expression Generator](https://crontab.guru/)
- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)

---

**🚀 Once set up, your AI agent will run automatically in the cloud, generating and uploading content to Google Docs on your schedule - completely FREE!**
