"""Server configuration for YouTube to Doc MVP."""

from pathlib import Path
from typing import Dict, List
from fastapi.templating import Jinja2Templates

# Constants
MAX_DISPLAY_SIZE = 300_000
DELETE_CACHE_AFTER = 60 * 60  # seconds

EXAMPLE_VIDEOS: List[Dict[str, str]] = [
    {"name": "Python Tutorial", "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc"},
    {"name": "FastAPI Crash Course", "url": "https://www.youtube.com/watch?v=7t2alSnE2-I"},
    {"name": "JavaScript ES6", "url": "https://www.youtube.com/watch?v=WZQc7RUAg18"},
]

# Templates
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
