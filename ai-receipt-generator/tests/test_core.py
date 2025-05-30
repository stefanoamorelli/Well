from core.data_generator import generate_receipt_data
from core.prompt_renderer import generate_image_prompt
from pathlib import Path
import json

def test_generate_receipt_data_structure():
    data = generate_receipt_data()
    assert isinstance(data, dict)
    assert "transaction_id" in data
    assert "merchant" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_image_prompt_generation():
    data = generate_receipt_data()
    style_path = Path("core/prompts/styles/table_noire.json")
    style = json.loads(style_path.read_text(encoding="utf-8"))
    prompt = generate_image_prompt(data, style)
    assert isinstance(prompt, str)
    assert len(prompt.strip()) > 50  # the prompt must be non-trivial
