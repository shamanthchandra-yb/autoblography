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
- **Configurable Prompts**: Customize AI behavior for different content types and audiences

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

#### Generate Blog from Slack Thread

```bash
python -m autoblography --source slack --input "https://company.slack.com/archives/C1234567/p1234567890123456"
```

#### Generate Blog from Google Doc

```bash
python -m autoblography --source gdoc --input "https://docs.google.com/document/d/1ABC123XYZ/edit"
```

#### Specify Output Filename

```bash
python -m autoblography --source slack --input "https://..." --output "my_blog_post.docx"
```

## 📁 Project Structure

```
autoblography/
├── src/autoblography/
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
| `VERTEX_AI_MODEL` | No | AI model to use | `gemini-1.5-flash` |
| `KAPA_API_KEY` | No | Kapa AI API key | - |
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

### Slack Thread Processing

1. **Fetch Messages**: Retrieve all messages from the specified Slack thread
2. **Clean Content**: Remove sensitive information and anonymize participants
3. **Generate Ideas**: AI analyzes the conversation to create blog post ideas
4. **Find References**: Search for relevant existing documentation and blogs
5. **Create Content**: Generate structured blog post with proper formatting
6. **Add Images**: Create technical diagrams and illustrations
7. **Export**: Save as Word document with full formatting

### Google Docs Processing

1. **Read Document**: Extract text, images, and comments from Google Doc
2. **Enrich Context**: Follow links and gather additional content
3. **Generate Ideas**: AI analyzes the document to create blog post ideas
4. **Find References**: Search for relevant existing documentation and blogs
5. **Create Content**: Generate structured blog post with proper formatting
6. **Add Images**: Create technical diagrams and illustrations
7. **Export**: Save as Word document with full formatting

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

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/autoblography/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autoblography/discussions)
- **Email**: your.email@example.com

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

---

**Made with ❤️ for the developer community** 