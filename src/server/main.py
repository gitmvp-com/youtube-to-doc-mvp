"""Main FastAPI application for YouTube to Doc MVP."""

import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .routers import index
from .server_config import templates
from .server_utils import lifespan

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="YouTube to Doc MVP", version="1.0.0", lifespan=lifespan)

# Mount static files
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure allowed hosts
allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
allowed_hosts = [host.strip() for host in allowed_hosts]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/robots.txt")
async def robots() -> FileResponse:
    """Serve robots.txt file."""
    robots_path = Path(__file__).parent.parent.parent / "static" / "robots.txt"
    if robots_path.exists():
        return FileResponse(robots_path)
    return FileResponse("static/robots.txt")


@app.get("/api", response_class=HTMLResponse)
@app.get("/api/", response_class=HTMLResponse)
async def api_docs(request: Request) -> HTMLResponse:
    """API documentation page."""
    return templates.TemplateResponse("api.jinja", {"request": request})


# Include routers
app.include_router(index)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
