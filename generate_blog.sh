#!/bin/bash

# AutoBlography Blog Generator with Real-time Logging
# Usage: ./generate_blog.sh <url> <source_type> [output_filename]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%H:%M:%S')
    
    case $level in
        "INFO")
            echo -e "[${timestamp}] ${BLUE}ℹ️${NC} $message"
            ;;
        "SUCCESS")
            echo -e "[${timestamp}] ${GREEN}✅${NC} $message"
            ;;
        "ERROR")
            echo -e "[${timestamp}] ${RED}❌${NC} $message"
            ;;
        "WARNING")
            echo -e "[${timestamp}] ${YELLOW}⚠️${NC} $message"
            ;;
        "PROGRESS")
            echo -e "[${timestamp}] ${BLUE}🔄${NC} $message"
            ;;
    esac
}

# Check if required arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <url> <source_type> [output_filename]"
    echo "  url: Slack thread or Google Doc URL"
    echo "  source_type: slack or gdoc"
    echo "  output_filename: Optional output filename (default: blog_$(date +%Y%m%d_%H%M%S).docx)"
    exit 1
fi

URL=$1
SOURCE_TYPE=$2
OUTPUT_FILE=${3:-"blog_$(date +%Y%m%d_%H%M%S).docx"}

# Validate source type
if [ "$SOURCE_TYPE" != "slack" ] && [ "$SOURCE_TYPE" != "gdoc" ]; then
    print_status "ERROR" "Invalid source type. Must be 'slack' or 'gdoc'"
    exit 1
fi

# Validate URL format
if [ "$SOURCE_TYPE" = "slack" ] && [[ ! "$URL" =~ slack\.com ]]; then
    print_status "ERROR" "Invalid Slack URL format"
    exit 1
elif [ "$SOURCE_TYPE" = "gdoc" ] && [[ ! "$URL" =~ docs\.google\.com ]]; then
    print_status "ERROR" "Invalid Google Doc URL format"
    exit 1
fi

print_status "INFO" "Starting AutoBlography blog generation"
print_status "INFO" "URL: $URL"
print_status "INFO" "Source Type: $SOURCE_TYPE"
print_status "INFO" "Output File: $OUTPUT_FILE"

# Check if web service is running
print_status "PROGRESS" "Checking web service availability..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    print_status "ERROR" "Web service is not running. Please start it with: python web_app.py"
    exit 1
fi
print_status "SUCCESS" "Web service is available"

# Generate blog with real-time logging
print_status "PROGRESS" "Starting blog generation..."

# Use the logging endpoint to get real-time updates
curl -X POST http://localhost:8000/generate-blog-with-logs \
    -F "url=$URL" \
    -F "source_type=$SOURCE_TYPE" \
    --no-buffer \
    | while IFS= read -r line; do
        if [[ $line == data:* ]]; then
            # Extract the message from the data: prefix
            message="${line#data: }"
            echo -e "[$(date '+%H:%M:%S')] ${BLUE}📝${NC} $message"
            
            # Check for completion
            if [[ $message == SUCCESS:* ]]; then
                print_status "SUCCESS" "Blog generation completed!"
                
                # Extract filename and download
                filename=$(echo "$message" | grep -o 'File: [^[:space:]]*' | cut -d' ' -f2)
                if [ -n "$filename" ]; then
                    print_status "PROGRESS" "Downloading file: $filename"
                    
                    # Download the file
                    curl -X POST http://localhost:8000/generate-blog \
                        -F "url=$URL" \
                        -F "source_type=$SOURCE_TYPE" \
                        --output "$OUTPUT_FILE" \
                        --silent
                    
                    if [ -f "$OUTPUT_FILE" ]; then
                        print_status "SUCCESS" "Blog saved to: $OUTPUT_FILE"
                        print_status "SUCCESS" "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
                    else
                        print_status "ERROR" "Failed to download file"
                    fi
                fi
                break
            elif [[ $message == ERROR:* ]]; then
                print_status "ERROR" "Blog generation failed: ${message#ERROR: }"
                exit 1
            fi
        fi
    done

print_status "SUCCESS" "Blog generation process completed!" 