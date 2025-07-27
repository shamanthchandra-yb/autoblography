"""
Application settings and configuration
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings loaded from environment variables"""
    
    # Slack Configuration
    slack_token: Optional[str] = None
    
    # Google Cloud Configuration
    google_project_id: Optional[str] = None
    google_location: str = "us-central1"
    
    # AI Configuration
    # Note: gemini-2.0-flash-001 is used for simple tasks (Slack/Google Doc processing)
    # gemini-2.5-pro is used for complex tasks (blog generation, image generation)
    vertex_ai_model: str = "gemini-2.0-flash-001"
    
    # Output Configuration
    output_dir: str = "output"
    image_output_dir: str = "images"
    
    # Kapa AI Configuration (if used)
    kapa_api_key: Optional[str] = None
    kapa_base_url: str = "https://api.kapa.ai"
    
    def __post_init__(self):
        """Load settings from environment variables"""
        self.slack_token = os.getenv("SLACK_TOKEN", self.slack_token)
        self.google_project_id = os.getenv("GOOGLE_PROJECT_ID", self.google_project_id)
        self.google_location = os.getenv("GOOGLE_LOCATION", self.google_location)
        self.vertex_ai_model = os.getenv("VERTEX_AI_MODEL", self.vertex_ai_model)
        self.output_dir = os.getenv("OUTPUT_DIR", self.output_dir)
        self.image_output_dir = os.getenv("IMAGE_OUTPUT_DIR", self.image_output_dir)
        self.kapa_api_key = os.getenv("KAPA_API_KEY", self.kapa_api_key)
        self.kapa_base_url = os.getenv("KAPA_BASE_URL", self.kapa_base_url)
    
    def validate(self) -> bool:
        """Validate that required settings are present"""
        required_settings = []
        
        if not self.slack_token:
            required_settings.append("SLACK_TOKEN")
        
        if not self.google_project_id:
            required_settings.append("GOOGLE_PROJECT_ID")
        
        if not self.kapa_api_key:
            required_settings.append("KAPA_API_KEY")
        
        if required_settings:
            print(f"❌ Missing required environment variables: {', '.join(required_settings)}")
            return False
        
        return True


# Global settings instance
settings = Settings() 