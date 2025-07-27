# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    binutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional web dependencies
RUN pip install --no-cache-dir fastapi uvicorn python-multipart jinja2

# Copy the application code
COPY . .

# Install the autoblography package in development mode
RUN pip install -e .

# Create necessary directories
RUN mkdir -p output images credentials

# Set proper permissions
RUN chmod 755 output images credentials

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"] 