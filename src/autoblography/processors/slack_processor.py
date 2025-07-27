"""
Slack content processing and cleaning
"""

import os
from typing import Dict, List
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..config.settings import settings
from ..config.prompts import PromptTemplates


class SlackProcessor:
    """Processes and cleans Slack conversation data"""
    
    def __init__(self, project_id: str = None, location: str = None):
        """
        Initialize Slack processor
        
        Args:
            project_id: Google Cloud project ID. If not provided, uses settings
            location: Google Cloud location. If not provided, uses settings
        """
        self.project_id = project_id or settings.google_project_id
        self.location = location or settings.google_location
        
        if not self.project_id:
            raise ValueError("Google Cloud project ID is required")
        
        os.environ["GCLOUD_PROJECT"] = self.project_id
        
        # Initialize the AI model
        self.model = ChatVertexAI(
            model_name=settings.vertex_ai_model,
            project=self.project_id,
            location=self.location,
        )

    def format_slack_data(self, slack_json_data: List[Dict]) -> str:
        """
        Takes a list of Slack message objects (JSON/dictionaries) and formats
        it into a simple, readable string.
        
        Args:
            slack_json_data: List of Slack message objects
            
        Returns:
            Formatted conversation string
        """
        formatted_lines = []
        for message in slack_json_data:
            # We only care about actual user messages
            if message.get('type') == 'message' and message.get('user'):
                user_id = message['user']
                text = message.get('text', '')
                formatted_lines.append(f"From: {user_id}\n{text}\n")

        return "\n".join(formatted_lines)

    def cleanup_slack_thread(self, raw_conversation: str) -> str:
        """
        Cleans a raw Slack conversation by removing sensitive information
        and anonymizing participants.
        
        Args:
            raw_conversation: Raw Slack conversation text
            
        Returns:
            Cleaned conversation text
        """
        prompt_template = PromptTemplates.SLACK_CLEANUP_SLACK_THREAD
        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        
        chain = prompt | self.model | output_parser
        
        print(f"🤖 Processing Slack conversation with {settings.vertex_ai_model}...")
        result = chain.invoke({"conversation_text": raw_conversation})
        
        return result

    def generate_key_high_level_idea(self, cleaned_conversation: str) -> Dict[str, str]:
        """
        Generates blog post ideas from cleaned Slack conversation.
        
        Args:
            cleaned_conversation: Cleaned conversation text
            
        Returns:
            Dictionary with blog idea components
        """
        prompt_template = PromptTemplates.SLACK_GENERATE_KEY_HIGH_LEVEL_IDEA
        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        
        chain = prompt | self.model | output_parser
        result_text = chain.invoke({"cleaned_conversation": cleaned_conversation})

        # Parse the text output into a dictionary
        idea_dict = {}
        for line in result_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                idea_dict[key.strip()] = value.strip()

        print(f"""--- Blog Idea Variables ---
        Title: {idea_dict.get("Title")}
        Target Audience: {idea_dict.get("Audience")}
        Key Takeaway: {idea_dict.get("Takeaway")}
        Summary for Kapa AI: {idea_dict.get("KapaAIinput")}
        --------------------------""")

        return idea_dict 