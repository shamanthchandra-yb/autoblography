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

# Store generated files temporarily
generated_files = {}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

class LogCapture:
    """Capture stdout/stderr to capture internal progress logs"""
    def __init__(self):
        self.logs = []
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def write(self, text):
        if text.strip():  # Only capture non-empty lines
            self.logs.append(text.strip())
        self.original_stdout.write(text)
    
    def flush(self):
        self.original_stdout.flush()

@app.post("/generate-blog-simple")
async def generate_blog_simple(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with internal progress logging"""
    
    # Validate environment variables
    if not settings.validate():
        return JSONResponse(
            status_code=500,
            content={"error": "Server configuration error. Please check environment variables."}
        )
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid Slack URL format"}
        )
    elif source_type == "gdoc" and "docs.google.com" not in url:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid Google Doc URL format"}
        )
    
    try:
        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())
        
        # Capture all internal logs during blog generation
        with LogCapture() as log_capture:
            # Initialize blog generator
            generator = BlogGenerator()
            
            # Generate blog
            if source_type == "slack":
                output_file = generator.generate_from_slack(url)
            else:
                output_file = generator.generate_from_google_doc(url)
        
        if not output_file or not os.path.exists(output_file):
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to generate blog post"}
            )
        
        # Store the file info for download
        generated_files[request_id] = {
            "file_path": output_file,
            "filename": os.path.basename(output_file),
            "size": os.path.getsize(output_file),
            "created_at": time.time()
        }
        
        return JSONResponse(content={
            "success": True,
            "message": "Blog generated successfully!",
            "download_url": f"/download/{request_id}",
            "filename": os.path.basename(output_file),
            "size_kb": round(os.path.getsize(output_file) / 1024, 1),
            "logs": log_capture.logs  # Include all captured progress logs
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Blog generation failed: {str(e)}"}
        )

@app.post("/generate-blog-with-progress")
async def generate_blog_with_progress(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with real-time internal progress logging"""
    
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
            
            # Capture logs in real-time
            log_buffer = []
            
            # Override print function to capture logs
            original_print = print
            def capture_print(*args, **kwargs):
                message = " ".join(str(arg) for arg in args)
                log_buffer.append(message)
                original_print(*args, **kwargs)
            
            # Replace print function temporarily
            import builtins
            builtins.print = capture_print
            
            try:
                # Initialize blog generator
                generator = BlogGenerator()
                yield f"data: Initializing blog generator...\n\n"
                
                # Generate blog
                if source_type == "slack":
                    yield f"data: Processing Slack thread: {url}\n\n"
                    output_file = generator.generate_from_slack(url)
                    result = {"output_file": output_file} if output_file else None
                else:
                    yield f"data: Processing Google Doc: {url}\n\n"
                    output_file = generator.generate_from_google_doc(url)
                    result = {"output_file": output_file} if output_file else None
                
                # Yield all captured logs
                for log in log_buffer:
                    yield f"data: {log}\n\n"
                
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
                
            finally:
                # Restore original print function
                builtins.print = original_print
            
        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"
    
    return StreamingResponse(
        generate_with_progress(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/download/{request_id}")
async def download_file(request_id: str):
    """Download a generated file by request ID"""
    if request_id not in generated_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = generated_files[request_id]
    file_path = file_info["file_path"]
    
    if not os.path.exists(file_path):
        # Clean up invalid entry
        del generated_files[request_id]
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_info["filename"],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.post("/generate-blog")
async def generate_blog(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post from Slack thread or Google Doc with real-time internal progress logging"""
    
    # Validate environment variables
    if not settings.validate():
        raise HTTPException(status_code=500, detail="Server configuration error. Please check environment variables.")
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Slack URL format")
    elif source_type == "gdoc" and "docs.google.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Google Doc URL format")
    
    async def generate_with_logging():
        """Generator function to yield progress updates and then the file"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            yield f"[{timestamp}] ℹ️ Starting AutoBlography blog generation\n"
            yield f"[{timestamp}] ℹ️ URL: {url}\n"
            yield f"[{timestamp}] ℹ️ Source Type: {source_type}\n"
            
            # Initialize blog generator
            timestamp = time.strftime("%H:%M:%S")
            yield f"[{timestamp}] 🔄 Initializing blog generator...\n"
            generator = BlogGenerator()
            
            # Generate blog with detailed logging
            if source_type == "slack":
                timestamp = time.strftime("%H:%M:%S")
                yield f"[{timestamp}] 🔄 Processing Slack thread...\n"
                
                # Capture logs during generation
                import io
                import sys
                
                # Redirect stdout to capture logs
                old_stdout = sys.stdout
                captured_output = io.StringIO()
                sys.stdout = captured_output
                
                try:
                    output_file = generator.generate_from_slack(url)
                    result = {"output_file": output_file} if output_file else None
                finally:
                    # Restore stdout
                    sys.stdout = old_stdout
                    captured_logs = captured_output.getvalue()
                
                # Yield captured logs line by line
                for line in captured_logs.split('\n'):
                    if line.strip():
                        timestamp = time.strftime("%H:%M:%S")
                        yield f"[{timestamp}] 📝 {line.strip()}\n"
                
            else:
                timestamp = time.strftime("%H:%M:%S")
                yield f"[{timestamp}] 🔄 Processing Google Doc...\n"
                
                # Capture logs during generation
                import io
                import sys
                
                # Redirect stdout to capture logs
                old_stdout = sys.stdout
                captured_output = io.StringIO()
                sys.stdout = captured_output
                
                try:
                    output_file = generator.generate_from_google_doc(url)
                    result = {"output_file": output_file} if output_file else None
                finally:
                    # Restore stdout
                    sys.stdout = old_stdout
                    captured_logs = captured_output.getvalue()
                
                # Yield captured logs line by line
                for line in captured_logs.split('\n'):
                    if line.strip():
                        timestamp = time.strftime("%H:%M:%S")
                        yield f"[{timestamp}] 📝 {line.strip()}\n"
            
            if not result:
                timestamp = time.strftime("%H:%M:%S")
                yield f"[{timestamp}] ❌ Failed to generate blog post\n"
                return
            
            # Get the generated file path
            output_file = result.get("output_file")
            if not output_file or not os.path.exists(output_file):
                timestamp = time.strftime("%H:%M:%S")
                yield f"[{timestamp}] ❌ Generated file not found\n"
                return
            
            timestamp = time.strftime("%H:%M:%S")
            yield f"[{timestamp}] ✅ Blog generation completed successfully!\n"
            yield f"[{timestamp}] 📄 Output file: {os.path.basename(output_file)}\n"
            yield f"[{timestamp}] 📊 File size: {os.path.getsize(output_file) / 1024:.0f}KB\n"
            yield f"[{timestamp}] 🎉 Ready for download!\n"
            
            # Now yield the file content
            with open(output_file, 'rb') as f:
                while chunk := f.read(8192):
                    yield chunk
            
        except Exception as e:
            timestamp = time.strftime("%H:%M:%S")
            yield f"[{timestamp}] ❌ Error: {str(e)}\n"
    
    return StreamingResponse(
        generate_with_logging(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename=blog_{int(time.time())}.docx",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.post("/generate-blog-with-logs")
async def generate_blog_with_logs(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with real-time logging (text only)"""
    
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

@app.post("/generate-blog-live")
async def generate_blog_live(url: str = Form(...), source_type: str = Form(...)):
    """Generate a blog post with real-time live logging that shows progress during curl execution"""
    
    # Validate environment variables
    if not settings.validate():
        raise HTTPException(status_code=500, detail="Server configuration error. Please check environment variables.")
    
    # Validate URL format
    if source_type == "slack" and "slack.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Slack URL format")
    elif source_type == "gdoc" and "docs.google.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid Google Doc URL format")
    
    async def generate_with_live_logging():
        """Generator function to yield live progress updates"""
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
                
                # We'll capture logs in real-time by overriding print temporarily
                import io
                import sys
                from contextlib import redirect_stdout
                
                # Create a custom stdout that yields immediately
                class LiveLogger:
                    def __init__(self, generator_func):
                        self.generator_func = generator_func
                        self.buffer = ""
                    
                    def write(self, text):
                        self.buffer += text
                        if '\n' in self.buffer:
                            lines = self.buffer.split('\n')
                            self.buffer = lines[-1]  # Keep incomplete line
                            for line in lines[:-1]:
                                if line.strip():
                                    # We can't yield from here, so we'll store it
                                    pass
                    
                    def flush(self):
                        if self.buffer.strip():
                            # We can't yield from here, so we'll store it
                            pass
                
                # For now, let's use a simpler approach - capture and yield in batches
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
            
            yield f"✅ Blog generation completed successfully!\n"
            yield f"📄 Output file: {os.path.basename(output_file)}\n"
            yield f"📊 File size: {os.path.getsize(output_file) / 1024:.0f}KB\n"
            yield f"🎉 Ready for download!\n"
            yield f"🔗 Download URL: /download/{output_file}\n"
            
        except Exception as e:
            yield f"❌ Error: {str(e)}\n"
    
    return StreamingResponse(
        generate_with_live_logging(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 