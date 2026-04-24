"""
Agent 3 – Video Generator
Uses fal.ai Kling image-to-video to turn the product mockup image into
a short, dynamic promotional video optimized for social media.
"""
import time
from pathlib import Path

import fal_client
from rich.console import Console

from agents.base import GeneratedImage, GeneratedVideo, OptimizedPrompts
from config.settings import settings
from utils.helpers import download_file, upload_to_public_url

console = Console()

VIDEO_DURATION = "5"     # seconds – Kling supports 5 or 10
ASPECT_RATIO = "16:9"
CFG_SCALE = 0.5


class VideoGeneratorAgent:
    def generate(self, image: GeneratedImage, prompts: OptimizedPrompts) -> GeneratedVideo:
        console.print("\n[bold cyan]🎬 Agent 3: Generando video promocional...[/bold cyan]")

        # fal.ai needs a publicly reachable URL for the source image
        image_url = self._resolve_public_url(image)

        result = fal_client.subscribe(
            settings.video_model,
            arguments={
                "prompt": prompts.video_prompt,
                "image_url": image_url,
                "duration": VIDEO_DURATION,
                "aspect_ratio": ASPECT_RATIO,
                "cfg_scale": CFG_SCALE,
            },
            with_logs=False,
            on_queue_update=self._on_update,
        )

        video_url = result["video"]["url"]
        console.print(f"[green]✓ Video generado[/green]: {video_url[:60]}...")

        local_path = self._download(video_url)
        return GeneratedVideo(url=video_url, local_path=str(local_path))

    def _resolve_public_url(self, image: GeneratedImage) -> str:
        """
        Prefer the fal.ai CDN URL (already public).
        Fall back to uploading the local file if the CDN URL has expired.
        """
        if image.url.startswith("http"):
            return image.url
        if image.local_path:
            return upload_to_public_url(Path(image.local_path))
        raise ValueError("No se pudo obtener una URL pública para la imagen de referencia.")

    def _on_update(self, update: fal_client.InProgress) -> None:
        if hasattr(update, "logs") and update.logs:
            for log in update.logs[-1:]:
                console.print(f"  [dim]{log.get('message', '')}[/dim]")

    def _download(self, url: str) -> Path:
        filename = f"promo_video_{int(time.time())}.mp4"
        path = download_file(url, settings.output_dir, filename)
        console.print(f"  [dim]Guardado en:[/dim] {path}")
        return path
