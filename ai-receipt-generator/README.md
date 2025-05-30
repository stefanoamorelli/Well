# 📟 receipt-gen-ai

> Generator of realistic fake receipts (text + image) from structured data.
> Uses Faker for synthetic data, custom image prompts, and DALL·E 3 (GPT-Image) for visual generation.

---

## 📂 Project Overview

This project allows you to:

* Automatically generate a **structured fake receipt** in JSON format
* Transform it into a coherent image prompt (like a scanned receipt)
* Call **OpenAI GPT-Image (gpt-image-1)** to generate a **realistic receipt photo**
* Use it via **CLI** or **REST API (optional)**

---

## 🌐 Installation

### 1. Clone the repository

```bash
git clone https://github.com/WellApp-ai/Well.git
cd ai-receipt-generator
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -e .[dev]
```

### 4.Create a .env file at the project root

> Inside the .env file, add your API keys (you can include one or both):

```text
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```
> These keys will be automatically loaded if you use the .env approach.

---

## 🔧 Usage (CLI)

### Generate a receipt image using a style

```bash
python src/core/cli.py --style table_noire
```

Available options:

* `--input-path`: YAML or JSON file containing the data (merged into `receipt_input.yaml`)
* `--style`: visual style name from `prompts/styles/` (without `.json`)
* `--output-path`: path to export the generated prompt as `.txt`
* `--save-image`: whether to save the PNG image (default: yes)
* `--open-image`: whether to automatically open the PNG file

---

## 🔎 Quick Example

```bash
python src/core/cli.py --style table_noire
```

* Prompt exported to: `exports/prompt_for_chatgpt.txt`
* Image saved to: `exports/receipt_generated.png`

---

## 📁 Project Structure

```txt
ai-receipt-generator/
├── src/ 
│    └── core/
│       ├── data_generator.py         # Generate JSON data (Faker)
│       ├── prompt_renderer.py        # Inject data into image prompt
│       ├── cli.py                    # Main CLI entry point (Typer)
│       ├── config_loader.py          # Load models.yaml
│       ├── generators/
│       │   ├── base.py
│       │   └── openai_generator.py
│       │   └── anthropic_generator.py
│       ├── prompts/
│       │   ├── image_prompt_template.txt
│       │   └── styles/
│       │       └── table_noire.json
│       ├── api/                      # (Optional)
│       │   ├── app.py                # FastAPI app
│       │   ├── router.py
│       │   ├── models.py
├── config/
│   └── receipt_input.yaml        # Editable fields (merchant, total, items, etc.)
├── exports/
│   ├── prompt_for_chatgpt.txt
│   └── receipt_generated.png
├── examples/
│   └── generated_receipt.json
├── tests/
│   └── test_core.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
```

---

## ⚙️ Configuration Files

### `config/models.yaml`

Defines the models used:

```yaml
openai_image:
  model: gpt-image-1
  size: 1024x1024
  quality: high
```

> This file is loaded automatically. You can edit it to change the model, image size, or quality.

### `config/receipt_input.yaml`

You can pre-fill some fields here:

```yaml
merchant_name: Starbucks
transaction_date_time: 2025-05-21T15:00:00Z
ttc: 12.90
items:
  - description: Latte
    unit_price: 3.20
    quantity: 2
```

Unspecified fields are randomly generated using Faker.

---

## 🎯 REST API (optional)

You can expose the engine via FastAPI:

```bash
uvicorn core.api.app:app --reload
```

### Available endpoints:

| URL                 | Method | Description                                |
| ------------------- | ------ | ------------------------------------------ |
| `/current-config`   | GET    | Returns the current `receipt_input.yaml`   |
| `/update-input`     | POST   | Updates the `receipt_input.yaml` file      |
| `/styles`           | GET    | Lists available visual styles              |
| `/create-style`     | POST   | Adds a new style JSON file                 |
| `/generate-receipt` | POST   | Generates an image prompt and base64 image |

---

## 🔾 Server Launch Options

### ▶️ Option 1 — Using included `run.bat` (Windows)

```bash
./run.bat
```

This will:

* Activate the virtual environment
* Set `PYTHONPATH=src`
* Launch the FastAPI app with hot-reload

---

### ▶️ Option 2 — Using `run_api.sh` (macOS/Linux)

```bash
chmod +x run_api.sh
./run_api.sh
```

Same behavior as above: activates your venv, sets the path, and launches the API.

---

### ▶️ Option 3 — Manual launch

```bash
uvicorn core.api.app:app --reload --reload-dir=src --app-dir=src
```

Make sure you are in the project root and that the `venv` is activated.

---

### 🔐 Authentication

This project requires access to OpenAI API.

You can set your key either:

* In a `.env` file (recommended)

```env
OPENAI_API_KEY=sk-xxx
```

* Or directly inside `config/models.yaml` under `openai_image.api_key`

---

## 🧪 Testing

```bash
pytest
```

* Tests the JSON structure
* Verifies that the generated image prompt is not empty

---

## 💎 Extras

* You can create your own visual styles in `prompts/styles/*.json`
* You can infinitely customize the data fields
* The project is modular: everything is organized by role

---

## 📄 License

MIT

> Created by Pierre Ribeiro. Free to use and contribute.
