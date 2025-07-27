#!/usr/bin/env python3
"""
Integration tests for Autoblography core functionality.
These tests use mock data to verify the pipeline works without requiring actual API credentials.
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

def test_slack_app_parsing():
    """Test Slack URL parsing functionality."""
    print("🔗 Testing Slack URL parsing...")
    
    try:
        from ai_hackathon_2025.slack_app import SlackApp
        
        slack_app = SlackApp()
        
        # Test permalink parsing
        test_url = "https://workspace.slack.com/archives/C1234567/p1234567890123456"
        channel_id, thread_ts = slack_app._parse_permalink(test_url)
        
        if channel_id == "C1234567" and thread_ts == "1234567890.123456":
            print("✅ Slack URL parsing works correctly")
            return True
        else:
            print(f"❌ Slack URL parsing failed: {channel_id}, {thread_ts}")
            return False
            
    except Exception as e:
        print(f"❌ Slack URL parsing test failed: {e}")
        return False

def test_google_doc_id_extraction():
    """Test Google Doc ID extraction from URL."""
    print("\n📄 Testing Google Doc ID extraction...")
    
    try:
        from ai_hackathon_2025.google_document_reader import extract_doc_id_from_url
        
        test_cases = [
            ("https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit", 
             "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"),
            ("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", 
             "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
        ]
        
        all_passed = True
        for test_url, expected_id in test_cases:
            result = extract_doc_id_from_url(test_url)
            if result == expected_id:
                print(f"✅ {test_url[:50]}... -> {result}")
            else:
                print(f"❌ {test_url[:50]}... -> {result} (expected {expected_id})")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Google Doc ID extraction test failed: {e}")
        return False

def test_blog_generation_mock():
    """Test blog generation with mock data."""
    print("\n📝 Testing blog generation (mock)...")
    
    try:
        # Mock the AI calls to avoid needing real credentials
        with patch('ai_hackathon_2025.generate_and_save_blog.ChatVertexAI') as mock_ai:
            with patch('ai_hackathon_2025.generate_and_save_blog.pypandoc.convert_text') as mock_pandoc:
                
                # Setup mocks
                mock_ai_instance = MagicMock()
                mock_ai.return_value = mock_ai_instance
                
                # Mock AI response
                mock_response = MagicMock()
                mock_response.content = """
                {
                    "title": "Test Blog Post",
                    "introduction": "This is a test introduction",
                    "sections": [
                        {
                            "heading": "Test Section",
                            "content": "Test content"
                        }
                    ],
                    "conclusion": "Test conclusion"
                }
                """
                
                mock_ai_instance.invoke.return_value = mock_response
                mock_pandoc.return_value = None
                
                from ai_hackathon_2025.generate_and_save_blog import generate_structured_blog_assets
                
                # Test with mock data
                mock_slack_data = "User1: Hello\nUser2: How are you?\nUser1: I'm good!"
                mock_docs_data = [("https://example.com", "Example documentation")]
                
                result = generate_structured_blog_assets("slack", mock_slack_data, mock_docs_data)
                
                if result and isinstance(result, dict):
                    print("✅ Blog generation pipeline works (mocked)")
                    return True
                else:
                    print("❌ Blog generation returned unexpected result")
                    return False
                    
    except Exception as e:
        print(f"❌ Blog generation test failed: {e}")
        return False

def test_image_generation_mock():
    """Test image generation with mock data."""
    print("\n🎨 Testing image generation (mock)...")
    
    try:
        with patch('ai_hackathon_2025.image_generation.vertexai') as mock_vertexai:
            with patch('ai_hackathon_2025.image_generation.ImageGenerationModel') as mock_model:
                
                # Setup mocks
                mock_model_instance = MagicMock()
                mock_model.from_pretrained.return_value = mock_model_instance
                
                mock_response = MagicMock()
                mock_image = MagicMock()
                mock_image.save.return_value = None
                mock_response.images = [mock_image]
                mock_model_instance.generate_images.return_value = mock_response
                
                from ai_hackathon_2025.image_generation import generate_image_from_prompt_imagen
                
                # Test with mock data
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    temp_filename = tmp_file.name
                
                try:
                    generate_image_from_prompt_imagen("test prompt", temp_filename)
                    print("✅ Image generation pipeline works (mocked)")
                    return True
                finally:
                    # Clean up
                    if os.path.exists(temp_filename):
                        os.unlink(temp_filename)
                        
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

def test_cli_help():
    """Test that CLI help works."""
    print("\n💻 Testing CLI help...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'ai_hackathon_2025.main', '--help'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'usage:' in result.stdout.lower():
            print("✅ CLI help works")
            print(f"   Output preview: {result.stdout[:100]}...")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ CLI help test failed: {e}")
        return False

def test_prompt_constants():
    """Test that prompt constants are accessible."""
    print("\n📋 Testing prompt constants...")
    
    try:
        from ai_hackathon_2025.prompt_constant import (
            SLACK_GENERATE_STRUCTURED_BLOG_ASSETS,
            GDOC_GENERATE_STRUCTURED_BLOG_ASSETS
        )
        
        if (isinstance(SLACK_GENERATE_STRUCTURED_BLOG_ASSETS, str) and 
            len(SLACK_GENERATE_STRUCTURED_BLOG_ASSETS) > 100):
            print("✅ Slack prompt constant loaded")
        else:
            print("❌ Slack prompt constant issue")
            return False
            
        if (isinstance(GDOC_GENERATE_STRUCTURED_BLOG_ASSETS, str) and 
            len(GDOC_GENERATE_STRUCTURED_BLOG_ASSETS) > 100):
            print("✅ Google Doc prompt constant loaded")
        else:
            print("❌ Google Doc prompt constant issue")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Prompt constants test failed: {e}")
        return False

def run_integration_tests():
    """Run all integration tests."""
    print("🔬 Running Autoblography Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Slack URL Parsing", test_slack_app_parsing),
        ("Google Doc ID Extraction", test_google_doc_id_extraction),
        ("Blog Generation (Mock)", test_blog_generation_mock),
        ("Image Generation (Mock)", test_image_generation_mock),
        ("CLI Help", test_cli_help),
        ("Prompt Constants", test_prompt_constants)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} integration tests passed")
    
    if passed == total:
        print("\n🎉 All integration tests passed!")
        print("Your core functionality is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} integration tests failed.")
        print("Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)