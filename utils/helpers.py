import base64
import mimetypes
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
import requests
from rich.console import Console

console = Console()


def encode_image_to_base64(image_path: str) -> tuple[str, str]:
    """Return (base64_data, media_type) for a local image file."""
    path = Path(image_path)
    media_type, _ = mimetypes.guess_type(str(path))
    if not media_type:
        media_type = "image/jpeg"
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def download_file(url: str, dest_dir: Path, filename: Optional[str] = None) -> Path:
    """Download a remote file and save it locally. Returns the local path."""
    if not filename:
        parsed = urlparse(url)
        filename = Path(parsed.path).name or f"file_{int(time.time())}"
    dest = dest_dir / filename
    with httpx.stream("GET", url, follow_redirects=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_bytes(chunk_size=8192):
                f.write(chunk)
    return dest


def upload_to_public_url(local_path: Path) -> str:
    """
    Placeholder: upload a local file to a publicly accessible URL.

    In production, replace this with your preferred storage solution:
    - AWS S3 + presigned URL
    - Cloudinary
    - Bunny CDN
    - etc.

    For now, returns the local file:// URL so the pipeline can be tested
    without cloud storage set up.
    """
    return local_path.resolve().as_uri()


def wait_with_progress(seconds: int, label: str = "Waiting") -> None:
    """Show a countdown while waiting for an async process."""
    import time
    for i in range(seconds, 0, -1):
        console.print(f"[dim]{label}: {i}s remaining...[/dim]", end="\r")
        time.sleep(1)
    console.print()


def truncate(text: str, max_len: int = 2200) -> str:
    """Truncate text to platform character limits."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
