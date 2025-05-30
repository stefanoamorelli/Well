# AI model configuration

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG_PATH = Path("config/models.yaml")
REQUIRED_OPENAI_IMAGE_FIELDS = ["model", "size", "quality"]

def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to read config file ({path}): {e}")
        return {}

def validate_config(config: dict) -> bool:
    """
    Checks that the openai_image section contains the required fields.
    """
    image_config = config.get("openai_image", {})
    missing = [key for key in REQUIRED_OPENAI_IMAGE_FIELDS if key not in image_config]

    if missing:
        print(f"❌ Missing fields in openai_image: {', '.join(missing)}")
        return False

    return True

def resolve_api_key(config: dict, model_key: str) -> str:
    """
    Returns the API key from config[model_key].api_key or fallback to .env.
    """
    settings = config.get(model_key, {})
    return settings.get("api_key") or os.getenv("OPENAI_API_KEY")
