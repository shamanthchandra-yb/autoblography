#!/usr/bin/env python3
"""
Minimal structure test for Autoblography.
Tests project structure without requiring external dependencies.
"""

import sys
import os
from pathlib import Path

def test_project_structure():
    """Test that all required files and directories exist."""
    print("📁 Testing project structure...")
    
    required_items = [
        # Core package files
        ("ai_hackathon_2025/__init__.py", "file"),
        ("ai_hackathon_2025/main.py", "file"),
        ("ai_hackathon_2025/generate_and_save_blog.py", "file"),
        ("ai_hackathon_2025/slack_app.py", "file"),
        ("ai_hackathon_2025/google_document_reader.py", "file"),
        ("ai_hackathon_2025/image_generation.py", "file"),
        ("ai_hackathon_2025/ask_ai.py", "file"),
        ("ai_hackathon_2025/process_slack_thread.py", "file"),
        ("ai_hackathon_2025/prompt_constant.py", "file"),
        
        # Documentation
        ("README.md", "file"),
        ("docs/SETUP.md", "file"),
        ("examples/EXAMPLES.md", "file"),
        ("CHANGELOG.md", "file"),
        
        # Configuration files
        ("setup.py", "file"),
        ("requirements.txt", "file"),
        ("LICENSE", "file"),
        (".gitignore", "file"),
        
        # Scripts
        ("scripts/setup_dev.sh", "file"),
        ("test_all.py", "file"),
        
        # Test files
        ("tests/test_setup.py", "file"),
        ("tests/test_integration.py", "file"),
        
        # Directories
        ("docs", "dir"),
        ("examples", "dir"),
        ("scripts", "dir"),
        ("tests", "dir"),
    ]
    
    missing_items = []
    for item_path, item_type in required_items:
        path = Path(item_path)
        if item_type == "file" and not path.is_file():
            missing_items.append(f"File: {item_path}")
        elif item_type == "dir" and not path.is_dir():
            missing_items.append(f"Directory: {item_path}")
    
    if missing_items:
        print("❌ Missing items:")
        for item in missing_items:
            print(f"   - {item}")
        return False
    else:
        print("✅ All required files and directories present")
        return True

def test_file_contents():
    """Test that key files have content."""
    print("\n📄 Testing file contents...")
    
    files_to_check = [
        ("README.md", 1000),  # Should be substantial
        ("ai_hackathon_2025/__init__.py", 100),  # Should have imports
        ("ai_hackathon_2025/main.py", 500),  # Should have main logic
        ("setup.py", 200),  # Should have setup config
        ("requirements.txt", 50),  # Should have dependencies
    ]
    
    all_good = True
    for file_path, min_size in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) >= min_size:
                    print(f"✅ {file_path} ({len(content)} chars)")
                else:
                    print(f"⚠️ {file_path} seems too short ({len(content)} chars, expected {min_size}+)")
                    all_good = False
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            all_good = False
    
    return all_good

def test_python_syntax():
    """Test that Python files have valid syntax."""
    print("\n🐍 Testing Python syntax...")
    
    python_files = [
        "ai_hackathon_2025/__init__.py",
        "ai_hackathon_2025/main.py",
        "setup.py",
        "test_all.py",
        "tests/test_setup.py",
        "tests/test_integration.py"
    ]
    
    all_good = True
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Try to compile the code
            compile(source_code, file_path, 'exec')
            print(f"✅ {file_path}")
        except SyntaxError as e:
            print(f"❌ Syntax error in {file_path}: {e}")
            all_good = False
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
            all_good = False
    
    return all_good

def test_package_info():
    """Test package information without importing."""
    print("\n📦 Testing package information...")
    
    try:
        # Check __init__.py has version info
        with open("ai_hackathon_2025/__init__.py", 'r') as f:
            init_content = f.read()
        
        if '__version__' in init_content:
            print("✅ Package version defined")
        else:
            print("⚠️ Package version not found")
            
        if '__author__' in init_content:
            print("✅ Package author defined")
        else:
            print("⚠️ Package author not found")
            
        # Check setup.py has proper configuration
        with open("setup.py", 'r') as f:
            setup_content = f.read()
            
        if 'name="autoblography"' in setup_content:
            print("✅ Package name configured")
        else:
            print("⚠️ Package name not found in setup.py")
            
        if 'entry_points' in setup_content:
            print("✅ Console script entry point configured")
        else:
            print("⚠️ Console script entry point not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking package info: {e}")
        return False

def test_documentation_quality():
    """Test documentation quality."""
    print("\n📚 Testing documentation quality...")
    
    docs_to_check = [
        ("README.md", ["# ", "## ", "```", "Installation", "Usage"]),
        ("docs/SETUP.md", ["# ", "## ", "Prerequisites", "Setup"]),
        ("examples/EXAMPLES.md", ["# ", "## ", "Example", "```"]),
        ("CHANGELOG.md", ["# ", "## ", "[1.0.0]", "Added"])
    ]
    
    all_good = True
    for doc_path, required_elements in docs_to_check:
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"⚠️ {doc_path} missing: {missing_elements}")
                all_good = False
            else:
                print(f"✅ {doc_path}")
                
        except Exception as e:
            print(f"❌ Error checking {doc_path}: {e}")
            all_good = False
    
    return all_good

def main():
    """Run all structure tests."""
    print("🧪 Autoblography Structure Test (No Dependencies)")
    print("=" * 60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("File Contents", test_file_contents),
        ("Python Syntax", test_python_syntax),
        ("Package Info", test_package_info),
        ("Documentation Quality", test_documentation_quality)
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
    print("\n" + "=" * 60)
    print("📊 STRUCTURE TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} structure tests passed")
    
    if passed == total:
        print("\n🎉 All structure tests passed!")
        print("\n📋 Your project structure is correctly organized!")
        print("\n🚀 Next steps to test functionality:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run full tests: python test_all.py")
        print("3. Set up credentials and test with real data")
        
        return True
    else:
        print(f"\n⚠️ {total - passed} structure tests failed.")
        print("Fix the issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)