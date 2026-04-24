import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # Anthropic
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = "claude-sonnet-4-6"

    # fal.ai
    fal_key: str = field(default_factory=lambda: os.getenv("FAL_KEY", ""))
    image_model: str = "fal-ai/flux-pro"
    video_model: str = "fal-ai/kling-video/v1.6/standard/image-to-video"

    # Instagram
    instagram_user_id: str = field(default_factory=lambda: os.getenv("INSTAGRAM_USER_ID", ""))
    instagram_access_token: str = field(default_factory=lambda: os.getenv("INSTAGRAM_ACCESS_TOKEN", ""))

    # Facebook
    facebook_page_id: str = field(default_factory=lambda: os.getenv("FACEBOOK_PAGE_ID", ""))
    facebook_access_token: str = field(default_factory=lambda: os.getenv("FACEBOOK_ACCESS_TOKEN", ""))

    # TikTok
    tiktok_access_token: str = field(default_factory=lambda: os.getenv("TIKTOK_ACCESS_TOKEN", ""))
    tiktok_open_id: str = field(default_factory=lambda: os.getenv("TIKTOK_OPEN_ID", ""))

    # General
    output_dir: Path = field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "./outputs")))
    dry_run: bool = field(default_factory=lambda: os.getenv("DRY_RUN", "false").lower() == "true")

    # Graph API version
    graph_api_version: str = "v19.0"

    def __post_init__(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.fal_key:
            os.environ["FAL_KEY"] = self.fal_key

    def validate(self) -> list[str]:
        """Return list of missing required config keys."""
        missing = []
        if not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")
        if not self.fal_key:
            missing.append("FAL_KEY")
        if not self.dry_run:
            if not self.instagram_user_id:
                missing.append("INSTAGRAM_USER_ID")
            if not self.instagram_access_token:
                missing.append("INSTAGRAM_ACCESS_TOKEN")
            if not self.facebook_page_id:
                missing.append("FACEBOOK_PAGE_ID")
            if not self.facebook_access_token:
                missing.append("FACEBOOK_ACCESS_TOKEN")
            if not self.tiktok_access_token:
                missing.append("TIKTOK_ACCESS_TOKEN")
        return missing


settings = Settings()
