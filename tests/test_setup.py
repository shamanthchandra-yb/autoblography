#!/usr/bin/env python3
"""
Basic tests to verify Autoblography setup and structure.
Run these tests to ensure the project restructuring was successful.
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def test_python_version():
    """Test that Python version is 3.8 or higher."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.8+")
        return False

def test_package_structure():
    """Test that the package structure is correct."""
    print("\n📁 Testing package structure...")
    
    required_files = [
        "ai_hackathon_2025/__init__.py",
        "ai_hackathon_2025/main.py",
        "ai_hackathon_2025/generate_and_save_blog.py",
        "ai_hackathon_2025/slack_app.py",
        "ai_hackathon_2025/google_document_reader.py",
        "ai_hackathon_2025/image_generation.py",
        "ai_hackathon_2025/ask_ai.py",
        "ai_hackathon_2025/process_slack_thread.py",
        "ai_hackathon_2025/prompt_constant.py",
        "README.md",
        "setup.py",
        "requirements.txt",
        "LICENSE"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_package_imports():
    """Test that the main package can be imported."""
    print("\n📦 Testing package imports...")
    
    try:
        import ai_hackathon_2025
        print(f"✅ Main package imported successfully")
        print(f"   Version: {getattr(ai_hackathon_2025, '__version__', 'unknown')}")
        
        # Test individual module imports
        modules_to_test = [
            'ai_hackathon_2025.main',
            'ai_hackathon_2025.slack_app',
            'ai_hackathon_2025.google_document_reader',
            'ai_hackathon_2025.generate_and_save_blog',
            'ai_hackathon_2025.image_generation',
            'ai_hackathon_2025.ask_ai',
            'ai_hackathon_2025.process_slack_thread',
            'ai_hackathon_2025.prompt_constant'
        ]
        
        failed_imports = []
        for module_name in modules_to_test:
            try:
                importlib.import_module(module_name)
                print(f"✅ {module_name}")
            except ImportError as e:
                print(f"❌ {module_name}: {e}")
                failed_imports.append(module_name)
        
        return len(failed_imports) == 0
        
    except ImportError as e:
        print(f"❌ Failed to import main package: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available."""
    print("\n📋 Testing dependencies...")
    
    required_packages = [
        'google.auth',
        'googleapiclient',
        'langchain_core',
        'langchain_google_vertexai',
        'slack_sdk',
        'requests',
        'pypandoc'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {missing_packages}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_cli_interface():
    """Test that the CLI interface works."""
    print("\n💻 Testing CLI interface...")
    
    try:
        # Test help command
        result = subprocess.run([
            sys.executable, '-m', 'ai_hackathon_2025.main', '--help'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ CLI help command works")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ CLI help command timed out")
        return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_environment_setup():
    """Test environment configuration."""
    print("\n🔧 Testing environment setup...")
    
    # Check for .env file
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file exists")
        
        # Read and check basic structure
        with open('.env', 'r') as f:
            content = f.read()
            
        required_vars = [
            'GOOGLE_APPLICATION_CREDENTIALS',
            'GCLOUD_PROJECT'
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Missing environment variables in .env: {missing_vars}")
        else:
            print("✅ Required environment variables present in .env")
            
    else:
        print("⚠️ .env file not found - create one for configuration")
    
    return True

def test_documentation():
    """Test that documentation files exist and are readable."""
    print("\n📚 Testing documentation...")
    
    doc_files = [
        ("README.md", "Main documentation"),
        ("docs/SETUP.md", "Setup guide"),
        ("examples/EXAMPLES.md", "Usage examples"),
        ("CHANGELOG.md", "Change history")
    ]
    
    all_good = True
    for file_path, description in doc_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 100:  # Basic content check
                        print(f"✅ {description} ({file_path})")
                    else:
                        print(f"⚠️ {description} seems too short ({file_path})")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                all_good = False
        else:
            print(f"❌ Missing: {description} ({file_path})")
            all_good = False
    
    return all_good

def run_all_tests():
    """Run all tests and provide a summary."""
    print("🧪 Running Autoblography Test Suite")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Structure", test_package_structure),
        ("Package Imports", test_package_imports),
        ("Dependencies", test_dependencies),
        ("CLI Interface", test_cli_interface),
        ("Environment Setup", test_environment_setup),
        ("Documentation", test_documentation)
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
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your project is ready to use.")
        print("\nNext steps:")
        print("1. Configure your .env file with actual credentials")
        print("2. Try running: python -m ai_hackathon_2025.main --help")
        print("3. Test with a real Slack thread or Google Doc")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)