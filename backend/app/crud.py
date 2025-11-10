from sqlmodel import select
from .models import WebItem
from sqlmodel import Session

def create_item(session: Session, url: str, title: str = None, text: str = None, domain: str = None, meta: dict = None):
    import json
    item = WebItem(url=url, title=title, text=text, domain=domain, meta=json.dumps(meta or {}))
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def get_all_items(session: Session, limit: int = 100):
    statement = select(WebItem).order_by(WebItem.scraped_at.desc()).limit(limit)
    return session.exec(statement).all()

def get_item_by_id(session: Session, item_id: int):
    statement = select(WebItem).where(WebItem.id == item_id)
    return session.exec(statement).first()

def get_items_with_text(session: Session):
    statement = select(WebItem).where(WebItem.text != None)
    return session.exec(statement).all()

def update_status(session: Session, item_id: int, status: str):
    item = get_item_by_id(session, item_id)
    if item:
        item.status = status
        session.add(item)
        session.commit()
        session.refresh(item)
    return item
