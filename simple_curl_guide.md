# Simple Curl Usage Guide

## 🚀 Generate Blog with Simple Curl Commands

### Step 1: Generate the Blog
```bash
curl -X POST http://localhost:8000/generate-blog-simple \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack"
```

**Response:**
```json
{
  "success": true,
  "message": "Blog generated successfully!",
  "download_url": "/download/66e688b4-b002-42a6-8307-e3d72d45ba21",
  "filename": "blog_post_20250727_151044.docx",
  "size_kb": 791.2
}
```

### Step 2: Download the File
```bash
curl -X GET http://localhost:8000/download/66e688b4-b002-42a6-8307-e3d72d45ba21 \
  --output my_blog.docx
```

## 📝 Complete Example

### For Slack Thread:
```bash
# Generate blog
RESPONSE=$(curl -s -X POST http://localhost:8000/generate-blog-simple \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack")

# Extract download URL
DOWNLOAD_URL=$(echo $RESPONSE | grep -o '"/download/[^"]*"' | tr -d '"')

# Download file
curl -X GET http://localhost:8000$DOWNLOAD_URL --output blog.docx
```

### For Google Doc:
```bash
# Generate blog
RESPONSE=$(curl -s -X POST http://localhost:8000/generate-blog-simple \
  -F "url=https://docs.google.com/document/d/1ABC123XYZ/edit" \
  -F "source_type=gdoc")

# Extract download URL
DOWNLOAD_URL=$(echo $RESPONSE | grep -o '"/download/[^"]*"' | tr -d '"')

# Download file
curl -X GET http://localhost:8000$DOWNLOAD_URL --output blog.docx
```

## 🔧 One-Liner Script

### For Slack:
```bash
RESPONSE=$(curl -s -X POST http://localhost:8000/generate-blog-simple -F "url=YOUR_SLACK_URL" -F "source_type=slack") && curl -X GET http://localhost:8000$(echo $RESPONSE | grep -o '"/download/[^"]*"' | tr -d '"') --output blog.docx
```

### For Google Doc:
```bash
RESPONSE=$(curl -s -X POST http://localhost:8000/generate-blog-simple -F "url=YOUR_GDOC_URL" -F "source_type=gdoc") && curl -X GET http://localhost:8000$(echo $RESPONSE | grep -o '"/download/[^"]*"' | tr -d '"') --output blog.docx
```

## 📋 What You Get

- **Step 1**: JSON response with success status and download link
- **Step 2**: Direct file download (.docx format)
- **File**: Ready-to-use Word document with embedded images

## 🎯 Usage Tips

1. **Replace URLs**: Just change the URL in the curl command
2. **Custom Filename**: Change `--output blog.docx` to your preferred name
3. **Error Handling**: Check the JSON response for error messages
4. **File Size**: The response shows the file size in KB

## ❌ Error Examples

**Invalid URL:**
```json
{"error": "Invalid Slack URL format"}
```

**Server Error:**
```json
{"error": "Server configuration error. Please check environment variables."}
```

---

**That's it! Simple curl commands with no scripts needed.** 🎉 