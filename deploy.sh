#!/bin/bash

# Simple AutoBlography Deployment Script
# This script sets up and deploys AutoBlography using Docker

set -e

echo "🚀 AutoBlography Deployment"
echo "============================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check if file exists
check_file() {
    if [ ! -f "$1" ]; then
        echo -e "${RED}❌ Missing: $1${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Found: $1${NC}"
        return 0
    fi
}

# Check prerequisites
echo "📋 Checking prerequisites..."
missing_files=()

check_file ".env" || missing_files+=(".env")
check_file "credentials/google-credentials.json" || missing_files+=("credentials/google-credentials.json")

if [ ${#missing_files[@]} -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Missing required files:${NC}"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "💡 Quick setup:"
    echo "  1. Copy env_example.txt to .env and edit with your credentials"
    echo "  2. Place your Google service account key in credentials/google-credentials.json"
    echo "  3. Run this script again"
    exit 1
fi

echo ""
echo "🔧 Building and starting containers..."
docker-compose down || true
docker-compose build --no-cache
docker-compose up -d

echo ""
echo "⏳ Waiting for service to start..."
sleep 10

# Check if service is healthy
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}🎉 AutoBlography is now running!${NC}"
    echo ""
    echo "🌐 Service URL: http://localhost:8000"
    echo "🔍 Health Check: http://localhost:8000/health"
    echo ""
    echo "📝 Test with:"
    echo "  curl -X POST http://localhost:8000/generate-blog \\"
    echo "    -F \"url=https://yugabyte.slack.com/archives/CAR5BCH29/p1745351641318829\" \\"
    echo "    -F \"source_type=slack\""
    echo ""
    echo "📊 View logs: docker-compose logs -f"
else
    echo -e "${RED}❌ Service failed to start${NC}"
    echo "📊 Checking logs..."
    docker-compose logs --tail=20
    exit 1
fi 