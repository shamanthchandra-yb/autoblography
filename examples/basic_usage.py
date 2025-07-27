#!/usr/bin/env python3
"""
Basic usage example for AutoBlography
"""

import os
from autoblography import BlogGenerator


def main():
    """Example usage of AutoBlography"""
    
    # Initialize the blog generator
    generator = BlogGenerator()
    
    # Example 1: Generate blog from Slack thread
    print("=== Example 1: Slack Thread to Blog ===")
    # slack_thread_url = "https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219"
    slack_thread_url = "https://yugabyte.slack.com/archives/C017TTZ9EV7/p1751000062671159"
    
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