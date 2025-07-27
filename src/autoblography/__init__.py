"""
AutoBlography - AI-powered blog generation from Slack threads and Google Docs
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "AI-powered blog generation tool that converts Slack threads and Google Docs into structured blog posts"

from .core.blog_generator import BlogGenerator
from .integrations.slack_integration import SlackIntegration
from .integrations.google_docs_integration import GoogleDocsIntegration

__all__ = [
    "BlogGenerator",
    "SlackIntegration", 
    "GoogleDocsIntegration"
] 