from jinja2 import Template
from pathlib import Path
import json

def load_template(path: str) -> Template:
    with open(path, "r", encoding="utf-8") as f:
        return Template(f.read())

def generate_image_prompt(json_data: dict, style_data: dict) -> str:
    template = load_template("src/core/prompts/image_prompt_template.txt")
    return template.render(
        json_payload=json.dumps(json_data, indent=2),
        style_json=json.dumps(style_data, indent=2)
    )

if __name__ == "__main__":
    # For testing
    input_path = Path("examples/generated_receipt.json")
    if not input_path.exists():
        print("❌ Receipt JSON not found.")
    else:
        data = json.loads(input_path.read_text(encoding="utf-8"))
        prompt = generate_image_prompt(data)
        print("🧾 Generated image prompt:\n")
        print(prompt)

