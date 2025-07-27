"""
Core blog generation functionality
"""

import json
import os
import time
from typing import Dict, List, Tuple, Optional, Any
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..config.settings import settings
from ..config.prompts import PromptTemplates
from ..integrations.slack_integration import SlackIntegration
from ..integrations.google_docs_integration import GoogleDocsIntegration
from ..processors.slack_processor import SlackProcessor
from ..processors.gdoc_processor import GDocProcessor
from ..processors.ai_processor import AIProcessor
from ..utils.file_utils import save_markdown_as_word, save_markdown_file
from ..utils.image_utils import generate_images


class BlogGenerator:
    """Main blog generation orchestrator"""
    
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None):
        """
        Initialize blog generator
        
        Args:
            project_id: Google Cloud project ID. If not provided, uses settings
            location: Google Cloud location. If not provided, uses settings
        """
        self.project_id = project_id or settings.google_project_id
        self.location = location or settings.google_location
        
        if not self.project_id:
            raise ValueError("Google Cloud project ID is required")
        
        os.environ["GCLOUD_PROJECT"] = self.project_id
        
        # Initialize components
        self.slack_integration = SlackIntegration()
        self.google_docs_integration = GoogleDocsIntegration()
        self.slack_processor = SlackProcessor()
        self.gdoc_processor = GDocProcessor()
        self.ai_processor = AIProcessor()
        
        # Initialize AI model for blog generation - use gemini-2.5-pro for complex tasks
        self.model = ChatVertexAI(
            model_name="gemini-2.5-pro",
            project=self.project_id,
            location=self.location,
        )

    def generate_structured_blog_assets(self, source_type: str, source_data: Any, documentation_links: List[Tuple[str, str]]) -> Optional[Dict[str, Any]]:
        """
        Generates structured blog assets including content and image prompts.
        
        Args:
            source_type: Type of source ('slack' or 'gdoc')
            source_data: Source data (conversation or document content)
            documentation_links: List of relevant documentation links
            
        Returns:
            Dictionary with blog content and image prompts, or None if error
        """
        print(f"Generating blog post from {source_type} source...")
        
        prompt_template = ""
        invoke_input = {}

        if source_type == "slack":
            prompt_template = PromptTemplates.SLACK_GENERATE_STRUCTURED_BLOG_ASSETS
            invoke_input = {
                "conversation_text": source_data,
                "documentation_links": json.dumps(documentation_links)
            }
        elif source_type == "gdoc":
            prompt_template = PromptTemplates.GDOC_GENERATE_STRUCTURED_BLOG_ASSETS
            invoke_input = {
                "main_document_text": source_data["main_text"],
                "linked_documents_content": source_data.get("linked_documents_content", ""),
                "document_comments": "\n".join(source_data.get("comments", [])),
                "documentation_links": json.dumps(documentation_links)
            }
        else:
            raise ValueError("Invalid source_type. Must be 'slack' or 'gdoc'.")

        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        chain = prompt | self.model | output_parser

        # Generate the blog content
        raw_response = chain.invoke(invoke_input)
        
        print("\n--- Raw AI Response ---")
        print(raw_response)
        print("-----------------------\n")

        try:
            # Find the first '{' and the last '}' to isolate the JSON object
            start_index = raw_response.find('{')
            end_index = raw_response.rfind('}') + 1

            if start_index == -1 or end_index == 0:
                raise json.JSONDecodeError("Could not find a JSON object in the response.", raw_response, 0)

            # Extract only the JSON part of the string
            json_string = raw_response[start_index:end_index]
            
            # Clean up common JSON issues
            # Replace smart quotes with regular quotes
            json_string = json_string.replace('"', '"').replace('"', '"')
            json_string = json_string.replace(''', "'").replace(''', "'")
            
            # Replace em dashes and en dashes with regular hyphens
            json_string = json_string.replace('—', '-').replace('–', '-')
            
            # Remove any trailing commas before closing braces/brackets
            import re
            json_string = re.sub(r',(\s*[}\]])', r'\1', json_string)
            
            # Handle escaped characters properly
            json_string = json_string.replace('\\n', '\\n').replace('\\t', '\\t')
            
            # Fix common JSON syntax issues
            # Ensure proper escaping of backslashes
            json_string = json_string.replace('\\\\', '\\\\')
            
            # Clean up control characters that can break JSON parsing
            # Remove any control characters except newlines and tabs
            json_string = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', json_string)

            # Try to parse the JSON
            structured_output = json.loads(json_string)
            return structured_output

        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Failed to parse JSON from the AI's response. Reason: {e}")
            print(f"❌ JSON string that failed to parse:")
            print(json_string[:500] + "..." if len(json_string) > 500 else json_string)
            print("-----------------------")
            
            # Try a fallback approach - extract content manually
            print("🔄 Attempting fallback content extraction...")
            try:
                # Extract blog content manually
                blog_start = json_string.find('"blog_markdown_content": "') + len('"blog_markdown_content": "')
                blog_end = json_string.find('",\n    "image_prompts"')
                if blog_start > 0 and blog_end > blog_start:
                    blog_content = json_string[blog_start:blog_end]
                    
                    # Extract image prompts manually
                    image_prompts_start = json_string.find('"image_prompts": [')
                    if image_prompts_start > 0:
                        # Simple fallback structure
                        fallback_output = {
                            "blog_markdown_content": blog_content,
                            "image_prompts": [
                                {
                                    "placeholder": "[IMAGE_1]",
                                    "prompt": "A technical diagram showing the main concept discussed in the blog post."
                                }
                            ]
                        }
                        print("✅ Fallback content extraction successful!")
                        return fallback_output
            except Exception as fallback_error:
                print(f"❌ Fallback extraction also failed: {fallback_error}")
            
            return None

    def add_blog_assets(self, blog_assets: Dict[str, Any]) -> str:
        """
        Processes blog assets by generating images from prompts and replacing placeholders
        in the blog content with Markdown image syntax.

        Args:
            blog_assets: A dictionary containing blog content and image prompts.

        Returns:
            The blog content with placeholders replaced by Markdown image syntax.
        """
        return generate_images(blog_assets)

    def generate_from_slack(self, thread_link: str, output_filename: Optional[str] = None) -> Optional[str]:
        """
        Generate a blog post from a Slack thread.
        
        Args:
            thread_link: Slack thread permalink
            output_filename: Optional output filename. If not provided, generates one with timestamp
            
        Returns:
            Path to the generated blog file, or None if error
        """
        print(f"🚀 Starting Slack blog generation pipeline...")
        
        # 1. Fetch Slack messages
        slack_messages_all_details = self.slack_integration.get_all_thread_messages(thread_link)
        only_slack_messages = self.slack_processor.format_slack_data(slack_messages_all_details)
        print("\n✅ Collected Slack messages successfully!")

        # 2. Clean and process the conversation
        processed_slack_thread = self.slack_processor.cleanup_slack_thread(only_slack_messages)
        print("\n✅ Cleaning Complete!")

        # 3. Generate blog idea
        print("\n🤖 Getting title, target audience, key takeaways from cleaned conversation...")
        blog_idea = self.slack_processor.generate_key_high_level_idea(processed_slack_thread)

        # 4. Get relevant existing blogs
        print("\n--- Get relevant existing blogs and documentation links from Kapa AI ---")
        ask_ai_response = self.ai_processor.get_relevant_existing_blogs(
            query_text=blog_idea.get("Title", "") + "\n" + blog_idea.get("Takeaway", "") + "\n" + blog_idea.get("KapaAIinput", "")
        )

        # 5. Generate blog assets
        blog_assets = self.generate_structured_blog_assets("slack", processed_slack_thread, ask_ai_response or [])
        if not blog_assets:
            print("❌ Failed to generate blog assets")
            return None
            
        print("\n✅ Blog generation complete with placeholders!")

        # 6. Add images and finalize
        blog_content_with_placeholders = self.add_blog_assets(blog_assets)
        
        # 7. Save the blog
        if not output_filename:
            output_filename = f"blog_post_{time.strftime('%Y%m%d_%H%M%S')}.docx"
        
        print(f"📄 Saving the blog post to: {output_filename}")
        save_markdown_as_word(output_filename, blog_content_with_placeholders)
        
        return output_filename

    def generate_from_google_doc(self, doc_url: str, output_filename: Optional[str] = None) -> Optional[str]:
        """
        Generate a blog post from a Google Doc.
        
        Args:
            doc_url: Google Doc URL
            output_filename: Optional output filename. If not provided, generates one with timestamp
            
        Returns:
            Path to the generated blog file, or None if error
        """
        print(f"🚀 Starting Google Doc blog generation pipeline...")
        
        # 1. Extract document ID and read the document
        doc_id = self.google_docs_integration.extract_doc_id_from_url(doc_url)
        if not doc_id:
            print(f"❌ Could not extract document ID from URL: {doc_url}")
            return None
            
        print(f"📄 Reading Google Doc ID: {doc_id}")
        document_assets = self.google_docs_integration.read_document_multimodal(doc_id)
        if not document_assets:
            print("❌ Failed to read Google Doc")
            return None

        # 2. Enrich context from links
        gdoc_content = self.google_docs_integration.enrich_context_from_links(document_assets["text"])

        # 3. Generate blog idea
        blog_idea = self.gdoc_processor.generate_key_high_level_idea_for_gdoc(gdoc_content["main_text"])
        print("\n✅ AI-Generated summary of the document is complete!")

        # 4. Get relevant existing blogs
        print("\n--- Get relevant existing blogs and documentation links from Kapa AI ---")
        ask_ai_response = self.ai_processor.get_relevant_existing_blogs(
            query_text=blog_idea.get("Title", "") + "\n" + blog_idea.get("Takeaway", "") + "\n" + blog_idea.get("KapaAIinput", "")
        )

        # 5. Generate blog assets
        blog_assets = self.generate_structured_blog_assets("gdoc", gdoc_content, ask_ai_response or [])
        if not blog_assets:
            print("❌ Failed to generate blog assets")
            return None
            
        print("\n✅ Blog generation complete with placeholders!")

        # 6. Add images and finalize
        blog_content_with_placeholders = self.add_blog_assets(blog_assets)
        
        # 7. Save the blog
        if not output_filename:
            output_filename = f"blog_post_{time.strftime('%Y%m%d_%H%M%S')}.docx"
        
        print(f"📄 Saving the blog post to: {output_filename}")
        save_markdown_as_word(output_filename, blog_content_with_placeholders)
        
        return output_filename 