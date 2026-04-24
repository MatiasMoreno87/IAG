# Social Media Automation Agent

Pipeline multi-agente que genera y publica contenido de redes sociales con IA de punta a punta.

## Flujo del pipeline

```
Entrada (briefing + imagen de referencia)
        │
        ▼
┌───────────────────┐
│  Agent 1          │  Claude Vision analiza la imagen y el briefing
│  Prompt Optimizer │  → genera prompts optimizados para imagen y video
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Agent 2          │  fal.ai Flux Pro genera imagen mockup
│  Image Generator  │  del producto en alta calidad
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Agent 3          │  fal.ai Kling convierte la imagen en video
│  Video Generator  │  promocional dinámico (5-10 seg)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Agent 4          │  Claude genera copy persuasivo y de venta
│  Copy Writer      │  adaptado a Instagram, Facebook y TikTok
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Agent 5          │  Publica imagen + video + copy en
│  Social Publisher │  Instagram · Facebook · TikTok
└───────────────────┘
```

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus API keys
```

## Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key |
| `FAL_KEY` | fal.ai API key (imagen y video) |
| `INSTAGRAM_USER_ID` | ID de cuenta Instagram Business/Creator |
| `INSTAGRAM_ACCESS_TOKEN` | Token de larga duración de Instagram |
| `FACEBOOK_PAGE_ID` | ID de la Página de Facebook |
| `FACEBOOK_ACCESS_TOKEN` | Page Access Token de Facebook |
| `TIKTOK_ACCESS_TOKEN` | Token de TikTok Content Posting API |
| `TIKTOK_OPEN_ID` | Open ID de TikTok |
| `DRY_RUN` | `true` para probar sin publicar realmente |

## Uso

### Verificar configuración
```bash
python main.py check-config
```

### Ejecutar pipeline completo
```bash
python main.py run \
  --product "Crema Hidratante XY" \
  --description "Crema 100% natural para piel sensible, con aloe vera y vitamina E" \
  --audience "Mujeres 25-40 interesadas en skincare natural y sostenible" \
  --tone "profesional y cálido" \
  --image ./reference.jpg \
  --hashtags "#skincare #natural #belleza #cuidadodelapiel" \
  --platforms instagram facebook tiktok
```

### Dry run (sin publicar)
```bash
python main.py run --product "..." --description "..." --audience "..." --dry-run
```

### Solo algunas plataformas
```bash
python main.py run ... --platforms instagram --platforms tiktok
```

## Outputs

Cada ejecución genera en `./outputs/`:
- `mockup_<timestamp>.jpg` — imagen mockup del producto
- `promo_video_<timestamp>.mp4` — video promocional
- `report_<timestamp>.json` — reporte completo con URLs, copy y resultados

## Modelos de IA utilizados

| Agente | Modelo | Propósito |
|---|---|---|
| Prompt Optimizer | Claude claude-sonnet-4-6 + Vision | Análisis de imagen y optimización de prompts |
| Image Generator | fal.ai Flux Pro | Generación de imagen mockup |
| Video Generator | fal.ai Kling v1.6 | Generación de video image-to-video |
| Copy Writer | Claude claude-sonnet-4-6 | Copy persuasivo multi-plataforma |
| Social Publisher | Graph API + TikTok API | Publicación automatizada |

## APIs requeridas

- **Anthropic** — [console.anthropic.com](https://console.anthropic.com)
- **fal.ai** — [fal.ai](https://fal.ai) (imagen y video)
- **Facebook/Instagram** — [developers.facebook.com](https://developers.facebook.com) (Instagram Graph API)
- **TikTok** — [developers.tiktok.com](https://developers.tiktok.com) (Content Posting API)
