"""Home page router for YouTube to Doc MVP."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from ..query_processor import process_query
from ..server_config import EXAMPLE_VIDEOS, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render home page."""
    return templates.TemplateResponse(
        "index.jinja",
        {
            "request": request,
            "examples": EXAMPLE_VIDEOS,
        },
    )


@router.post("/", response_class=HTMLResponse)
async def process_video(
    request: Request,
    input_text: str = Form(...),
) -> HTMLResponse:
    """Process YouTube video and generate documentation."""
    return await process_query(
        request,
        input_text,
        max_transcript_length=10_000_000,
    )
