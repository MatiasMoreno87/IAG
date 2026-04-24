#!/usr/bin/env python3
"""
Social Media Automation Agent
==============================
Multi-agent pipeline that takes a product brief (+ optional reference image) and:

  1. Optimizes prompts          (Agent 1 – Claude Vision)
  2. Generates a mockup image   (Agent 2 – fal.ai Flux Pro)
  3. Generates a promo video    (Agent 3 – fal.ai Kling)
  4. Writes persuasive copy     (Agent 4 – Claude)
  5. Publishes everywhere       (Agent 5 – IG / FB / TikTok Graph APIs)

Usage:
  python main.py run \\
    --product "Crema Hidratante XY" \\
    --description "Crema 100% natural para piel sensible" \\
    --audience "Mujeres 25-40 interesadas en skincare natural" \\
    --tone "profesional y cálido" \\
    --image ./reference.jpg \\
    --hashtags "#skincare #natural #belleza" \\
    --platforms instagram facebook tiktok

  python main.py run --help
"""
import json
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents.base import CampaignInput, CampaignOutput
from agents.copy_writer import CopyWriterAgent
from agents.image_generator import ImageGeneratorAgent
from agents.prompt_optimizer import PromptOptimizerAgent
from agents.social_publisher import SocialPublisherAgent
from agents.video_generator import VideoGeneratorAgent
from config.settings import settings

console = Console()

PLATFORM_CHOICES = ["instagram", "facebook", "tiktok"]


# ── Pipeline ──────────────────────────────────────────────────────────────────

def run_pipeline(campaign: CampaignInput) -> CampaignOutput:
    start = time.time()

    console.print(
        Panel(
            f"[bold white]Campaña:[/bold white] {campaign.product_name}\n"
            f"[dim]Plataformas: {', '.join(campaign.platforms)}[/dim]",
            title="🚀 Social Media Automation Agent",
            border_style="cyan",
        )
    )

    # ── Agent 1: Optimize prompts ─────────────────────────────────────────────
    optimizer = PromptOptimizerAgent()
    prompts = optimizer.optimize(campaign)

    # ── Agent 2: Generate mockup image ────────────────────────────────────────
    img_gen = ImageGeneratorAgent()
    image = img_gen.generate(prompts)

    # ── Agent 3: Generate promo video ─────────────────────────────────────────
    vid_gen = VideoGeneratorAgent()
    video = vid_gen.generate(image, prompts)

    # ── Agent 4: Generate persuasive copy ─────────────────────────────────────
    copywriter = CopyWriterAgent()
    copy = copywriter.generate(campaign, prompts)

    # ── Agent 5: Publish to social media ──────────────────────────────────────
    publisher = SocialPublisherAgent()
    publications = publisher.publish(copy, image, video, campaign.platforms)

    output = CampaignOutput(
        prompts=prompts,
        image=image,
        video=video,
        copy=copy,
        publications=publications,
    )

    elapsed = time.time() - start
    _print_summary(output, elapsed)
    _save_report(output, campaign)
    return output


# ── Output helpers ────────────────────────────────────────────────────────────

def _print_summary(output: CampaignOutput, elapsed: float) -> None:
    console.print()
    console.print(Panel("[bold green]✅ Pipeline completado[/bold green]", border_style="green"))

    # Assets
    assets = Table(show_header=True, header_style="bold magenta")
    assets.add_column("Asset")
    assets.add_column("URL / Ruta")
    assets.add_row("🖼  Imagen mockup", output.image.local_path or output.image.url)
    assets.add_row("🎬 Video promo", output.video.local_path or output.video.url)
    console.print(assets)

    # Copy preview
    console.print("\n[bold]Copy generado:[/bold]")
    for platform, copy_obj in [
        ("Instagram", output.copy.instagram),
        ("Facebook", output.copy.facebook),
        ("TikTok", output.copy.tiktok),
    ]:
        console.print(f"\n[bold cyan]{platform}[/bold cyan]")
        console.print(f"  {copy_obj.caption[:120]}...")
        console.print(f"  [dim]{copy_obj.hashtags[:80]}[/dim]")
        console.print(f"  [italic]{copy_obj.call_to_action}[/italic]")

    # Publication results
    pub_table = Table(show_header=True, header_style="bold blue")
    pub_table.add_column("Plataforma")
    pub_table.add_column("Estado")
    pub_table.add_column("URL")
    for r in output.publications:
        status = "[green]✓[/green]" if r.success else f"[red]✗ {r.error}[/red]"
        pub_table.add_row(r.platform, status, r.post_url or "-")
    console.print("\n[bold]Publicaciones:[/bold]")
    console.print(pub_table)

    console.print(f"\n[dim]Tiempo total: {elapsed:.1f}s[/dim]")


