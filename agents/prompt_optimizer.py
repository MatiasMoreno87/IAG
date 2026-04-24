"""
Agent 1 – Prompt Optimizer
Analyzes the reference image (if provided) and campaign brief using Claude Vision,
then produces optimized prompts for the image generator and video generator.
"""
import json
from typing import Optional

import anthropic
from rich.console import Console

from agents.base import CampaignInput, OptimizedPrompts
from config.settings import settings
from utils.helpers import encode_image_to_base64

console = Console()

SYSTEM_PROMPT = """Eres un experto en marketing digital y generación de contenido visual para redes sociales.
Tu rol es analizar briefings de campaña y crear prompts altamente optimizados para:
1. Generación de imágenes mockup de productos (usando modelos de difusión como Flux Pro).
2. Generación de videos promocionales cortos (usando modelos de video como Kling).

Los prompts deben ser:
- Específicos, ricos en detalles visuales y estilo.
- Orientados a conversión y engagement en redes sociales.
- Adaptados al tono de la marca y audiencia objetivo.
- En inglés (los modelos de imagen/video responden mejor en inglés).

Responde SIEMPRE con un JSON válido con las claves:
{
  "image_prompt": "<prompt para generar imagen mockup>",
  "video_prompt": "<prompt para generar video promocional>",
  "content_summary": "<resumen conciso del producto y campaña en español, max 3 oraciones>"
}"""

IMAGE_ANALYSIS_PROMPT = """Analiza esta imagen de referencia del producto/campaña y el briefing a continuación.
Genera prompts optimizados para crear contenido visual de alta calidad para redes sociales.

BRIEFING:
- Producto: {product_name}
- Descripción: {description}
- Audiencia objetivo: {target_audience}
- Tono de marca: {brand_tone}
- Notas adicionales: {extra_notes}

Considera los elementos visuales de la imagen de referencia (colores, estilo, composición)
y amplíalos para crear un mockup profesional y un video dinámico que conviertan."""

TEXT_ONLY_PROMPT = """Basándote en el siguiente briefing de campaña, genera prompts optimizados
para crear contenido visual atractivo y que convierta para redes sociales.

BRIEFING:
- Producto: {product_name}
- Descripción: {description}
- Audiencia objetivo: {target_audience}
- Tono de marca: {brand_tone}
- Notas adicionales: {extra_notes}

Crea prompts que capturen la esencia del producto y generen deseo en la audiencia objetivo."""


class PromptOptimizerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def optimize(self, campaign: CampaignInput) -> OptimizedPrompts:
        console.print("\n[bold cyan]🧠 Agent 1: Optimizando prompts...[/bold cyan]")

        messages = self._build_messages(campaign)

        response = self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        )

        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)

        result = OptimizedPrompts(
            image_prompt=data["image_prompt"],
            video_prompt=data["video_prompt"],
            content_summary=data["content_summary"],
        )

        console.print(f"[green]✓ Prompts generados[/green]")
        console.print(f"  [dim]Imagen:[/dim] {result.image_prompt[:80]}...")
        console.print(f"  [dim]Video:[/dim]  {result.video_prompt[:80]}...")
        return result

    def _build_messages(self, campaign: CampaignInput) -> list:
        extra = campaign.extra_notes or "Ninguna"

        if campaign.reference_image_path:
            img_data, media_type = encode_image_to_base64(campaign.reference_image_path)
            prompt_text = IMAGE_ANALYSIS_PROMPT.format(
                product_name=campaign.product_name,
                description=campaign.description,
                target_audience=campaign.target_audience,
                brand_tone=campaign.brand_tone,
                extra_notes=extra,
            )
            return [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": img_data,
                            },
                        },
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ]
        else:
            prompt_text = TEXT_ONLY_PROMPT.format(
                product_name=campaign.product_name,
                description=campaign.description,
                target_audience=campaign.target_audience,
                brand_tone=campaign.brand_tone,
                extra_notes=extra,
            )
            return [{"role": "user", "content": prompt_text}]
