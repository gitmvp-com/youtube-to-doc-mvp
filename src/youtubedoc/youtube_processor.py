"""YouTube video processor for extracting metadata and transcripts."""

import asyncio
from typing import Tuple, Optional
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

from .schemas.video_schema import VideoQuery


class YoutubeProcessor:
    """Process YouTube videos and extract information."""

    def __init__(self):
        """Initialize the YouTube processor."""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
        }

    async def process_video(
        self,
        query: VideoQuery,
    ) -> Tuple[dict, Optional[str]]:
        """Process a YouTube video and extract metadata and transcript.
        
        Parameters
        ----------
        query : VideoQuery
            The video query containing URL and processing parameters.

        Returns
        -------
        Tuple[dict, Optional[str]]
            A tuple of (video_info, transcript) where video_info is a dictionary
            containing video metadata and transcript is the full transcript text.
        """
        video_id = query.extract_video_id()
        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {query.url}")

        # Get video info
        video_info = await self._get_video_info(video_id, query.url)

        # Get transcript
        transcript = await self._get_transcript(
            video_id,
            query.max_transcript_length,
        )

        return video_info, transcript

    async def _get_video_info(self, video_id: str, url: str) -> dict:
        """Extract video information using yt-dlp."""
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, self._extract_video_info, video_id)
            return info
        except Exception as exc:
            raise ValueError(f"Failed to extract video info: {exc}") from exc

    def _extract_video_info(self, video_id: str) -> dict:
        """Extract video info synchronously."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                
                return {
                    "video_id": video_id,
                    "title": info.get("title", "Unknown"),
                    "description": info.get("description", ""),
                    "duration": info.get("duration", 0),
                    "view_count": self._format_number(info.get("view_count", 0)),
                    "channel": info.get("uploader", "Unknown"),
                    "upload_date": self._format_date(info.get("upload_date", "")),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
        except Exception as exc:
            raise ValueError(f"Could not fetch video info: {exc}") from exc

    async def _get_transcript(
        self,
        video_id: str,
        max_length: int,
    ) -> Optional[str]:
        """Extract video transcript."""
        try:
            loop = asyncio.get_event_loop()
            transcript = await loop.run_in_executor(
                None,
                self._extract_transcript,
                video_id,
            )
            return transcript[:max_length] if transcript else None
        except TranscriptsDisabled:
            raise ValueError("Transcripts are disabled for this video.")
        except NoTranscriptFound:
            raise ValueError("No transcript found for this video.")
        except Exception as exc:
            raise ValueError(f"Could not fetch transcript: {exc}") from exc

    @staticmethod
    def _extract_transcript(video_id: str) -> str:
        """Extract transcript synchronously."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry["text"] for entry in transcript_list])
        except Exception as exc:
            raise ValueError(f"Failed to extract transcript: {exc}") from exc

    @staticmethod
    def _format_number(num: int) -> str:
        """Format large numbers in human-readable format."""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(num)

    @staticmethod
    def _format_date(date_str: str) -> str:
        """Format date string YYYYMMDD to YYYY-MM-DD."""
        if len(date_str) == 8:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return date_str
