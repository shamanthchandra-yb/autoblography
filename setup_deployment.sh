#!/bin/bash

# AutoBlography Deployment Setup Script
# This script helps set up the environment for deployment

set -e

echo "🚀 Setting up AutoBlography deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env with your actual credentials"
else
    echo "✅ .env file already exists"
fi

# Create credentials directory
if [ ! -d credentials ]; then
    echo "📁 Creating credentials directory..."
    mkdir -p credentials
else
    echo "✅ credentials directory already exists"
fi

# Check if Google credentials exist
if [ ! -f credentials/google-credentials.json ]; then
    echo "⚠️  Google credentials not found at credentials/google-credentials.json"
    echo "📋 Please place your Google service account JSON key in:"
    echo "   credentials/google-credentials.json"
    echo ""
    echo "💡 You can copy your existing key:"
    echo "   cp hackathon-2025-463220-58174c9d60ed.json credentials/google-credentials.json"
else
    echo "✅ Google credentials found"
fi

# Create output directories
echo "📁 Creating output directories..."
mkdir -p output images

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env with your actual credentials"
echo "2. Ensure credentials/google-credentials.json exists"
echo "3. Run: docker-compose up -d"
echo ""
echo "🔒 Security note: credentials/ directory is in .gitignore" 