#!/usr/bin/env python3
"""
Simple CLI tool for AutoBlography with real-time logging
"""

import sys
import time
import argparse
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from autoblography import BlogGenerator
from autoblography.config.settings import settings

def print_progress(message, level="INFO"):
    """Print a progress message with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    prefix = {
        "INFO": "ℹ️",
        "SUCCESS": "✅", 
        "ERROR": "❌",
        "WARNING": "⚠️",
        "PROGRESS": "🔄"
    }.get(level, "ℹ️")
    
    print(f"[{timestamp}] {prefix} {message}")

def main():
    parser = argparse.ArgumentParser(description="AutoBlography CLI with real-time logging")
    parser.add_argument("--url", required=True, help="Slack thread or Google Doc URL")
    parser.add_argument("--source", required=True, choices=["slack", "gdoc"], 
                       help="Source type: slack or gdoc")
    parser.add_argument("--output", help="Output filename (optional)")
    
    args = parser.parse_args()
    
    # Validate settings
    print_progress("Validating environment variables...")
    if not settings.validate():
        print_progress("❌ Environment validation failed. Please check your configuration.", "ERROR")
        sys.exit(1)
    
    print_progress("✅ Environment validation passed", "SUCCESS")
    
    try:
        # Initialize blog generator
        print_progress("Initializing blog generator...", "PROGRESS")
        generator = BlogGenerator()
        
        # Generate blog based on source type
        if args.source == "slack":
            print_progress(f"Processing Slack thread: {args.url}", "PROGRESS")
            output_file = generator.generate_from_slack(args.url)
            result = {"output_file": output_file} if output_file else None
        else:
            print_progress(f"Processing Google Doc: {args.url}", "PROGRESS")
            output_file = generator.generate_from_google_doc(args.url)
            result = {"output_file": output_file} if output_file else None
        
        if not result:
            print_progress("❌ Blog generation failed", "ERROR")
            sys.exit(1)
        
        # Get output file
        output_file = result.get("output_file")
        if not output_file or not Path(output_file).exists():
            print_progress("❌ Generated file not found", "ERROR")
            sys.exit(1)
        
        print_progress(f"✅ Blog generation completed successfully!", "SUCCESS")
        print_progress(f"📄 Output file: {output_file}", "SUCCESS")
        
        # If output filename specified, copy the file
        if args.output:
            import shutil
            shutil.copy2(output_file, args.output)
            print_progress(f"📋 Copied to: {args.output}", "SUCCESS")
        
    except KeyboardInterrupt:
        print_progress("⏹️  Blog generation interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_progress(f"❌ Error: {str(e)}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main() 