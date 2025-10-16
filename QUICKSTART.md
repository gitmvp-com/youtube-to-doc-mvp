# YouTube to Doc MVP - Quick Start Guide

Welcome! This is a minimal viable product (MVP) version of the YouTube to Doc application.

## What This MVP Does

- Extract YouTube Video Metadata: Title, duration, views, channel, upload date
- Extract Video Transcripts: Automatic subtitle extraction from videos
- Generate AI-Friendly Documentation: Markdown format optimized for LLM consumption
- Token Estimation: Estimate token counts for OpenAI models
- Beautiful Web Interface: Simple and intuitive form-based UI

## 5-Minute Setup

### Option A: Docker (Easiest)

```bash
# 1. Clone and enter directory
git clone https://github.com/gitmvp-com/youtube-to-doc-mvp.git
cd youtube-to-doc-mvp

# 2. Run with Docker
docker-compose up

# 3. Open browser
# Visit: http://localhost:8000
```

### Option B: Local Python

```bash
# 1. Clone and enter directory
git clone https://github.com/gitmvp-com/youtube-to-doc-mvp.git
cd youtube-to-doc-mvp

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run the app
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Open browser
# Visit: http://localhost:8000
```

## Usage

1. Enter a YouTube URL in the input field
2. Click Generate Documentation
3. View the results including video metadata, full transcript, and token count
4. Copy to clipboard for use in your projects

## Supported YouTube URL Formats

- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- https://www.youtube.com/embed/VIDEO_ID
- https://www.youtube.com/v/VIDEO_ID

## API Endpoints

- GET /: Home page
- POST /: Process a video (input_text parameter)
- GET /health: Health check
- GET /api: API documentation

## Configuration

Edit .env file to customize ALLOWED_HOSTS, DEBUG mode, and MAX_TRANSCRIPT_LENGTH.

## Troubleshooting

- Port in use: Use a different port with --port flag
- Transcript not found: Ensure video is public and has captions
- FFmpeg not found: Install with apt-get (Linux) or brew (Mac)

## Full Version Features

This MVP is the core. Full version adds:
- Multiple language support
- Comments extraction
- S3 integration
- Advanced rate limiting
- Authentication
- Cloud deployment

Based on: https://github.com/filiksyos/Youtube-to-Doc
