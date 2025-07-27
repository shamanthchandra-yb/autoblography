"""
Main CLI entry point for AutoBlography
"""

import argparse
import sys
from pathlib import Path

from .core.blog_generator import BlogGenerator
from .config.settings import settings


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AutoBlography - AI-powered blog generation from Slack threads and Google Docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate blog from Slack thread
  python -m autoblography --source slack --input "https://company.slack.com/archives/C1234567/p1234567890123456"
  
  # Generate blog from Google Doc
  python -m autoblography --source gdoc --input "https://docs.google.com/document/d/1ABC123XYZ/edit"
  
  # Specify output filename
  python -m autoblography --source slack --input "https://..." --output "my_blog_post.docx"
        """
    )
    
    parser.add_argument(
        "--source", 
        type=str, 
        required=True, 
        choices=['slack', 'gdoc'], 
        help="The source of the content ('slack' or 'gdoc')"
    )
    
    parser.add_argument(
        "--input", 
        type=str, 
        required=True, 
        help="The Slack thread URL or the Google Doc URL"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output filename (optional, will generate timestamped filename if not provided)"
    )
    
    parser.add_argument(
        "--project-id", 
        type=str, 
        help="Google Cloud project ID (optional, uses GOOGLE_PROJECT_ID env var if not provided)"
    )
    
    parser.add_argument(
        "--location", 
        type=str, 
        default="us-central1",
        help="Google Cloud location (default: us-central1)"
    )

    args = parser.parse_args()

    # Validate settings
    if not settings.validate():
        print("\n❌ Configuration validation failed. Please check your environment variables.")
        print("\nRequired environment variables:")
        print("  - SLACK_TOKEN: Your Slack API token")
        print("  - GOOGLE_PROJECT_ID: Your Google Cloud project ID")
        print("  - KAPA_API_KEY: Kapa AI API key for finding relevant blogs")
        print("\nOptional environment variables:")
        print("  - GOOGLE_LOCATION: Google Cloud location (default: us-central1)")
        print("  - VERTEX_AI_MODEL: AI model to use (default: gemini-2.0-flash-001)")
        print("  - OUTPUT_DIR: Output directory (default: output)")
        print("  - IMAGE_OUTPUT_DIR: Image output directory (default: images)")
        sys.exit(1)

    try:
        # Initialize blog generator
        generator = BlogGenerator(
            project_id=args.project_id,
            location=args.location
        )

        # Generate blog based on source type
        if args.source == 'slack':
            output_file = generator.generate_from_slack(args.input, args.output)
        elif args.source == 'gdoc':
            output_file = generator.generate_from_google_doc(args.input, args.output)
        else:
            print("❌ Invalid source type. Please use 'slack' or 'gdoc'.")
            sys.exit(1)

        if output_file:
            print(f"\n🎉 Blog generation completed successfully!")
            print(f"📄 Output file: {output_file}")
        else:
            print("\n❌ Blog generation failed.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 