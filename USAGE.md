# AutoBlography - Quick Usage Guide

## 🚀 Quick Start

### 1. Set Environment Variables
```bash
export SLACK_TOKEN="xoxb-your-slack-token"
export GOOGLE_PROJECT_ID="your-google-cloud-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
export KAPA_API_KEY="your-kapa-api-key"
```

### 2. Choose Your Method

#### **Easiest: Bash Script**
```bash
chmod +x generate_blog.sh
./generate_blog.sh "https://company.slack.com/archives/C1234567/p1234567890123456" slack my_blog.docx
```

#### **With Progress Logging: Python CLI**
```bash
python cli_with_logs.py --url "https://company.slack.com/archives/C1234567/p1234567890123456" --source slack --output my_blog.docx
```

#### **Web Service:**
```bash
python web_app.py
# Then visit http://localhost:8000 or use curl:
curl -X POST http://localhost:8000/generate-blog \
  -F "url=https://company.slack.com/archives/C1234567/p1234567890123456" \
  -F "source_type=slack" \
  --output my_blog.docx
```

## 📋 What You'll See

The tools show real-time progress:
- ✅ Environment validation
- 🔄 Processing content
- 🤖 AI generating blog
- 🎨 Creating images
- 📄 Saving file
- ✅ Complete!

## 🔧 Troubleshooting

**Web service won't start:**
```bash
pkill -f "python web_app.py"  # Kill existing process
python web_app.py             # Restart
```

**"python not found":**
```bash
python3 web_app.py            # Use python3
# Or activate virtual environment:
source venv/bin/activate && python web_app.py
```

## 📝 Examples

### Slack Thread
```bash
./generate_blog.sh "https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" slack blog.docx
```

### Google Doc
```bash
./generate_blog.sh "https://docs.google.com/document/d/1ABC123XYZ/edit" gdoc blog.docx
```

### With Custom Output
```bash
python cli_with_logs.py --url "https://..." --source slack --output "my_custom_name.docx"
```

## 🎯 Tips

- **URL Format**: Must be valid Slack thread or Google Doc URL
- **Permissions**: Ensure you have access to the content
- **Output**: Files are saved as .docx with embedded images
- **Progress**: All tools show real-time status updates
- **Errors**: Clear error messages help identify issues quickly

---

**Need help?** Check the main README.md for detailed documentation. 