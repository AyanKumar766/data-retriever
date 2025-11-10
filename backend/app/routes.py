from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from .db import get_session
from . import crud, scraper, embedder
from pathlib import Path
import os

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# mount static must be done in main.py using app.mount

@router.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    items = crud.get_all_items(session, limit=200)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@router.get("/add", response_class=HTMLResponse)
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@router.post("/add", response_class=RedirectResponse)
def add_item(request: Request, url: str = Form(...), session: Session = Depends(get_session)):
    data = scraper.scrape_page(url)
    if "error" in data:
        # keep it simple, redirect back with error flash could be added
        raise HTTPException(status_code=400, detail=data["error"])
    item = crud.create_item(session, data["url"], data["title"], data["text"], data["domain"])
    # Optionally build index incrementally or leave to manual endpoint
    return RedirectResponse("/", status_code=303)

# JSON API endpoints
@router.get("/api/items")
def api_get_items(session: Session = Depends(get_session)):
    items = crud.get_all_items(session)
    return items

@router.post("/api/items")
def api_create_item(payload: dict, session: Session = Depends(get_session)):
    # expects JSON {url, title?, text?, domain?}
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing url")
    item = crud.create_item(session, url, payload.get("title"), payload.get("text"), payload.get("domain"))
    return {"status": "ok", "id": item.id}

@router.post("/api/build_index")
def api_build_index(session: Session = Depends(get_session)):
    res = embedder.build_index(session)
    return res

@router.get("/api/search")
def api_search(q: str = None, k: int = 5, session: Session = Depends(get_session)):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query 'q'")
    res = embedder.query_index(q, k)
    # Fetch full items from DB for each hit
    if "results" in res:
        hits = []
        for h in res["results"]:
            item = crud.get_item_by_id(session, h["item_id"])
            if item:
                hits.append({
                    "id": item.id,
                    "url": item.url,
                    "title": item.title,
                    "domain": item.domain,
                    "snippet": (item.text[:400] + "...") if item.text else "",
                    "score": h["score"]
                })
        return {"query": q, "results": hits}
    return res
