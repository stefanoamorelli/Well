from fastapi import APIRouter, HTTPException
from pathlib import Path
import yaml, json, base64
from src.core.api.models import InputUpdate, StyleCreate, GenerationRequest
from src.core.data_generator import generate_receipt_data
from src.core.prompt_renderer import generate_image_prompt
from src.core.config_loader import load_config, validate_config
from openai import OpenAI

router = APIRouter()

CONFIG_PATH = Path("config/receipt_input.yaml")
STYLE_DIR = Path("src/core/prompts/styles")

@router.get("/current-config")
def get_current_config():
    if not CONFIG_PATH.exists():
        raise HTTPException(status_code=404, detail="receipt_input.yaml not found")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

@router.post("/update-input")
def update_input(data: InputUpdate):
    old = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
    merged = {**old, **data.fields}
    CONFIG_PATH.write_text(yaml.dump(merged, allow_unicode=True), encoding="utf-8")
    return {"message": "✅ receipt_input.yaml updated", "merged": merged}

@router.get("/styles")
def list_styles():
    return [f.stem for f in STYLE_DIR.glob("*.json")]

@router.post("/create-style")
def create_style(style: StyleCreate):
    path = STYLE_DIR / f"{style.name}.json"
    if path.exists():
        raise HTTPException(status_code=400, detail="This style already exists.")
    path.write_text(json.dumps(style.content, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"message": f"✅ New style {style.name}.json created."}

@router.post("/generate-receipt")
def generate_receipt(data: GenerationRequest):
    # Load input
    fields = data.input_fields or {}
    receipt_data = generate_receipt_data(overrides=fields)

    # Load style
    style_path = STYLE_DIR / f"{data.style}.json"
    if not style_path.exists():
        raise HTTPException(status_code=404, detail="Style not found")
    style = json.loads(style_path.read_text(encoding="utf-8"))

    # Generate prompt
    prompt = generate_image_prompt(receipt_data, style)

    # Call OpenAI API
    config = load_config()
    if not validate_config(config):
        raise HTTPException(status_code=500, detail="Invalid OpenAI configuration")

    image_cfg = config.get("openai_image", {})
    client = OpenAI()
    try:
        response = client.images.generate(
            model=image_cfg["model"],
            prompt=prompt,
            n=1,
            size=image_cfg["size"],
            quality=image_cfg["quality"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

    # Return base64 image
    return {
        "message": "✅ Image successfully generated",
        "b64_image": response.data[0].b64_json
    }
