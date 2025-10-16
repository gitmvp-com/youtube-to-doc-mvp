"""Data models for YouTube video processing."""

from typing import Optional
from urllib.parse import urlparse, parse_qs
from pydantic import BaseModel, Field


class VideoQuery(BaseModel):
    """Schema for YouTube video query parameters."""
    
    url: str = Field(..., description="YouTube video URL")
    max_transcript_length: int = Field(10000, description="Maximum transcript length")

    def extract_video_id(self) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        try:
            parsed = urlparse(self.url)
            
            # Handle youtube.com/watch?v=VIDEO_ID
            if parsed.netloc.endswith("youtube.com") and parsed.path == "/watch":
                video_id = parse_qs(parsed.query).get("v", [None])[0]
                if video_id:
                    return video_id
            
            # Handle youtu.be/VIDEO_ID
            if parsed.netloc == "youtu.be":
                video_id = parsed.path.lstrip("/")
                if video_id:
                    return video_id
            
            # Handle youtube.com/embed/VIDEO_ID
            if parsed.netloc.endswith("youtube.com") and "/embed/" in parsed.path:
                video_id = parsed.path.split("/embed/")[1].split("/")[0]
                if video_id:
                    return video_id
            
            # Handle youtube.com/v/VIDEO_ID
            if parsed.netloc.endswith("youtube.com") and parsed.path.startswith("/v/"):
                video_id = parsed.path.split("/v/")[1].split("/")[0]
                if video_id:
                    return video_id
        
        except Exception:
            return None
        
        return None
