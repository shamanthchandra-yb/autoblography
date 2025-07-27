# AutoBlography Web Service Deployment Guide

## 🚀 Quick Deployment

### Prerequisites
- Docker and Docker Compose installed on your VM
- Google Cloud service account credentials file
- Environment variables configured

### Step 1: Prepare Environment Variables

Create a `.env` file in the project root:

```bash
# Slack Configuration
SLACK_TOKEN=xoxb-your-slack-token-here

# Google Cloud Configuration
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_LOCATION=us-central1

# Kapa AI Configuration
KAPA_API_KEY=your-kapa-api-key

# AI Configuration
VERTEX_AI_MODEL=gemini-2.0-flash-001
```

### Step 2: Prepare Credentials

Copy your Google Cloud service account JSON file to the project root and rename it to `credentials.json`:

```bash
cp /path/to/your/service-account-key.json ./credentials.json
```

### Step 3: Deploy with Docker Compose

```bash
# Build and start the service
docker-compose up -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 4: Access the Web Interface

Open your browser and go to: `http://your-vm-ip:8000`

## 🔧 Manual Deployment

### Option 1: Direct Python

```bash
# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn python-multipart jinja2

# Set environment variables
export SLACK_TOKEN="your-token"
export GOOGLE_PROJECT_ID="your-project"
export KAPA_API_KEY="your-key"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Run the service
python web_app.py
```

### Option 2: Docker Only

```bash
# Build the image
docker build -t autoblography-web .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e SLACK_TOKEN="your-token" \
  -e GOOGLE_PROJECT_ID="your-project" \
  -e KAPA_API_KEY="your-key" \
  -v /path/to/credentials.json:/app/credentials.json:ro \
  -v ./output:/app/output \
  -v ./images:/app/images \
  --name autoblography-web \
  autoblography-web
```

## 📋 API Endpoints

### Web Interface
- `GET /` - Main web interface

### API Endpoints
- `POST /generate-blog` - Generate blog from URL
  - Parameters: `url` (string), `source_type` (slack|gdoc)
  - Returns: Generated blog file

- `GET /health` - Health check endpoint
  - Returns: `{"status": "healthy", "timestamp": 1234567890}`

## 🔍 Monitoring

### Check Service Status
```bash
# Health check
curl http://localhost:8000/health

# View logs
docker-compose logs -f autoblography-web
```

### View Generated Files
```bash
# List generated blogs
ls -la output/

# List generated images
ls -la images/
```

## 🛠️ Troubleshooting

### Common Issues

1. **Environment Variables Not Set**
   - Check `.env` file exists and has correct values
   - Verify credentials.json is in the right location

2. **Port Already in Use**
   - Change port in docker-compose.yml: `"8001:8000"`

3. **Permission Issues**
   - Ensure output and images directories are writable
   - Check credentials.json file permissions

4. **Service Won't Start**
   - Check logs: `docker-compose logs autoblography-web`
   - Verify all environment variables are set

### Logs and Debugging

```bash
# View real-time logs
docker-compose logs -f

# Check container status
docker-compose ps

# Restart service
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

## 🔒 Security Notes

- The service runs without authentication (internal network only)
- Generated files are stored locally on the VM
- Consider adding a reverse proxy (nginx) for production use
- Set up firewall rules to restrict access to company IPs only

## 📈 Scaling

For multiple users, consider:
- Adding a reverse proxy with rate limiting
- Implementing a simple queue system
- Using cloud storage for generated files
- Adding user authentication 