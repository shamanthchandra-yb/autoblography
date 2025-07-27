"""
Google Docs integration for reading documents and extracting content
"""

import os
import re
import google.auth
from typing import Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from llama_index.readers.web import SimpleWebPageReader

from ..config.settings import settings
from ..config.prompts import PromptTemplates


class GoogleDocsIntegration:
    """Google Docs integration for reading documents and extracting content"""
    
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None):
        """
        Initialize Google Docs integration
        
        Args:
            project_id: Google Cloud project ID. If not provided, uses GOOGLE_PROJECT_ID from settings
            location: Google Cloud location. If not provided, uses GOOGLE_LOCATION from settings
        """
        self.project_id = project_id or settings.google_project_id
        self.location = location or settings.google_location
        
        if not self.project_id:
            raise ValueError("Google Cloud project ID is required. Set GOOGLE_PROJECT_ID environment variable or pass project_id parameter.")
        
        os.environ["GCLOUD_PROJECT"] = self.project_id
        
        # Scopes for both Docs and Drive APIs
        self.scopes = [
            'https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]

    def read_document_multimodal(self, document_id: str) -> Optional[Dict]:
        """
        Reads a Google Doc, extracts all text (including hyperlink URLs),
        downloads all images, and reads all comments.
        
        Args:
            document_id: Google Doc document ID
            
        Returns:
            Dictionary with text, image paths, and comments, or None if error
        """
        print(f"📄 Reading Google Doc multimodally (ID: {document_id})...")

        # Authenticate using the environment variable
        creds, _ = google.auth.default(scopes=self.scopes)

        # Build both the Docs and Drive service clients
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Get the document structure from the Docs API
        try:
            document = docs_service.documents().get(documentId=document_id).execute()
        except HttpError as e:
            if e.resp.status == 403:
                print(f"   -> ❌ ERROR: Permission denied for Google Doc ID '{document_id}'. Ensure it's shared with the service account.")
                return None
            else:
                raise e

        doc_content = document.get('body').get('content')

        extracted_text = ""
        image_paths = []
        image_counter = 1

        # Parse the document content for text, links, and images
        print("📝 Parsing document text, links, and images...")
        for element in doc_content:
            if 'paragraph' in element:
                para_elements = element.get('paragraph').get('elements')
                for el in para_elements:
                    # Standard Text Run
                    text_run = el.get('textRun')
                    if text_run:
                        extracted_text += text_run.get('content')
                        text_style = text_run.get('textStyle', {})
                        link = text_style.get('link')
                        if link and 'url' in link:
                            extracted_text += f" ({link.get('url')}) "

                    # Rich Link (like Google Doc previews)
                    rich_link = el.get('richLink')
                    if rich_link:
                        rich_link_props = rich_link.get('richLinkProperties')
                        if rich_link_props and 'uri' in rich_link_props:
                            url = rich_link_props.get('uri')
                            extracted_text += f" ({url}) "
                            print(f"   -> Found rich link: {url}")

                    # Embedded Objects (Images, Smart Chips)
                    inline_obj_element = el.get('inlineObjectElement')
                    if inline_obj_element:
                        inline_obj_id = inline_obj_element.get('inlineObjectId')
                        if inline_obj_id:
                            inline_object = document.get('inlineObjects').get(inline_obj_id)
                            embedded_object = inline_object.get('inlineObjectProperties').get('embeddedObject')

                            if 'imageProperties' in embedded_object:
                                image_properties = embedded_object.get('imageProperties')
                                content_uri = image_properties.get('contentUri')

                                if content_uri:
                                    print(f"🖼️  Found image. Attempting to download...")

                                    try:
                                        resp, content = drive_service._http.request(content_uri)

                                        if resp.status == 200:
                                            # Create images directory if it doesn't exist
                                            os.makedirs(settings.image_output_dir, exist_ok=True)
                                            
                                            image_filename = f"gdoc_image_{image_counter}.png"
                                            image_path = os.path.join(settings.image_output_dir, image_filename)
                                            
                                            with open(image_path, 'wb') as f:
                                                f.write(content)
                                            
                                            image_paths.append(image_path)
                                            print(f"   -> ✅ Downloaded image: {image_path}")
                                            image_counter += 1
                                        else:
                                            print(f"   -> ❌ Failed to download image: {resp.status}")
                                    except Exception as e:
                                        print(f"   -> ❌ Error downloading image: {e}")

        # Get comments from the document
        print("💬 Fetching document comments...")
        comments = []
        try:
            comments_response = docs_service.documents().comments().list(documentId=document_id).execute()
            comments = comments_response.get('comments', [])
            print(f"   -> Found {len(comments)} comments")
        except Exception as e:
            print(f"   -> ❌ Error fetching comments: {e}")

        # Extract comment text
        comment_texts = []
        for comment in comments:
            if 'content' in comment:
                comment_texts.append(comment['content'])

        return {
            "text": extracted_text,
            "images": image_paths,
            "comments": comment_texts
        }

    def enrich_context_from_links(self, main_gdoc_text: str) -> Dict:
        """
        Enriches the context by fetching content from links found in the document.
        
        Args:
            main_gdoc_text: Main document text containing links
            
        Returns:
            Dictionary with main text and linked content
        """
        print("🔗 Enriching context from links...")
        
        # Extract URLs from the text
        url_pattern = r'https?://[^\s\)]+'
        urls = re.findall(url_pattern, main_gdoc_text)
        
        linked_documents_content = ""
        
        for url in urls:
            try:
                print(f"   -> Fetching content from: {url}")
                documents = SimpleWebPageReader(html_to_text=True).load_data([url])
                
                if documents:
                    # Take first 1000 characters to avoid overwhelming the context
                    content = documents[0].text[:1000]
                    linked_documents_content += f"\n--- Content from {url} ---\n{content}\n"
                    print(f"   -> ✅ Successfully fetched content from {url}")
                else:
                    print(f"   -> ⚠️  No content found at {url}")
                    
            except Exception as e:
                print(f"   -> ❌ Error fetching content from {url}: {e}")
        
        return {
            "main_text": main_gdoc_text,
            "linked_documents_content": linked_documents_content
        }

    def extract_doc_id_from_url(self, url: str) -> Optional[str]:
        """
        Extracts document ID from Google Doc URL.
        
        Args:
            url: Google Doc URL
            
        Returns:
            Document ID or None if not found
        """
        # Pattern for Google Doc URLs
        patterns = [
            r'/document/d/([a-zA-Z0-9-_]+)',
            r'/document/d/([a-zA-Z0-9-_]+)/edit',
            r'/document/d/([a-zA-Z0-9-_]+)/view'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None 