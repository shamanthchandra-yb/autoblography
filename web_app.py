#!/usr/bin/env python3
"""
Simple FastAPI web service for AutoBlography
"""

import os
import time
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv("test.env")

from autoblography import BlogGenerator
from autoblography.config.settings import settings


# Initialize FastAPI app
app = FastAPI(
    title="AutoBlography Web Service",
    description="AI-powered blog generation from Slack threads and Google Docs",
    version="1.0.0"
)

# Create templates directory and HTML template
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Create simple HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>AutoBlography - Blog Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="url"], select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .status { margin-top: 20px; padding: 10px; border-radius: 4px; }
        .status.processing { background: #fff3cd; border: 1px solid #ffeaa7; }
        .status.success { background: #d4edda; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; border: 1px solid #f5c6cb; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <h1>🚀 AutoBlography</h1>
    <p>Generate AI-powered blogs from Slack threads or Google Docs</p>
    
    <form id="blogForm" action="/generate-blog" method="post">
        <div class="form-group">
            <label for="url">URL:</label>
            <input type="url" id="url" name="url" required 
                   placeholder="https://company.slack.com/archives/C1234567/p1234567890123456 or https://docs.google.com/document/d/1ABC123XYZ/edit">
        </div>
        
        <div class="form-group">
            <label for="source_type">Source Type:</label>
            <select id="source_type" name="source_type" required>
                <option value="slack">Slack Thread</option>
                <option value="gdoc">Google Doc</option>
            </select>
        </div>
        
        <button type="submit" id="submitBtn">Generate Blog</button>
    </form>
    
    <div id="status" class="status hidden"></div>
    
    <script>
        document.getElementById('blogForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const status = document.getElementById('status');
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Generating...';
            status.className = 'status processing';
            status.textContent = '🚀 Starting blog generation... This may take a few minutes.';
            status.classList.remove('hidden');
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/generate-blog', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'generated_blog.docx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    status.className = 'status success';
                    status.textContent = '✅ Blog generated successfully! Download started.';
                } else {
                    const errorText = await response.text();
                    status.className = 'status error';
                    status.textContent = '❌ Error: ' + errorText;
                }
            } catch (error) {
                status.className = 'status error';
                status.textContent = '❌ Network error: ' + error.message;
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Generate Blog';
            }
        });
    </script>
</body>
</html>
"""

# Write the HTML template
with open(templates_dir / "index.html", "w") as f:
    f.write(html_template)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-blog")
async def generate_blog(
    url: str = Form(...),
    source_type: str = Form(...)
):
    """
    Generate a blog from Slack thread or Google Doc URL
    
    Args:
        url: Slack thread URL or Google Doc URL
        source_type: 'slack' or 'gdoc'
    
    Returns:
        Generated blog file as download
    """
    try:
        # Validate settings
        if not settings.validate():
            raise HTTPException(
                status_code=500, 
                detail="Server configuration error. Please check environment variables."
            )
        
        # Validate source type
        if source_type not in ['slack', 'gdoc']:
            raise HTTPException(
                status_code=400, 
                detail="Invalid source_type. Must be 'slack' or 'gdoc'"
            )
        
        # Validate URL format
        if source_type == 'slack' and 'slack.com' not in url:
            raise HTTPException(
                status_code=400, 
                detail="Invalid Slack URL format"
            )
        elif source_type == 'gdoc' and 'docs.google.com' not in url:
            raise HTTPException(
                status_code=400, 
                detail="Invalid Google Doc URL format"
            )
        
        # Initialize blog generator
        generator = BlogGenerator()
        
        # Generate blog based on source type
        if source_type == 'slack':
            output_file = generator.generate_from_slack(url)
        else:  # gdoc
            output_file = generator.generate_from_google_doc(url)
        
        if not output_file or not os.path.exists(output_file):
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate blog. Please check the URL and try again."
            )
        
        # Return the generated file
        return FileResponse(
            path=output_file,
            filename=f"blog_{int(time.time())}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error generating blog: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Blog generation failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 