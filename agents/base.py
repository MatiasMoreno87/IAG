from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CampaignInput:
    """All the raw inputs provided by the user for a campaign."""
    product_name: str
    description: str
    target_audience: str
    brand_tone: str              # e.g. "profesional", "divertido", "lujoso"
    reference_image_path: Optional[str] = None
    extra_notes: Optional[str] = None
    platforms: list[str] = field(default_factory=lambda: ["instagram", "facebook", "tiktok"])
    hashtags: list[str] = field(default_factory=list)


@dataclass
class OptimizedPrompts:
    image_prompt: str
    video_prompt: str
    content_summary: str         # concise product/campaign summary for copy


@dataclass
class GeneratedImage:
    url: str                     # remote URL (fal.ai CDN)
    local_path: Optional[str] = None


@dataclass
class GeneratedVideo:
    url: str
    local_path: Optional[str] = None


@dataclass
class PlatformCopy:
    caption: str
    hashtags: str
    call_to_action: str

    @property
    def full_text(self) -> str:
        parts = [self.caption]
        if self.call_to_action:
            parts.append(self.call_to_action)
        if self.hashtags:
            parts.append(self.hashtags)
        return "\n\n".join(parts)


@dataclass
class GeneratedCopy:
    instagram: PlatformCopy
    facebook: PlatformCopy
    tiktok: PlatformCopy


@dataclass
class PublishResult:
    platform: str
    success: bool
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class CampaignOutput:
    prompts: OptimizedPrompts
    image: GeneratedImage
    video: GeneratedVideo
    copy: GeneratedCopy
    publications: list[PublishResult] = field(default_factory=list)
