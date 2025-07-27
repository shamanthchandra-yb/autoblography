# 🚀 Setup Guide for Autoblography

This guide will walk you through setting up Autoblography on your local machine.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git
- Internet connection for API calls

### Required Accounts & Services
1. **Google Cloud Platform Account**
   - Active billing account
   - Vertex AI API enabled
   - Google Docs API enabled

2. **Slack Workspace** (optional, for Slack integration)
   - Admin access to create Slack apps
   - Ability to install apps in your workspace

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shamanthchandra-yb/autoblography.git
cd autoblography
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Google Cloud Setup

#### 4.1 Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project ID

#### 4.2 Enable Required APIs
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Google Docs API
gcloud services enable docs.googleapis.com

# Enable Google Drive API (for document access)
gcloud services enable drive.googleapis.com
```

#### 4.3 Create Service Account
1. Go to IAM & Admin > Service Accounts
2. Click "Create Service Account"
3. Give it a name (e.g., "autoblography-service")
4. Grant the following roles:
   - Vertex AI User
   - Google Docs API User
   - Storage Object Viewer (if using Cloud Storage)

#### 4.4 Generate Service Account Key
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose JSON format
5. Download the key file
6. Save it securely (e.g., `~/.config/gcloud/service-account-key.json`)

### 5. Slack Setup (Optional)

#### 5.1 Create Slack App
1. Go to [Slack API](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Give your app a name and select workspace

#### 5.2 Configure OAuth & Permissions
1. Go to "OAuth & Permissions"
2. Add the following Bot Token Scopes:
   - `channels:history`
   - `channels:read`
   - `users:read`
   - `chat:write`

#### 5.3 Install App to Workspace
1. Click "Install to Workspace"
2. Copy the "Bot User OAuth Token"

### 6. Environment Configuration

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCLOUD_PROJECT=your-project-id

# Slack Configuration (optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

# Optional: Vertex AI Location
VERTEX_AI_LOCATION=us-central1
```

### 7. Test Installation

#### Test Google Cloud Connection
```bash
python -c "
from ai_hackathon_2025.google_document_reader import read_google_doc_multimodal
print('Google Cloud connection: OK')
"
```

#### Test Slack Connection (if configured)
```bash
python -c "
from ai_hackathon_2025.slack_app import SlackApp
app = SlackApp()
print('Slack connection: OK')
"
```

### 8. Run Your First Blog Generation

#### From Google Doc
```bash
python -m ai_hackathon_2025.main --source gdoc --input "https://docs.google.com/document/d/YOUR_DOC_ID"
```

#### From Slack Thread
```bash
python -m ai_hackathon_2025.main --source slack --input "https://your-workspace.slack.com/archives/CHANNEL/pTIMESTAMP"
```

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
Error: Could not automatically determine credentials
```
**Solution**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to valid service account key

#### 2. API Not Enabled
```
Error: The API is not enabled for project
```
**Solution**: Enable required APIs in Google Cloud Console

#### 3. Permission Denied
```
Error: Permission denied accessing document
```
**Solution**: Ensure service account has access to the Google Doc or make doc publicly readable

#### 4. Slack Token Issues
```
Error: Invalid token
```
**Solution**: Check that your Slack bot token is correct and has required permissions

### Getting Help

1. Check the [Issues](https://github.com/shamanthchandra-yb/autoblography/issues) page
2. Review the main [README.md](../README.md)
3. Ensure all prerequisites are met
4. Verify environment variables are set correctly

## Next Steps

Once setup is complete, you can:
- Generate your first blog post
- Customize the AI prompts in `prompt_constant.py`
- Explore the generated Word documents
- Integrate with your existing workflow

Happy blogging! 🎉