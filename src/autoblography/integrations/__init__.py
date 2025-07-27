"""
Integration modules for external services
"""

from .slack_integration import SlackIntegration
from .google_docs_integration import GoogleDocsIntegration

__all__ = ["SlackIntegration", "GoogleDocsIntegration"] 