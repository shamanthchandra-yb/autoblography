#!/usr/bin/env python3
"""
Simple FastAPI web service for AutoBlography
"""

import os
import time
import tempfile
import uuid
import io
import sys
import json
from pathlib import Path
from typing import Optional
import logging

from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv("test.env")

from autoblography import BlogGenerator
from autoblography.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AutoBlography", description="AI Blog Generator from Slack threads and Google Docs")

# Mount static files and templates
templates = Jinja2Templates(directory="templates")

# Persistent file storage
STORAGE_FILE = "generated_files.json"

def load_generated_files():
    """Load generated files from persistent storage"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_generated_files(files):
    """Save generated files to persistent storage"""
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(files, f)
    except Exception as e:
        logger.error(f"Failed to save generated files: {e}")

# Initialize generated files from storage
generated_files = load_generated_files()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/generate-blog")
async def generate_blog(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with real-time progress logs and provide download link"""
    
    # Validate environment variables
    if not settings.validate():
        raise HTTPException(status_code=500, detail="Server configuration error. Please check environment variables.")
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Slack URL format")
    elif source_type == "gdoc" and "docs.google.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Google Doc URL format")
    
    async def generate_with_logging():
        """Generator function to yield progress updates"""
        try:
            yield f"🚀 Starting AutoBlography blog generation...\n"
            yield f"📝 URL: {url}\n"
            yield f"📝 Source Type: {source_type}\n"
            yield f"⏳ Initializing blog generator...\n"
            
            # Initialize blog generator
            generator = BlogGenerator()
            
            # Generate blog with live logging
            if source_type == "slack":
                yield f"🔄 Processing Slack thread...\n"
                
                # Capture logs during generation
                import io
                from contextlib import redirect_stdout
                
                captured_output = io.StringIO()
                
                with redirect_stdout(captured_output):
                    output_file = generator.generate_from_slack(url)
                    result = {"output_file": output_file} if output_file else None
                
                # Yield captured logs
                logs = captured_output.getvalue()
                for line in logs.split('\n'):
                    if line.strip():
                        yield f"📝 {line.strip()}\n"
                
            else:
                yield f"🔄 Processing Google Doc...\n"
                
                # Capture logs during generation
                import io
                from contextlib import redirect_stdout
                
                captured_output = io.StringIO()
                
                with redirect_stdout(captured_output):
                    output_file = generator.generate_from_google_doc(url)
                    result = {"output_file": output_file} if output_file else None
                
                # Yield captured logs
                logs = captured_output.getvalue()
                for line in logs.split('\n'):
                    if line.strip():
                        yield f"📝 {line.strip()}\n"
            
            if not result:
                yield f"❌ Failed to generate blog post\n"
                return
            
            # Get the generated file path
            output_file = result.get("output_file")
            if not output_file or not os.path.exists(output_file):
                yield f"❌ Generated file not found\n"
                return
            
            # Generate a unique ID for this file
            file_id = str(uuid.uuid4())
            generated_files[file_id] = {
                "file_path": output_file,
                "filename": os.path.basename(output_file),
                "size": os.path.getsize(output_file),
                "created_at": time.time()
            }
            
            # Save to persistent storage
            save_generated_files(generated_files)
            
            yield f"✅ Blog generation completed successfully!\n"
            yield f"📄 Output file: {os.path.basename(output_file)}\n"
            yield f"📊 File size: {os.path.getsize(output_file) / 1024:.0f}KB\n"
            yield f"🎉 Download your blog here:\n"
            yield f"🔗 curl -X GET http://localhost:8000/download/{file_id} --output {os.path.basename(output_file)}\n"
            
        except Exception as e:
            yield f"❌ Error: {str(e)}\n"
    
    return StreamingResponse(
        generate_with_logging(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """Download a generated file by file ID"""
    if file_id not in generated_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = generated_files[file_id]
    file_path = file_info["file_path"]
    
    if not os.path.exists(file_path):
        # Clean up invalid entry
        del generated_files[file_id]
        save_generated_files(generated_files)
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_info["filename"],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=True) 