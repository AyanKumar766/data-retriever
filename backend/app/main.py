from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routes import router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="AI Data Retriever")

# Static + templates mounting: static directory path
BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# CORS - allow local dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
