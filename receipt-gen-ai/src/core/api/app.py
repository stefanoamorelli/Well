from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.api.router import router

app = FastAPI(
    title="🧾 Receipt Gen AI",
    description=(
        "REST API for generating realistic receipts (text + image) from structured data.\n\n"
        "Allows customization of data, styles, and visual receipt generation via OpenAI GPT-image."
    ),
    version="1.0.0",
    contact={
        "name": "XXX XXXX",
        "email": "contact@example.com"
    },
    docs_url="/",             # ✅ Swagger UI served at root
    redoc_url="/redoc"        # ✅ Optional ReDoc UI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["AI Receipt Endpoints"])
