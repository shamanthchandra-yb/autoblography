# Simple cURL Guide for AutoBlography

This guide shows you how to generate blogs using simple `curl` commands.

## Method 1: Live Progress Logging (Recommended)

Use this method to see real-time progress logs during blog generation:

```bash
# Generate blog with live progress logs
curl -X POST http://localhost:8000/generate-blog-live \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack"
```

This will show you live progress like:
- 🚀 Starting Slack blog generation pipeline...
- Fetching thread from Channel ID: C017TTZ9EV7...
- ✅ Successfully fetched 17 messages from the thread.
- 🤖 Processing Slack conversation...
- ✅ Cleaning Complete!
- And more...

## Method 2: Two-Step Process

### Step 1: Generate the blog
```bash
# Generate blog and get download link
curl -X POST http://localhost:8000/generate-blog-simple \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack"
```

This returns a JSON response with a download URL:
```json
{
  "success": true,
  "message": "Blog generated successfully!",
  "download_url": "/download/3608ab0c-1e49-4c46-9119-ca0b605a8410",
  "filename": "blog_post_20250727_151644.docx",
  "size_kb": 1300.9,
  "logs": ["🚀 Starting Slack blog generation pipeline...", "✅ Successfully fetched 17 messages...", ...]
}
```

### Step 2: Download the file
```bash
# Download the generated blog
curl -O http://localhost:8000/download/3608ab0c-1e49-4c46-9119-ca0b605a8410
```

## Method 3: Direct Download

Generate and download in one command:
```bash
# Generate and download directly
curl -X POST http://localhost:8000/generate-blog \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack" \
  --output my_blog.docx
```

## URL Examples

### Slack Thread
```bash
curl -X POST http://localhost:8000/generate-blog-live \
  -F "url=https://yugabyte.slack.com/archives/C017TTZ9EV7/p1743650463482219" \
  -F "source_type=slack"
```

### Google Doc
```bash
curl -X POST http://localhost:8000/generate-blog-live \
  -F "url=https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit" \
  -F "source_type=gdoc"
```

## Prerequisites

- **Slack**: The Slack app must be added to the channel containing the thread
- **Google Doc**: You must have permission to access the Google Doc
- **Environment Variables**: All required API keys must be configured on the server

## Notes

- The live logging endpoint (`/generate-blog-live`) is recommended for seeing real-time progress
- Blog generation typically takes 2-3 minutes
- Generated files are Word documents (.docx) with embedded images
- The server automatically cleans up old files periodically 