def _save_report(output: CampaignOutput, campaign: CampaignInput) -> None:
    report = {
        "product": campaign.product_name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "prompts": {
            "image": output.prompts.image_prompt,
            "video": output.prompts.video_prompt,
            "summary": output.prompts.content_summary,
        },
        "assets": {
            "image_url": output.image.url,
            "image_local": output.image.local_path,
            "video_url": output.video.url,
            "video_local": output.video.local_path,
        },
        "copy": {
            "instagram": {
                "caption": output.copy.instagram.caption,
                "hashtags": output.copy.instagram.hashtags,
                "cta": output.copy.instagram.call_to_action,
            },
            "facebook": {
                "caption": output.copy.facebook.caption,
                "hashtags": output.copy.facebook.hashtags,
                "cta": output.copy.facebook.call_to_action,
            },
            "tiktok": {
                "caption": output.copy.tiktok.caption,
                "hashtags": output.copy.tiktok.hashtags,
                "cta": output.copy.tiktok.call_to_action,
            },
        },
        "publications": [
            {
                "platform": r.platform,
                "success": r.success,
                "post_id": r.post_id,
                "post_url": r.post_url,
                "error": r.error,
            }
            for r in output.publications
        ],
    }
    report_path = settings.output_dir / f"report_{int(time.time())}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    console.print(f"\n[dim]Reporte guardado en:[/dim] {report_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

@click.group()
def cli():
    """Social Media Automation Agent – genera y publica contenido con IA."""


@cli.command()
@click.option("--product", "-p", required=True, help="Nombre del producto.")
@click.option("--description", "-d", required=True, help="Descripción del producto/campaña.")
@click.option("--audience", "-a", required=True, help="Audiencia objetivo.")
@click.option("--tone", "-t", default="profesional", show_default=True, help="Tono de marca.")
@click.option("--image", "-i", default=None, type=click.Path(exists=True), help="Imagen de referencia (opcional).")
@click.option("--notes", "-n", default=None, help="Notas adicionales para los agentes.")
@click.option(
    "--platforms",
    multiple=True,
    default=PLATFORM_CHOICES,
    type=click.Choice(PLATFORM_CHOICES),
    show_default=True,
    help="Plataformas donde publicar.",
)
@click.option("--hashtags", default="", help="Hashtags separados por espacio.")
@click.option("--dry-run", is_flag=True, default=None, help="No publicar realmente.")
def run(product, description, audience, tone, image, notes, platforms, hashtags, dry_run):
    """Ejecuta el pipeline completo de generación y publicación."""
    # Allow CLI flag to override env
    if dry_run is not None:
        settings.dry_run = dry_run

    missing = settings.validate()
    if missing:
        console.print(f"[red]Error: faltan variables de entorno: {', '.join(missing)}[/red]")
        console.print("[dim]Copia .env.example a .env y completa los valores.[/dim]")
        sys.exit(1)

    campaign = CampaignInput(
        product_name=product,
        description=description,
        target_audience=audience,
        brand_tone=tone,
        reference_image_path=image,
        extra_notes=notes,
        platforms=list(platforms),
        hashtags=[h.strip("#") for h in hashtags.split() if h],
    )

    run_pipeline(campaign)


@cli.command()
def check_config():
    """Verifica que todas las variables de entorno estén configuradas."""
    missing = settings.validate()
    if missing:
        console.print(f"[red]Faltan:[/red] {', '.join(missing)}")
        sys.exit(1)
    console.print("[green]✓ Configuración completa.[/green]")
    console.print(f"  Modelo IA:     {settings.anthropic_model}")
    console.print(f"  Modelo imagen: {settings.image_model}")
    console.print(f"  Modelo video:  {settings.video_model}")
    console.print(f"  Output dir:    {settings.output_dir}")
    console.print(f"  Dry run:       {settings.dry_run}")


if __name__ == "__main__":
    cli()
