#!/usr/bin/env python3
"""
Test runner for Autoblography.
Runs all tests to verify the project is working correctly.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Run all tests."""
    print("🧪 Autoblography Test Runner")
    print("=" * 60)
    
    # Run setup tests
    print("\n1️⃣ Running Setup Tests...")
    print("-" * 30)
    
    try:
        from tests.test_setup import run_all_tests as run_setup_tests
        setup_success = run_setup_tests()
    except Exception as e:
        print(f"❌ Setup tests failed to run: {e}")
        setup_success = False
    
    # Run integration tests
    print("\n2️⃣ Running Integration Tests...")
    print("-" * 30)
    
    try:
        from tests.test_integration import run_integration_tests
        integration_success = run_integration_tests()
    except Exception as e:
        print(f"❌ Integration tests failed to run: {e}")
        integration_success = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST SUMMARY")
    print("=" * 60)
    
    if setup_success and integration_success:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour Autoblography project is ready to use!")
        print("\n📋 Next Steps:")
        print("1. Set up your .env file with actual credentials")
        print("2. Test with real data:")
        print("   python -m ai_hackathon_2025.main --source slack --input 'your-slack-url'")
        print("   python -m ai_hackathon_2025.main --source gdoc --input 'your-doc-url'")
        print("\n📚 Documentation:")
        print("- README.md - Project overview")
        print("- docs/SETUP.md - Detailed setup guide")
        print("- examples/EXAMPLES.md - Usage examples")
        
        return True
    else:
        print("❌ SOME TESTS FAILED")
        if not setup_success:
            print("- Setup tests failed - check project structure and dependencies")
        if not integration_success:
            print("- Integration tests failed - check core functionality")
        
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all files are in the correct locations")
        print("3. Review error messages above for specific issues")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)