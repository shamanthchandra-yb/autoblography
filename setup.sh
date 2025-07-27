#!/bin/bash

# Simple AutoBlography Setup Script
# This script sets up the basic file structure

echo "🔧 AutoBlography Setup"
echo "======================"

# Create directories
echo "📁 Creating directories..."
mkdir -p credentials output images

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env with your actual credentials"
else
    echo "✅ .env already exists"
fi

# Check if credentials exist
if [ ! -f credentials/google-credentials.json ]; then
    echo "⚠️  Google credentials not found"
    echo "📋 Please place your Google service account JSON key in:"
    echo "   credentials/google-credentials.json"
    echo ""
    echo "💡 If you have an existing key, you can copy it:"
    echo "   cp your-service-account-key.json credentials/google-credentials.json"
else
    echo "✅ Google credentials found"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Ensure credentials/google-credentials.json exists"
echo "3. Run: ./deploy.sh" 