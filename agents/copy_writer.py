"""
Agent 4 – Copy Writer
Uses Claude to generate persuasive, conversion-focused copy for each platform
(Instagram, Facebook, TikTok) tailored to tone, audience, and platform conventions.
"""
import json

import anthropic
from rich.console import Console

from agents.base import (
    CampaignInput,
    GeneratedCopy,
    OptimizedPrompts,
    PlatformCopy,
)
from config.settings import settings

console = Console()

SYSTEM_PROMPT = """Eres un experto copywriter de marketing digital especializado en redes sociales.
Escribes copy persuasivo, orientado a la conversión y adaptado a cada plataforma.

Principios que siempre aplicas:
- AIDA (Atención, Interés, Deseo, Acción) adaptado al formato de cada red social.
- Lenguaje emocional que conecta con la audiencia objetivo.
- CTA (llamada a la acción) clara y específica.
- Hashtags estratégicos y relevantes.
- Respetar el tono y personalidad de la marca.
- Formato nativo de cada plataforma (Instagram: visual storytelling; Facebook: más descripción; TikTok: energético, trending).

Responde SIEMPRE con JSON válido con esta estructura exacta:
{
  "instagram": {
    "caption": "<texto principal del post, máximo 2200 chars>",
    "hashtags": "<30 hashtags relevantes separados por espacio>",
    "call_to_action": "<CTA específica para Instagram Stories o el link en bio>"
  },
  "facebook": {
    "caption": "<texto principal, puede ser más largo y descriptivo, incluye storytelling>",
    "hashtags": "<5-10 hashtags relevantes>",
    "call_to_action": "<CTA con botón de acción sugerido: Comprar ahora / Más info / etc.>"
  },
  "tiktok": {
    "caption": "<texto corto y energético, máximo 150 chars, con emojis>",
    "hashtags": "<hashtags trending + de nicho, máximo 8>",
    "call_to_action": "<CTA para TikTok: sigue, comenta, usa el link en bio>"
  }
}"""

COPY_PROMPT = """Crea copy de alto impacto para la siguiente campaña de producto:

PRODUCTO: {product_name}
RESUMEN DE CAMPAÑA: {content_summary}
DESCRIPCIÓN COMPLETA: {description}
AUDIENCIA OBJETIVO: {target_audience}
TONO DE MARCA: {brand_tone}
HASHTAGS SUGERIDOS POR EL CLIENTE: {hashtags}
NOTAS ADICIONALES: {extra_notes}

Genera copy persuasivo y que convierta para Instagram, Facebook y TikTok.
Cada plataforma debe tener un approach diferente adaptado a su audiencia y formato."""


class CopyWriterAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, campaign: CampaignInput, prompts: OptimizedPrompts) -> GeneratedCopy:
        console.print("\n[bold cyan]✍️  Agent 4: Generando copy persuasivo...[/bold cyan]")

        hashtags_str = " ".join(campaign.hashtags) if campaign.hashtags else "No especificados"
        extra = campaign.extra_notes or "Ninguna"

        user_prompt = COPY_PROMPT.format(
            product_name=campaign.product_name,
            content_summary=prompts.content_summary,
            description=campaign.description,
            target_audience=campaign.target_audience,
            brand_tone=campaign.brand_tone,
            hashtags=hashtags_str,
            extra_notes=extra,
        )

        response = self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)

        result = GeneratedCopy(
            instagram=PlatformCopy(**data["instagram"]),
            facebook=PlatformCopy(**data["facebook"]),
            tiktok=PlatformCopy(**data["tiktok"]),
        )

        console.print("[green]✓ Copy generado para todas las plataformas[/green]")
        console.print(f"  [dim]Instagram:[/dim] {result.instagram.caption[:70]}...")
        console.print(f"  [dim]Facebook:[/dim]  {result.facebook.caption[:70]}...")
        console.print(f"  [dim]TikTok:[/dim]    {result.tiktok.caption[:70]}...")
        return result
