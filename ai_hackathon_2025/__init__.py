"""
Autoblography - AI-Powered Blog Generator

Transform your Slack conversations and Google Documents into professional blog posts 
with AI-powered content generation, image creation, and structured formatting.
"""

__version__ = "1.0.0"
__author__ = "AI Hackathon 2025 Team"
__email__ = "team@autoblography.ai"

# Core functionality imports
from .main import run_slack_pipeline, run_gdoc_pipeline
from .generate_and_save_blog import generate_structured_blog_assets, save_markdown_as_word
from .slack_app import SlackApp
from .google_document_reader import read_google_doc_multimodal
from .image_generation import generate_image_from_prompt_imagen

__all__ = [
    "run_slack_pipeline",
    "run_gdoc_pipeline", 
    "generate_structured_blog_assets",
    "save_markdown_as_word",
    "SlackApp",
    "read_google_doc_multimodal",
    "generate_image_from_prompt_imagen"
]