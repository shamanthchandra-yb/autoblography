#!/bin/bash

# Autoblography Development Setup Script
# This script sets up the development environment for Autoblography

set -e  # Exit on any error

echo "🚀 Setting up Autoblography development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "📥 Installing development dependencies..."
pip install -e .

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p docs
mkdir -p examples
mkdir -p generated_images
mkdir -p generated_blogs
mkdir -p temp

# Check for environment file
if [ ! -f ".env" ]; then
    echo "⚠️ Creating .env template file..."
    cat > .env << EOF
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCLOUD_PROJECT=your-project-id

# Slack Configuration (optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

# Optional: Vertex AI Location
VERTEX_AI_LOCATION=us-central1
EOF
    echo "📝 Please edit .env file with your actual configuration"
else
    echo "✅ .env file already exists"
fi

# Test installation
echo "🧪 Testing installation..."
python -c "import ai_hackathon_2025; print('✅ Package import successful')"

echo ""
echo "🎉 Setup complete! Next steps:"
echo "1. Edit the .env file with your Google Cloud and Slack credentials"
echo "2. Run: source venv/bin/activate (to activate the environment)"
echo "3. Test with: python -m ai_hackathon_2025.main --help"
echo ""
echo "📚 Check out docs/SETUP.md for detailed setup instructions"
echo "📋 See examples/EXAMPLES.md for usage examples"
echo ""
echo "Happy blogging! 🎉"