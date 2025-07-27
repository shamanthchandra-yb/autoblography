import argparse
import time
from ai_hackathon_2025.generate_and_save_blog import generate_structured_blog_assets, save_markdown_as_word, add_blog_assets
from ai_hackathon_2025.slack_app import SlackApp
from ai_hackathon_2025.google_document_reader import read_google_doc_multimodal, enrich_context_from_links, generate_key_high_level_idea_for_gdoc, extract_doc_id_from_url
from ai_hackathon_2025.process_slack_thread import format_slack_data, cleanup_slack_thread, generate_key_high_level_idea
from ai_hackathon_2025.ask_ai import get_relevant_existing_blogs


def run_slack_pipeline(thread_link: str):
    slack_app = SlackApp()

    slack_messages_all_details = slack_app.get_all_thread_messages(thread_link)
    only_slack_messages = format_slack_data(slack_messages_all_details)
    print("\n✅ Collected Slack messages successfully!")

    processed_slack_thread = cleanup_slack_thread(only_slack_messages)
    print("\n✅ Cleaning Complete! Here is the output")
    # print(processed_slack_thread)

    print("\n🤖 Getting title, target audience, key takeaways from cleaned conversation...")
    blog_idea = generate_key_high_level_idea(processed_slack_thread)

    print("\n--- Get relevant existing blogs and documentation links from Kapa AI ---")
    ask_ai_response = get_relevant_existing_blogs(query_text=blog_idea.get("Title") + "\n" + blog_idea.get("Takeaway") + "\n" + blog_idea.get("KapaAIinput"))

    blog_assets = generate_structured_blog_assets("slack", processed_slack_thread, ask_ai_response)
    print("\n✅ Blog generation complete with placeholders!")

    blog_content_with_placeholders = add_blog_assets(blog_assets)
    print("📄 Saving the blog post to a Word document...")
    # append the current date to the filename

    # Generate the filename with the current time
    final_blog_filename = f"blog_post_{time.strftime('%Y%m%d_%H%M%S')}.docx"
    save_markdown_as_word(final_blog_filename, blog_content_with_placeholders)


def run_gdoc_pipeline(doc_id: str):

    print(f"🚀 Starting pipeline for Google Doc ID: {doc_id}")

    # 1. Read the Google Doc and all its assets
    document_assets = read_google_doc_multimodal(doc_id)
    if not document_assets:
        return  # Exit if the doc can't be read

    # 2. Enrich the context by fetching content from links
    gdoc_content = enrich_context_from_links(document_assets["text"])

    blog_idea = generate_key_high_level_idea_for_gdoc(gdoc_content["main_text"])
    print("\n✅ AI-Generated summary of the document is complete!")

    print("\n--- Get relevant existing blogs and documentation links from Kapa AI ---")
    ask_ai_response = get_relevant_existing_blogs(query_text=blog_idea.get("Title") + "\n" + blog_idea.get("Takeaway") + "\n" + blog_idea.get("KapaAIinput"))
    print(ask_ai_response)

    blog_assets = generate_structured_blog_assets("gdoc", gdoc_content, ask_ai_response)
    print("\n✅ Blog generation complete with placeholders!")

    blog_content_with_placeholders = add_blog_assets(blog_assets)
    print("📄 Saving the blog post to a Word document...")
    # # append the current date to the filename
    #
    # # Generate the filename with the current time
    final_blog_filename = f"blog_post_{time.strftime('%Y%m%d_%H%M%S')}.docx"
    save_markdown_as_word(final_blog_filename, blog_content_with_placeholders)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Generate a blog post from a Slack thread or a Google Doc.")
    parser.add_argument("--source", type=str, required=True, choices=['slack', 'gdoc'], help="The source of the content ('slack' or 'gdoc').")
    parser.add_argument("--input", type=str, required=True, help="The Slack thread URL or the Google Doc ID.")

    args = parser.parse_args()

    if args.source == 'slack':
        run_slack_pipeline(args.input)
    elif args.source == 'gdoc':
        gdoc_id = extract_doc_id_from_url(args.input)
        run_gdoc_pipeline(gdoc_id)
    else:
        print("Invalid argument. Please use 'slack' or 'gdoc'.")
        exit(1)


if __name__ == "__main__":
    main()
