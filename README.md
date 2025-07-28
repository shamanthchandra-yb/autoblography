# AutoBlography 🤖📝

**AI-powered blog generation from Slack threads and Google Docs**

AutoBlography transforms internal technical discussions and documents into polished, publication-ready blog posts using AI. It uses advanced AI to clean, structure, and enhance content while maintaining technical accuracy and insights.

## ✨ Features

- **Slack Thread Processing**: Convert technical Slack conversations into structured blog posts
- **Google Docs Integration**: Transform internal documents and design docs into public-facing content
- **AI-Powered Content Enhancement**: Clean sensitive information, anonymize participants, and generate compelling narratives
- **Automatic Image Generation**: Create technical diagrams and illustrations using AI
- **Smart Content Linking**: Find and link to relevant existing documentation and blogs
- **Multiple Output Formats**: Generate Word documents (.docx) with proper formatting
- **Real-time Progress Logging**: See exactly what's happening during blog generation
- **Web Service**: Simple HTTP API for integration with other tools

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Vertex AI enabled
- Slack API token (for Slack integration)
- Google Cloud service account credentials
- Kapa AI API key (optional, for finding relevant blogs)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autoblography.git
   cd autoblography
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export SLACK_TOKEN="xoxb-your-slack-token"
   export GOOGLE_PROJECT_ID="your-google-cloud-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   export KAPA_API_KEY="your-kapa-api-key"  # Optional
   ```

### Usage

#### Option 1: CLI with Logs (Recommended)

```bash
# Generate blog from Slack thread
python cli_with_logs.py --url "https://company.slack.com/archives/C1234567/p1234567890123456" --source slack

# Generate from Google Doc
python cli_with_logs.py --url "https://docs.google.com/document/d/1ABC123XYZ/edit" --source gdoc
```

#### Option 2: Web Service

```bash
# Start the web service
python web_app.py

# Then visit http://localhost:8000
# Or use curl:
curl -X POST http://localhost:8000/generate-blog \
  -F "url=https://company.slack.com/archives/C1234567/p1234567890123456" \
  -F "source_type=slack"
```

#### Option 3: Bash Script

```bash
# Make script executable (first time only)
chmod +x generate_blog.sh

# Generate blog with colored progress output
./generate_blog.sh "https://company.slack.com/archives/C1234567/p1234567890123456" slack my_blog.docx
```

#### Option 4: Package CLI

```bash
# Use the installed package
python -m autoblography --source slack --input "https://company.slack.com/archives/C1234567/p1234567890123456"
```

## 📁 Project Structure

```
autoblography/
├── src/autoblography/           # Main package
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # CLI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── blog_generator.py    # Main blog generation orchestrator
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── slack_integration.py # Slack API integration
│   │   └── google_docs_integration.py # Google Docs API integration
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── slack_processor.py   # Slack content processing
│   │   ├── gdoc_processor.py    # Google Docs content processing
│   │   └── ai_processor.py      # AI utilities (Kapa AI, etc.)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py        # File operations
│   │   └── image_utils.py       # Image generation utilities
│   └── config/
│       ├── __init__.py
│       ├── settings.py          # Application settings
│       └── prompts.py           # AI prompt templates
├── cli_with_logs.py             # CLI tool with real-time logging
├── generate_blog.sh             # Bash script for easy blog generation
├── web_app.py                   # FastAPI web service
├── templates/                   # Web interface templates
├── tests/                       # Test suite
├── docs/                        # Documentation
├── examples/                    # Usage examples
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
└── README.md                    # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `SLACK_TOKEN` | Yes | Slack API token | - |
| `GOOGLE_PROJECT_ID` | Yes | Google Cloud project ID | - |
| `GOOGLE_LOCATION` | No | Google Cloud location | `us-central1` |
| `VERTEX_AI_MODEL` | No | AI model to use | `gemini-2.0-flash-001` |
| `KAPA_API_KEY` | Yes | Kapa AI API key for finding relevant blogs | - |
| `OUTPUT_DIR` | No | Output directory | `output` |
| `IMAGE_OUTPUT_DIR` | No | Image output directory | `images` |

### Google Cloud Setup

1. **Create a Google Cloud Project**
2. **Enable Vertex AI API**
3. **Create a Service Account** with the following roles:
   - Vertex AI User
   - Document AI API User
   - Cloud Storage Object Viewer
4. **Download the service account key** and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Slack Setup

1. **Create a Slack App** in your workspace
2. **Add the following OAuth scopes**:
   - `channels:history`
   - `groups:history`
   - `im:history`
   - `mpim:history`
3. **Install the app** to your workspace
4. **Copy the Bot User OAuth Token** and set it as `SLACK_TOKEN`

## 🔧 How It Works

### Blog Generation Process

1. **Fetch Content**: Retrieve messages from Slack thread or content from Google Doc
2. **Clean & Process**: Remove sensitive information, anonymize participants, and structure content
3. **Generate Ideas**: AI analyzes the content to create blog post ideas and target audience
4. **Find References**: Search for relevant existing documentation and blogs using Kapa AI
5. **Create Content**: Generate structured blog post with proper formatting and sections
6. **Add Images**: Create technical diagrams and illustrations using AI image generation
7. **Export**: Save as Word document (.docx) with full formatting and embedded images

### Real-time Progress Tracking

All tools provide real-time feedback showing:
- ✅ Environment validation
- 🔄 Content processing steps
- 🤖 AI model interactions
- 🎨 Image generation progress
- 📄 File creation and download status
- ❌ Error handling with clear messages

## 🔧 Development

### Setting up Development Environment

1. **Clone and install in development mode**
   ```bash
   git clone https://github.com/yourusername/autoblography.git
   cd autoblography
   pip install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   pytest tests/
   ```
---

**Built for AI Hackathon 2025** 🚀 