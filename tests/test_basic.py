"""
Basic tests for AutoBlography
"""

import pytest
from unittest.mock import Mock, patch

from autoblography.config.settings import Settings
from autoblography.integrations.slack_integration import SlackIntegration
from autoblography.integrations.google_docs_integration import GoogleDocsIntegration


class TestSettings:
    """Test settings configuration"""
    
    def test_settings_initialization(self):
        """Test that settings can be initialized"""
        settings = Settings()
        assert settings is not None
    
    def test_settings_validation_with_missing_required(self):
        """Test settings validation with missing required fields"""
        settings = Settings()
        # Mock missing required settings
        settings.slack_token = None
        settings.google_project_id = None
        
        assert not settings.validate()
    
    def test_settings_validation_with_required(self):
        """Test settings validation with required fields"""
        settings = Settings()
        # Mock required settings
        settings.slack_token = "xoxb-test-token"
        settings.google_project_id = "test-project"
        
        assert settings.validate()


class TestSlackIntegration:
    """Test Slack integration"""
    
    @patch('autoblography.integrations.slack_integration.WebClient')
    def test_slack_integration_initialization(self, mock_webclient):
        """Test Slack integration initialization"""
        integration = SlackIntegration(token="test-token")
        assert integration.token == "test-token"
        mock_webclient.assert_called_once_with(token="test-token")
    
    def test_parse_permalink_valid(self):
        """Test parsing valid Slack permalink"""
        integration = SlackIntegration(token="test-token")
        url = "https://company.slack.com/archives/C1234567/p1234567890123456"
        
        channel_id, thread_ts = integration._parse_permalink(url)
        
        assert channel_id == "C1234567"
        assert thread_ts == "1234567890.123456"
    
    def test_parse_permalink_invalid(self):
        """Test parsing invalid Slack permalink"""
        integration = SlackIntegration(token="test-token")
        url = "https://invalid-url.com"
        
        channel_id, thread_ts = integration._parse_permalink(url)
        
        assert channel_id is None
        assert thread_ts is None


class TestGoogleDocsIntegration:
    """Test Google Docs integration"""
    
    def test_google_docs_integration_initialization(self):
        """Test Google Docs integration initialization"""
        integration = GoogleDocsIntegration(project_id="test-project")
        assert integration.project_id == "test-project"
    
    def test_extract_doc_id_from_url_valid(self):
        """Test extracting document ID from valid Google Doc URL"""
        integration = GoogleDocsIntegration(project_id="test-project")
        url = "https://docs.google.com/document/d/1ABC123XYZ/edit"
        
        doc_id = integration.extract_doc_id_from_url(url)
        
        assert doc_id == "1ABC123XYZ"
    
    def test_extract_doc_id_from_url_invalid(self):
        """Test extracting document ID from invalid URL"""
        integration = GoogleDocsIntegration(project_id="test-project")
        url = "https://invalid-url.com"
        
        doc_id = integration.extract_doc_id_from_url(url)
        
        assert doc_id is None


if __name__ == "__main__":
    pytest.main([__file__]) 