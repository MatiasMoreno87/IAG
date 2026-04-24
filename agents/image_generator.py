"""
Agent 2 – Image Generator
Uses fal.ai Flux Pro to generate a professional product mockup image
based on the optimized prompt from Agent 1.
"""
import time
from pathlib import Path

import fal_client
from rich.console import Console

from agents.base import GeneratedImage, OptimizedPrompts
from config.settings import settings
from utils.helpers import download_file

console = Console()

IMAGE_SIZE = "landscape_16_9"   # ideal for social media feeds
NUM_IMAGES = 1
NUM_STEPS = 28
GUIDANCE_SCALE = 3.5


class ImageGeneratorAgent:
    def generate(self, prompts: OptimizedPrompts) -> GeneratedImage:
        console.print("\n[bold cyan]🎨 Agent 2: Generando imagen mockup...[/bold cyan]")

        result = fal_client.subscribe(
            settings.image_model,
            arguments={
                "prompt": prompts.image_prompt,
                "image_size": IMAGE_SIZE,
                "num_inference_steps": NUM_STEPS,
                "guidance_scale": GUIDANCE_SCALE,
                "num_images": NUM_IMAGES,
                "safety_tolerance": "2",
                "output_format": "jpeg",
            },
            with_logs=False,
            on_queue_update=self._on_update,
        )

        image_url = result["images"][0]["url"]
        console.print(f"[green]✓ Imagen generada[/green]: {image_url[:60]}...")

        local_path = self._download(image_url)
        return GeneratedImage(url=image_url, local_path=str(local_path))

    def _on_update(self, update: fal_client.InProgress) -> None:
        if hasattr(update, "logs") and update.logs:
            for log in update.logs[-1:]:
                console.print(f"  [dim]{log.get('message', '')}[/dim]")

    def _download(self, url: str) -> Path:
        filename = f"mockup_{int(time.time())}.jpg"
        path = download_file(url, settings.output_dir, filename)
        console.print(f"  [dim]Guardada en:[/dim] {path}")
        return path
