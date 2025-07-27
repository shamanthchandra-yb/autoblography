# AutoBlography 🤖📝

**AI-powered blog generation from Slack threads and Google Docs**

AutoBlography is an intelligent tool that transforms your internal technical discussions and documents into polished, publication-ready blog posts. It uses advanced AI to clean, structure, and enhance content while maintaining the technical accuracy and insights from your original sources.

## ✨ Features

- **Slack Thread Processing**: Convert technical Slack conversations into structured blog posts
- **Google Docs Integration**: Transform internal documents and design docs into public-facing content
- **AI-Powered Content Enhancement**: Clean sensitive information, anonymize participants, and generate compelling narratives
- **Automatic Image Generation**: Create technical diagrams and illustrations using AI
- **Smart Content Linking**: Find and link to relevant existing documentation and blogs
- **Multiple Output Formats**: Generate Word documents (.docx) with proper formatting
- **Real-time Progress Logging**: See exactly what's happening during blog generation
- **Web Service**: Simple HTTP API for integration with other tools
- **Multiple Usage Options**: CLI, web interface, and bash scripts for different workflows

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

2. **Install the package**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   export SLACK_TOKEN="xoxb-your-slack-token"
   export GOOGLE_PROJECT_ID="your-google-cloud-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   export KAPA_API_KEY="your-kapa-api-key"  # Optional
   ```

### Usage

#### Option 1: Simple CLI (Recommended)

```bash
# Generate blog with real-time progress logging
python cli_with_logs.py --url "https://company.slack.com/archives/C1234567/p1234567890123456" --source slack --output "my_blog.docx"

# Generate from Google Doc
python cli_with_logs.py --url "https://docs.google.com/document/d/1ABC123XYZ/edit" --source gdoc --output "my_blog.docx"
```

#### Option 2: Bash Script (Easiest)

```bash
# Make script executable (first time only)
chmod +x generate_blog.sh

# Generate blog with colored progress output
./generate_blog.sh "https://company.slack.com/archives/C1234567/p1234567890123456" slack my_blog.docx

# Generate from Google Doc
./generate_blog.sh "https://docs.google.com/document/d/1ABC123XYZ/edit" gdoc my_blog.docx
```

#### Option 3: Simple Curl with Live Progress (Recommended for sharing)

```bash
# Start the web service
python web_app.py

# Generate blog with real-time progress logging
curl -X POST http://localhost:8000/generate-blog-live \
  -F "url=https://company.slack.com/archives/C1234567/p1234567890123456" \
  -F "source_type=slack"
```

This shows real-time progress like:
- 🚀 Starting Slack blog generation pipeline...
- Fetching thread from Channel ID: C1234567...
- ✅ Successfully fetched 17 messages from the thread.
- 🤖 Processing Slack conversation...
- ✅ Cleaning Complete!
- And more...

**Alternative: Two-step process with download link:**
```bash
# Generate blog (returns JSON with download link)
curl -X POST http://localhost:8000/generate-blog-simple \
  -F "url=https://company.slack.com/archives/C1234567/p1234567890123456" \
  -F "source_type=slack"

# Download the file using the returned download URL
curl -X GET http://localhost:8000/download/YOUR_DOWNLOAD_ID --output my_blog.docx
```

**Or use the web interface at http://localhost:8000**

See [simple_curl_guide.md](simple_curl_guide.md) for complete examples and one-liners.

#### Option 4: Original CLI

```bash
# Basic CLI without progress logging
python -m autoblography --source slack --input "https://company.slack.com/archives/C1234567/p1234567890123456"
```

#### Option 5: Direct Download (Legacy)

```bash
# Direct download without progress info
curl -X POST http://localhost:8000/generate-blog \
  -F "url=https://company.slack.com/archives/C1234567/p1234567890123456" \
  -F "source_type=slack" \
  --output my_blog.docx
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

## 🔧 Development

### Setting up Development Environment

1. **Clone and install in development mode**
   ```bash
   git clone https://github.com/yourusername/autoblography.git
   cd autoblography
   pip install -e ".[dev]"
   ```

2. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

### Adding New Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following the existing code structure
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit pull request**

## 📝 How It Works

### Blog Generation Process

1. **Fetch Content**: Retrieve messages from Slack thread or content from Google Doc
2. **Clean & Process**: Remove sensitive information, anonymize participants, and structure content
3. **Generate Ideas**: AI analyzes the content to create blog post ideas and target audience
4. **Find References**: Search for relevant existing documentation and blogs using Kapa AI
5. **Create Content**: Generate structured blog post with proper formatting and sections
6. **Add Images**: Create technical diagrams and illustrations using AI image generation
7. **Export**: Save as Word document (.docx) with full formatting and embedded images

### Real-time Progress Tracking

All tools now provide real-time feedback showing:
- ✅ Environment validation
- 🔄 Content processing steps
- 🤖 AI model interactions
- 🎨 Image generation progress
- 📄 File creation and download status
- ❌ Error handling with clear messages

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Vertex AI** for powerful AI models
- **Slack API** for seamless integration
- **Google Docs API** for document processing
- **Kapa AI** for intelligent content discovery
- **Pandoc** for document conversion

## 🔧 Troubleshooting

### Common Issues

**"Address already in use" error:**
```bash
# Kill existing web service
pkill -f "python web_app.py"
# Then restart
python web_app.py
```

**"Command not found: python":**
```bash
# Use python3 instead
python3 web_app.py
# Or activate virtual environment
source venv/bin/activate && python web_app.py
```

**Environment validation fails:**
- Check all required environment variables are set
- Verify Google Cloud credentials are valid
- Ensure Slack token has proper permissions

**Blog generation fails:**
- Check URL format (must be valid Slack thread or Google Doc)
- Verify you have access to the content
- Check internet connection for AI model access

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/autoblography/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autoblography/discussions)
- **Email**: your.email@example.com

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

---

**Made with ❤️ for the developer community** 