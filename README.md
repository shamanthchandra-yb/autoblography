# 📝 Autoblography - AI-Powered Blog Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Hackathon-2025-orange.svg)](.)

> Transform your Slack conversations and Google Documents into professional blog posts with AI-powered content generation, image creation, and structured formatting.

## 🌟 Features

- **📱 Slack Integration**: Convert Slack thread conversations into structured blog posts
- **📄 Google Docs Support**: Transform Google Documents into engaging blog content
- **🤖 AI-Powered Content**: Leverage Google's Vertex AI (Gemini) for intelligent content generation
- **🎨 Image Generation**: Automatic image creation using Google's Imagen model
- **📊 Diagram Support**: Generate Mermaid diagrams and convert them to images
- **🔗 Link Enrichment**: Automatically fetch and incorporate content from referenced links
- **📝 Word Export**: Generate professional Word documents (.docx) from your content
- **🧠 Smart Context**: Integration with Kapa AI for relevant documentation and existing content

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Slack Thread  │    │  Google Docs    │
│   Conversations │    │   Documents     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────────┐
          │   Content Processor │
          │   & AI Enhancer     │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │   Blog Generator    │
          │   + Image Creation  │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │   Word Document     │
          │      Output         │
          └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Vertex AI enabled
- Slack Bot Token (for Slack integration)
- Google Docs API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autoblography
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   export SLACK_BOT_TOKEN="your-slack-bot-token"
   export GCLOUD_PROJECT="your-google-cloud-project-id"
   ```

### Usage

#### Generate blog from Slack thread:
```bash
python -m ai_hackathon_2025.main --source slack --input "https://your-slack-thread-url"
```

#### Generate blog from Google Doc:
```bash
python -m ai_hackathon_2025.main --source gdoc --input "https://docs.google.com/document/d/your-doc-id"
```

## 📁 Project Structure

```
autoblography/
├── ai_hackathon_2025/
│   ├── __init__.py
│   ├── main.py                      # Main entry point and CLI
│   ├── generate_and_save_blog.py    # Core blog generation logic
│   ├── slack_app.py                 # Slack API integration
│   ├── google_document_reader.py    # Google Docs API integration
│   ├── process_slack_thread.py      # Slack thread processing
│   ├── image_generation.py          # AI image generation
│   ├── ask_ai.py                    # Kapa AI integration
│   └── prompt_constant.py           # AI prompts and templates
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── .gitignore                      # Git ignore rules
```

## 🔧 Core Components

### 1. **Content Sources**
- **Slack Threads**: Extracts and processes conversation threads
- **Google Documents**: Reads documents with multimodal content (text, images, comments)

### 2. **AI Processing Pipeline**
- **Content Cleaning**: Removes noise and formats raw content
- **Context Enrichment**: Fetches additional content from embedded links
- **AI Enhancement**: Uses Vertex AI to generate structured, engaging blog content
- **Image Generation**: Creates relevant images using Google's Imagen model

### 3. **Output Generation**
- **Markdown Processing**: Structures content in markdown format
- **Word Document Export**: Converts to professional .docx format
- **Asset Integration**: Embeds generated images and diagrams

## 🤖 AI Models Used

- **Gemini 2.5 Pro**: Primary language model for content generation
- **Imagen 4.0**: Image generation from text prompts
- **Vertex AI**: Google Cloud's AI platform for model hosting

## 📋 Configuration

### Environment Variables
```bash
# Required
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GCLOUD_PROJECT=your-project-id

# Optional
SLACK_BOT_TOKEN=your-slack-token  # Required for Slack integration
```

### Google Cloud Setup
1. Enable Vertex AI API
2. Enable Google Docs API
3. Create a service account with appropriate permissions
4. Download the service account key JSON file

## 🎯 Use Cases

- **Team Knowledge Sharing**: Convert internal discussions into shareable blog posts
- **Documentation Creation**: Transform meeting notes and documents into structured content
- **Content Marketing**: Generate blog posts from brainstorming sessions
- **Technical Writing**: Create tutorials from Slack conversations or Google Docs

## 🔮 Features in Development

- [ ] Multiple output formats (HTML, PDF)
- [ ] Custom styling and themes
- [ ] Batch processing capabilities
- [ ] Web interface
- [ ] Integration with more platforms (Discord, Teams)
- [ ] Advanced image customization options

## 🤝 Contributing

This project was created during a hackathon. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Cloud Platform for Vertex AI services
- Slack API for conversation access
- The open-source community for excellent libraries
- Hackathon organizers and fellow participants

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the example usage in the code

---

**Built with ❤️ during AI Hackathon 2025**