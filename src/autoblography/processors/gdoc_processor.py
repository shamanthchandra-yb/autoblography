"""
Google Docs content processing
"""

import os
from typing import Dict
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..config.settings import settings
from ..config.prompts import PromptTemplates


class GDocProcessor:
    """Processes Google Docs content"""
    
    def __init__(self, project_id: str = None, location: str = None):
        """
        Initialize Google Docs processor
        
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

    def generate_key_high_level_idea_for_gdoc(self, technical_document_text: str) -> Dict[str, str]:
        """
        Generates blog post ideas from Google Doc content.
        
        Args:
            technical_document_text: Technical document text
            
        Returns:
            Dictionary with blog idea components
        """
        prompt_template = PromptTemplates.GDOC_GENERATE_KEY_HIGH_LEVEL_IDEA
        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        
        chain = prompt | self.model | output_parser
        result_text = chain.invoke({"technical_document_text": technical_document_text})

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