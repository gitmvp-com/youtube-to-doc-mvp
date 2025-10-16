"""Server utilities for YouTube to Doc MVP."""

from contextlib import asynccontextmanager
from typing import Generator


class Colors:
    """ANSI color codes for console output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'


@asynccontextmanager
async def lifespan(app) -> Generator:
    """Application lifespan manager."""
    # Startup
    print(f"{Colors.GREEN}YouTube to Doc MVP server starting up...{Colors.END}")
    yield
    # Shutdown
    print(f"{Colors.RED}YouTube to Doc MVP server shutting down...{Colors.END}")
