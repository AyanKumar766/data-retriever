from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import json

class WebItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    title: Optional[str] = None
    text: Optional[str] = None
    domain: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")  # new, processed, failed
    meta: Optional[str] = None  # JSON string if needed

    def meta_dict(self):
        if self.meta:
            try:
                return json.loads(self.meta)
            except Exception:
                return {}
        return {}
