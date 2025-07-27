# 🧪 Testing Guide for Autoblography

This guide explains how to test your Autoblography project at different levels to ensure everything is working correctly after the restructuring.

## 🎯 Testing Levels

### 1. **Structure Tests** (No Dependencies Required)
Tests project organization, file structure, and basic syntax.

```bash
python3 test_structure_only.py
```

**What it checks:**
- ✅ All required files and directories exist
- ✅ Files have appropriate content length
- ✅ Python syntax is valid
- ✅ Package information is configured
- ✅ Documentation quality

### 2. **Setup Tests** (Requires Dependencies)
Tests that dependencies are installed and modules can be imported.

```bash
python3 tests/test_setup.py
```

**What it checks:**
- ✅ Python version compatibility
- ✅ Package structure
- ✅ Module imports
- ✅ Dependencies availability
- ✅ CLI interface
- ✅ Environment setup
- ✅ Documentation

### 3. **Integration Tests** (Mock Testing)
Tests core functionality using mock data (no real API calls).

```bash
python3 tests/test_integration.py
```

**What it checks:**
- ✅ Slack URL parsing
- ✅ Google Doc ID extraction
- ✅ Blog generation pipeline (mocked)
- ✅ Image generation pipeline (mocked)
- ✅ CLI help functionality
- ✅ Prompt constants loading

### 4. **Full Test Suite**
Runs all tests in sequence.

```bash
python3 test_all.py
```

## 🚀 Quick Testing Workflow

### Step 1: Structure Test (Always Run First)
```bash
# This works without any dependencies
python3 test_structure_only.py
```
**Expected Result:** All 5 tests should pass ✅

### Step 2: Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Full Test Suite
```bash
# Run all tests
python3 test_all.py
```

## 🔧 Testing Without Full Setup

If you don't have Google Cloud credentials set up yet, you can still test most functionality:

### Basic Functionality Test
```bash
# Test CLI help (should work without credentials)
python3 -m ai_hackathon_2025.main --help
```

### Import Test
```python
# Test basic imports
python3 -c "
import ai_hackathon_2025
print('✅ Package imported successfully')
print(f'Version: {ai_hackathon_2025.__version__}')
"
```

## 🧪 Manual Testing Scenarios

### 1. **Test Slack URL Parsing**
```python
from ai_hackathon_2025.slack_app import SlackApp

app = SlackApp()
url = "https://workspace.slack.com/archives/C1234567/p1234567890123456"
channel_id, thread_ts = app._parse_permalink(url)
print(f"Channel: {channel_id}, Timestamp: {thread_ts}")
# Expected: Channel: C1234567, Timestamp: 1234567890.123456
```

### 2. **Test Google Doc ID Extraction**
```python
from ai_hackathon_2025.google_document_reader import extract_doc_id_from_url

doc_url = "https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
doc_id = extract_doc_id_from_url(doc_url)
print(f"Document ID: {doc_id}")
# Expected: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

### 3. **Test CLI Interface**
```bash
# Test help
python3 -m ai_hackathon_2025.main --help

# Test with invalid arguments (should show error)
python3 -m ai_hackathon_2025.main --source invalid --input test
```

## 🔍 Testing with Real Data

Once you have credentials set up:

### Environment Setup
```bash
# Create .env file
cat > .env << EOF
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCLOUD_PROJECT=your-project-id
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
EOF
```

### Test with Real Slack Thread
```bash
python3 -m ai_hackathon_2025.main \
  --source slack \
  --input "https://your-workspace.slack.com/archives/CHANNEL/pTIMESTAMP"
```

### Test with Real Google Doc
```bash
python3 -m ai_hackathon_2025.main \
  --source gdoc \
  --input "https://docs.google.com/document/d/YOUR_DOC_ID"
```

## 🐛 Troubleshooting Tests

### Common Issues and Solutions

#### 1. **Import Errors**
```
ModuleNotFoundError: No module named 'langchain_google_vertexai'
```
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

#### 2. **Permission Errors**
```
PermissionError: [Errno 13] Permission denied
```
**Solution:** Make scripts executable
```bash
chmod +x test_all.py tests/*.py scripts/*.sh
```

#### 3. **Virtual Environment Issues**
```
The virtual environment was not created successfully
```
**Solution:** Install venv package
```bash
# On Ubuntu/Debian
sudo apt install python3-venv

# On other systems, try
python3 -m pip install --user virtualenv
```

#### 4. **Google Cloud Authentication**
```
Could not automatically determine credentials
```
**Solution:** Set up service account
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### 5. **Slack Token Issues**
```
Invalid token
```
**Solution:** Check token format and permissions
- Token should start with `xoxb-`
- Bot needs required permissions in Slack app settings

## 📊 Understanding Test Results

### Test Status Indicators
- ✅ **PASS**: Test completed successfully
- ❌ **FAIL**: Test failed, needs attention
- ⚠️ **WARNING**: Test passed but with concerns

### What Each Test Validates

#### Structure Tests
- File organization matches expected layout
- All required files are present
- Python syntax is valid
- Documentation exists and is structured

#### Setup Tests
- Dependencies are installed correctly
- Modules can be imported without errors
- CLI interface is functional
- Environment can be configured

#### Integration Tests
- Core logic works with mock data
- URL parsing functions correctly
- AI pipeline can be instantiated
- Error handling works properly

## 🎯 Test Coverage

### Currently Tested ✅
- Project structure and organization
- Python syntax validation
- Module imports and dependencies
- CLI interface functionality
- URL parsing logic
- Mock AI pipeline execution
- Documentation completeness

### Not Yet Tested ⏳
- Real API calls to Google Cloud
- Actual Slack API integration
- End-to-end blog generation
- Image generation with real prompts
- Error handling with real failures

## 🚀 Continuous Testing

### Before Committing Changes
```bash
# Always run structure test first
python3 test_structure_only.py

# If you have dependencies installed
python3 test_all.py
```

### Before Deploying
```bash
# Full test with real credentials
python3 test_all.py

# Test with sample data
python3 -m ai_hackathon_2025.main --source gdoc --input "sample-doc-id"
```

### Performance Testing
```bash
# Time the execution
time python3 -m ai_hackathon_2025.main --source slack --input "slack-url"
```

---

## 📝 Test Results Interpretation

### All Tests Passing 🎉
Your project is ready for:
- Development and customization
- Real-world testing with credentials
- Demonstration to stakeholders
- Deployment and distribution

### Some Tests Failing ⚠️
Check the specific error messages and:
1. Fix structural issues first
2. Install missing dependencies
3. Verify file permissions
4. Check Python syntax errors

### Most Tests Failing ❌
Likely issues:
- Dependencies not installed
- Files in wrong locations
- Python version incompatibility
- Missing environment setup

---

*This testing guide ensures your Autoblography project is robust and ready for production use. Start with structure tests and progressively move to more complex testing scenarios.*