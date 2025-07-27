#!/usr/bin/env python3
"""
Basic usage example for AutoBlography
"""

import os
from autoblography import BlogGenerator


def main():
    """Example usage of AutoBlography"""
    
    # Set up environment variables (in production, set these in your environment)
    os.environ["SLACK_TOKEN"] = "xoxb-your-slack-token"
    os.environ["GOOGLE_PROJECT_ID"] = "your-google-cloud-project-id"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"
    
    # Initialize the blog generator
    generator = BlogGenerator()
    
    # Example 1: Generate blog from Slack thread
    print("=== Example 1: Slack Thread to Blog ===")
    slack_thread_url = "https://company.slack.com/archives/C1234567/p1234567890123456"
    
    try:
        output_file = generator.generate_from_slack(slack_thread_url)
        if output_file:
            print(f"✅ Blog generated successfully: {output_file}")
        else:
            print("❌ Failed to generate blog from Slack thread")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Generate blog from Google Doc
    print("=== Example 2: Google Doc to Blog ===")
    google_doc_url = "https://docs.google.com/document/d/1ABC123XYZ/edit"
    
    try:
        output_file = generator.generate_from_google_doc(google_doc_url)
        if output_file:
            print(f"✅ Blog generated successfully: {output_file}")
        else:
            print("❌ Failed to generate blog from Google Doc")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 