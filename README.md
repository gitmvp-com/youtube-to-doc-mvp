# YouTube to Doc - MVP

A minimal viable product that converts YouTube videos into comprehensive documentation. Extract transcripts, metadata, and generate formatted documentation perfect for AI tools and LLMs.

## 🚀 Features

- ✅ **YouTube Video Processing**: Extract video metadata and descriptions
- ✅ **Transcript Extraction**: Automatically extract video transcripts
- ✅ **AI-Friendly Output**: Generate structured markdown documentation
- ✅ **Simple Web Interface**: Easy-to-use form for processing videos
- ✅ **Fast Processing**: Efficient video processing
- ✅ **Docker Ready**: Quick deployment with Docker

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python 3.11
- **Frontend**: Jinja2 templates + HTML
- **Video Processing**: yt-dlp, youtube-transcript-api
- **Token Estimation**: tiktoken
- **Deployment**: Docker

## 📦 Installation

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/gitmvp-com/youtube-to-doc-mvp.git
cd youtube-to-doc-mvp

# Run with Docker Compose
docker-compose up
```

Then open `http://localhost:8000` in your browser.

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/gitmvp-com/youtube-to-doc-mvp.git
cd youtube-to-doc-mvp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the application
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🚀 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a YouTube video URL
3. Click "Generate Documentation"
4. The app will extract and display the documentation

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page |
| `POST` | `/` | Process a YouTube video |
| `GET` | `/health` | Health check endpoint |

## 🌐 Limitations (MVP)

This MVP version has simplified features:

- ❌ No comments extraction
- ❌ No multiple language support (English only)
- ❌ No S3 cloud storage integration
- ❌ No authentication
- ❌ No proxy support for cloud deployment

## 🤝 Contributing

Feel free to fork and submit pull requests!

## 📄 License

MIT License

## 🙏 Credits

Based on [filiksyos/Youtube-to-Doc](https://github.com/filiksyos/Youtube-to-Doc)
