# 👨‍💻 Contributing

This document is intended for developers who want to contribute to the `receipt-gen-ai` project, add new features, or integrate it with other tools.

---

## ⚙️ Local Development Setup

```bash
git clone https://github.com/yourusername/receipt-gen-ai.git
cd receipt-gen-ai
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
pip install -e .[dev]
```

### 🔐 Create a `.env` file at the project root

Set your API keys:

```bash
echo "OPENAI_API_KEY=your-openai-api-key" >> .env
echo "ANTHROPIC_API_KEY=your-anthropic-api-key" >> .env
```

---

## 🧪 Run Tests

```bash
pytest
```

All tests are located in the `tests/` folder. They cover:

* Validity of the generated JSON (`generate_receipt_data()`)
* Rendering of the image prompt (`generate_image_prompt()`)

---

## 🗂 Project Structure

```
receipt-gen-ai/
├── src/ 
│    └── core/
│       ├── data_generator.py         # Generate JSON data (Faker)
│       ├── prompt_renderer.py        # Inject data into image prompt
│       ├── cli.py                    # Main CLI entry point (Typer)
│       ├── config_loader.py          # Load model.yaml
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

## 🧠 Add a New Style

Create a `.json` file in `prompts/styles/`, e.g. `light_wood.json`

```json
{
  "style": "Photo-realistic thermal receipt",
  "background": "light wood table",
  "camera_angle": "top-down",
  "text_legibility": "fully readable text"
}
```

Then run it via:

```bash
python src/core/cli.py --style light_wood
```

---

## 🌐 API Development (Optional)

```bash
uvicorn core.api.app:app --reload
```

Routes are defined in `api/router.py` and typed in `api/models.py`.

---

## ▶️ Run the API with helper scripts

Instead of manually launching the API, you can use the included scripts:

### Windows

```bash
run.bat
```

### macOS / Linux

```bash
chmod +x run.sh
./run.sh
```

These scripts:
- Activate the virtual environment
- Set `PYTHONPATH` to `src`
- Launch the FastAPI app with hot-reload

---

## 🧰 Useful Commands

* Auto-formatting: `black .`
* Strict install: `pip install --no-cache-dir -e .[dev]`
* Full reinstall:

```bash
rm -rf venv __pycache__ .pytest_cache exports/*.png
python -m venv venv && source venv/bin/activate && pip install -e .[dev]
```

---

## 🚀 Create a Release

1. Clean generated files  
2. Delete `.env`, `exports/`, caches  
3. Make sure `pyproject.toml` is updated  
4. Push and create a GitHub release  

---

## 📦 Build Wheel (Optional)

```bash
python -m build
```

---

## 🤝 Internal Conventions

* Code is Python 3.10+
* No prefixes like `00_`, `a_`, etc. in file/module names
* `.txt` prompts = injected text / `.json` = visual parameters

---

## 🧾 Example: Web Integration

The REST API allows you to:

* Dynamically update the input YAML
* Switch visual styles (JSON)
* Generate a realistic receipt image

---

## 👤 Author / Contact

* Pierre Ribeiro  
* [https://github.com/RibHero]

> Please respect the license and submit improvements via PR 🙌
