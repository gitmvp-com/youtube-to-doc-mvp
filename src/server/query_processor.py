"""Process YouTube video queries and generate documentation."""

from typing import Optional

from fastapi import Request
from starlette.templating import _TemplateResponse

from ..youtubedoc.youtube_processor import YoutubeProcessor
from ..youtubedoc.schemas.video_schema import VideoQuery
from .server_config import EXAMPLE_VIDEOS, MAX_DISPLAY_SIZE, templates
from .server_utils import Colors


async def process_query(
    request: Request,
    input_text: str,
    max_transcript_length: int = 10_000_000,
) -> _TemplateResponse:
    """Process a YouTube video URL and generate documentation."""

    context = {
        "request": request,
        "video_url": input_text,
        "examples": EXAMPLE_VIDEOS,
        "content": None,
        "error_message": None,
        "result": False,
        "video_info": {},
    }

    try:
        # Parse and validate YouTube URL
        query = VideoQuery(
            url=input_text,
            max_transcript_length=max_transcript_length,
        )

        # Initialize YouTube processor
        processor = YoutubeProcessor()

        # Process the video
        video_info, transcript = await processor.process_video(query)

        # Generate documentation
        content_md = _generate_documentation(video_info, transcript)

        # Display content
        if len(content_md) > MAX_DISPLAY_SIZE:
            content_md = (
                f"(Content cropped to {int(MAX_DISPLAY_SIZE / 1_000)}k characters)\n"
                + content_md[:MAX_DISPLAY_SIZE]
            )

        context["content"] = content_md
        context["video_info"] = video_info
        context["result"] = True

        _print_success(
            url=input_text,
            title=video_info.get("title", "Unknown"),
            transcript_length=len(transcript) if transcript else 0,
        )

    except Exception as exc:
        _print_error(input_text, exc)
        error_msg = f"Error processing video: {exc}"
        
        if "not available" in str(exc).lower():
            error_msg = "Video not available. Please check the URL and try again."
        elif "transcript" in str(exc).lower():
            error_msg = "Transcript not available for this video."

        context["error_message"] = error_msg

    return templates.TemplateResponse(name="index.jinja", context=context)


def _generate_documentation(
    video_info: dict,
    transcript: Optional[str],
) -> str:
    """Generate formatted documentation from video information."""
    doc_parts = []

    # Header
    doc_parts.append("# YouTube Video Documentation\n\n")

    # Metadata
    doc_parts.append(f"**Title:** {video_info.get('title', 'Unknown')}\n")
    doc_parts.append(f"**URL:** {video_info.get('url', 'Unknown')}\n")
    doc_parts.append(f"**Duration:** {_format_duration(video_info.get('duration', 0))}\n")
    doc_parts.append(f"**Views:** {video_info.get('view_count', 'Unknown')}\n")
    doc_parts.append(f"**Channel:** {video_info.get('channel', 'Unknown')}\n")
    doc_parts.append(f"**Upload Date:** {video_info.get('upload_date', 'Unknown')}\n\n")

    # Description
    if video_info.get('description'):
        doc_parts.append("## Description\n")
        doc_parts.append(f"{video_info['description']}\n\n")

    # Transcript
    if transcript:
        doc_parts.append("## Transcript\n")
        doc_parts.append(f"{transcript}\n\n")

    # Token estimation
    content = "".join(doc_parts)
    estimated_tokens = _estimate_tokens(content)
    doc_parts.append(f"**Estimated Tokens:** {estimated_tokens}\n")

    return "".join(doc_parts)


def _format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs}s"


def _estimate_tokens(text: str) -> int:
    """Estimate token count for text content."""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))
    except ImportError:
        # Fallback: approximately 4 characters per token
        return len(text) // 4


def _print_success(url: str, title: str, transcript_length: int) -> None:
    """Print success message."""
    print(
        f"{Colors.GREEN}✓ Processed{Colors.END}: {url} | "
        f"{Colors.YELLOW}{title[:40]}{Colors.END} | "
        f"{Colors.CYAN}{transcript_length} chars{Colors.END}"
    )


def _print_error(url: str, error: Exception) -> None:
    """Print error message."""
    print(f"{Colors.RED}✗ Error{Colors.END}: {url} | {Colors.RED}{error}{Colors.END}")
