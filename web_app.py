#!/usr/bin/env python3
"""
Simple FastAPI web service for AutoBlography
"""

import os
import time
import tempfile
from pathlib import Path
from typing import Optional
import logging

from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
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
    """Generate a blog post from Slack thread or Google Doc"""
    
    # Validate environment variables
    if not settings.validate():
        raise HTTPException(status_code=500, detail="Server configuration error. Please check environment variables.")
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Slack URL format")
    elif source_type == "gdoc" and "docs.google.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Google Doc URL format")
    
    try:
        logger.info(f"Starting blog generation for {source_type}: {url}")
        
        # Initialize blog generator
        generator = BlogGenerator()
        
        # Generate blog with detailed logging
        logger.info("Initializing blog generator...")
        
        if source_type == "slack":
            logger.info("Processing Slack thread...")
            output_file = generator.generate_from_slack(url)
            result = {"output_file": output_file} if output_file else None
        else:
            logger.info("Processing Google Doc...")
            output_file = generator.generate_from_google_doc(url)
            result = {"output_file": output_file} if output_file else None
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to generate blog post")
        
        # Get the generated file path
        output_file = result.get("output_file")
        if not output_file or not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Generated file not found")
        
        logger.info(f"Blog generation completed successfully: {output_file}")
        
        # Return the file for download
        return FileResponse(
            path=output_file,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=os.path.basename(output_file)
        )
        
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Blog generation failed: {str(e)}")

@app.post("/generate-blog-with-logs")
async def generate_blog_with_logs(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with real-time logging"""
    
    # Validate environment variables
    if not settings.validate():
        raise HTTPException(status_code=500, detail="Server configuration error. Please check environment variables.")
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Slack URL format")
    elif source_type == "gdoc" and "docs.google.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Google Doc URL format")
    
    async def generate_with_progress():
        """Generator function to yield progress updates"""
        try:
            yield f"data: Starting blog generation for {source_type}...\n\n"
            
            # Initialize blog generator
            generator = BlogGenerator()
            yield f"data: Initializing blog generator...\n\n"
            
            if source_type == "slack":
                yield f"data: Processing Slack thread: {url}\n\n"
                output_file = generator.generate_from_slack(url)
                result = {"output_file": output_file} if output_file else None
            else:
                yield f"data: Processing Google Doc: {url}\n\n"
                output_file = generator.generate_from_google_doc(url)
                result = {"output_file": output_file} if output_file else None
            
            if not result:
                yield f"data: ERROR: Failed to generate blog post\n\n"
                return
            
            # Get the generated file path
            output_file = result.get("output_file")
            if not output_file or not os.path.exists(output_file):
                yield f"data: ERROR: Generated file not found\n\n"
                return
            
            yield f"data: SUCCESS: Blog generation completed! File: {os.path.basename(output_file)}\n\n"
            yield f"data: DOWNLOAD: {output_file}\n\n"
            
        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"
    
    return StreamingResponse(
        generate_with_progress(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 