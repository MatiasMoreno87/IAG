"""
Agent 5 – Social Publisher
Publishes the generated content (image + video + copy) to Instagram, Facebook and TikTok
using their respective Graph/Content APIs.
"""
import time
from pathlib import Path
from typing import Optional

import requests
from rich.console import Console

from agents.base import (
    GeneratedCopy,
    GeneratedImage,
    GeneratedVideo,
    PublishResult,
)
from config.settings import settings
from utils.helpers import truncate, upload_to_public_url

console = Console()

GRAPH_BASE = "https://graph.facebook.com"
IG_BASE = "https://graph.instagram.com"
TIKTOK_BASE = "https://open.tiktokapis.com/v2"

# How long to poll for IG/FB video processing (seconds)
VIDEO_POLL_TIMEOUT = 300
VIDEO_POLL_INTERVAL = 10


class InstagramPublisher:
    """Publishes photo + reel to an Instagram Business/Creator account."""

    def __init__(self):
        self.user_id = settings.instagram_user_id
        self.token = settings.instagram_access_token
        self.api = f"{IG_BASE}/{settings.graph_api_version}"

    # ── Photo post ────────────────────────────────────────────────────────────

    def publish_photo(self, image_url: str, caption: str) -> PublishResult:
        console.print("  [dim]→ Instagram: publicando imagen...[/dim]")
        try:
            container_id = self._create_image_container(image_url, caption)
            post_id = self._publish_container(container_id)
            url = f"https://www.instagram.com/p/{post_id}/"
            console.print(f"  [green]✓ Instagram imagen publicada:[/green] {url}")
            return PublishResult("instagram_photo", True, post_id, url)
        except Exception as e:
            console.print(f"  [red]✗ Instagram imagen falló:[/red] {e}")
            return PublishResult("instagram_photo", False, error=str(e))

    def _create_image_container(self, image_url: str, caption: str) -> str:
        r = requests.post(
            f"{self.api}/{self.user_id}/media",
            params={
                "image_url": image_url,
                "caption": truncate(caption, 2200),
                "access_token": self.token,
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["id"]

    # ── Reel (video) post ─────────────────────────────────────────────────────

    def publish_reel(self, video_url: str, caption: str) -> PublishResult:
        console.print("  [dim]→ Instagram: publicando Reel...[/dim]")
        try:
            container_id = self._create_video_container(video_url, caption)
            self._wait_for_container(container_id)
            post_id = self._publish_container(container_id)
            url = f"https://www.instagram.com/reel/{post_id}/"
            console.print(f"  [green]✓ Instagram Reel publicado:[/green] {url}")
            return PublishResult("instagram_reel", True, post_id, url)
        except Exception as e:
            console.print(f"  [red]✗ Instagram Reel falló:[/red] {e}")
            return PublishResult("instagram_reel", False, error=str(e))

    def _create_video_container(self, video_url: str, caption: str) -> str:
        r = requests.post(
            f"{self.api}/{self.user_id}/media",
            params={
                "media_type": "REELS",
                "video_url": video_url,
                "caption": truncate(caption, 2200),
                "share_to_feed": "true",
                "access_token": self.token,
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["id"]

    def _wait_for_container(self, container_id: str) -> None:
        deadline = time.time() + VIDEO_POLL_TIMEOUT
        while time.time() < deadline:
            r = requests.get(
                f"{self.api}/{container_id}",
                params={"fields": "status_code,status", "access_token": self.token},
                timeout=15,
            )
            r.raise_for_status()
            status = r.json().get("status_code", "")
            if status == "FINISHED":
                return
            if status == "ERROR":
                raise RuntimeError(f"Instagram container error: {r.json()}")
            time.sleep(VIDEO_POLL_INTERVAL)
        raise TimeoutError("Instagram video processing timed out.")

    def _publish_container(self, container_id: str) -> str:
        r = requests.post(
            f"{self.api}/{self.user_id}/media_publish",
            params={"creation_id": container_id, "access_token": self.token},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["id"]


class FacebookPublisher:
    """Publishes photo + video to a Facebook Page."""

    def __init__(self):
        self.page_id = settings.facebook_page_id
        self.token = settings.facebook_access_token
        self.api = f"{GRAPH_BASE}/{settings.graph_api_version}"

    def publish_photo(self, image_url: str, caption: str) -> PublishResult:
        console.print("  [dim]→ Facebook: publicando foto...[/dim]")
        try:
            r = requests.post(
                f"{self.api}/{self.page_id}/photos",
                params={
                    "url": image_url,
                    "caption": truncate(caption, 63206),
                    "access_token": self.token,
                },
                timeout=30,
            )
            r.raise_for_status()
            post_id = r.json()["post_id"]
            url = f"https://www.facebook.com/{post_id}"
            console.print(f"  [green]✓ Facebook foto publicada:[/green] {url}")
            return PublishResult("facebook_photo", True, post_id, url)
        except Exception as e:
            console.print(f"  [red]✗ Facebook foto falló:[/red] {e}")
            return PublishResult("facebook_photo", False, error=str(e))

    def publish_video(self, video_url: str, description: str) -> PublishResult:
        console.print("  [dim]→ Facebook: publicando video...[/dim]")
        try:
            r = requests.post(
                f"{self.api}/{self.page_id}/videos",
                params={
                    "file_url": video_url,
                    "description": truncate(description, 63206),
                    "access_token": self.token,
                },
                timeout=60,
            )
            r.raise_for_status()
            video_id = r.json()["id"]
            url = f"https://www.facebook.com/video/{video_id}"
            console.print(f"  [green]✓ Facebook video publicado:[/green] {url}")
            return PublishResult("facebook_video", True, video_id, url)
        except Exception as e:
            console.print(f"  [red]✗ Facebook video falló:[/red] {e}")
            return PublishResult("facebook_video", False, error=str(e))


class TikTokPublisher:
    """Publishes a video to TikTok using the Content Posting API v2."""

    def __init__(self):
        self.token = settings.tiktok_access_token
        self.open_id = settings.tiktok_open_id

    def publish_video(self, video_url: str, caption: str, hashtags: str) -> PublishResult:
        console.print("  [dim]→ TikTok: publicando video...[/dim]")
        try:
            title = truncate(f"{caption} {hashtags}", 150)
            r = requests.post(
                f"{TIKTOK_BASE}/post/publish/video/init/",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
                json={
                    "post_info": {
                        "title": title,
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                        "video_cover_timestamp_ms": 1000,
                    },
                    "source_info": {
                        "source": "URL_UPLOAD",
                        "video_url": video_url,
                        "video_size": 0,  # will be determined by TikTok
                        "chunk_size": 0,
                        "total_chunk_count": 1,
                    },
                },
                timeout=30,
            )
            r.raise_for_status()
            data = r.json().get("data", {})
            publish_id = data.get("publish_id", "")
            console.print(f"  [green]✓ TikTok video iniciado:[/green] publish_id={publish_id}")
            post_url = f"https://www.tiktok.com/@{self.open_id}"
            return PublishResult("tiktok", True, publish_id, post_url)
        except Exception as e:
            console.print(f"  [red]✗ TikTok falló:[/red] {e}")
            return PublishResult("tiktok", False, error=str(e))


class SocialPublisherAgent:
    """Orchestrates publishing across all requested platforms."""

    def __init__(self):
        self.ig = InstagramPublisher()
        self.fb = FacebookPublisher()
        self.tt = TikTokPublisher()

    def publish(
        self,
        copy: GeneratedCopy,
        image: GeneratedImage,
        video: GeneratedVideo,
        platforms: list[str],
    ) -> list[PublishResult]:
        console.print("\n[bold cyan]📡 Agent 5: Publicando en redes sociales...[/bold cyan]")

        if settings.dry_run:
            console.print("[yellow]⚠  DRY_RUN=true – saltando publicación real.[/yellow]")
            return [
                PublishResult(p, True, "dry-run-id", f"https://{p}.com/dry-run")
                for p in platforms
            ]

        results: list[PublishResult] = []

        if "instagram" in platforms:
            results.append(self.ig.publish_photo(image.url, copy.instagram.full_text))
            results.append(self.ig.publish_reel(video.url, copy.instagram.full_text))

        if "facebook" in platforms:
            results.append(self.fb.publish_photo(image.url, copy.facebook.full_text))
            results.append(self.fb.publish_video(video.url, copy.facebook.full_text))

        if "tiktok" in platforms:
            results.append(
                self.tt.publish_video(video.url, copy.tiktok.caption, copy.tiktok.hashtags)
            )

        successes = sum(1 for r in results if r.success)
        console.print(
            f"\n[bold]Publicaciones: {successes}/{len(results)} exitosas.[/bold]"
        )
        return results
