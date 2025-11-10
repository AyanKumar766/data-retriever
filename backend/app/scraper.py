import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

HEADERS = {
    "User-Agent": "ai-data-retriever/0.1 (+https://github.com/AyanKumar766)"
}

def _clean_text(s: str) -> str:
    # basic cleaning
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def scrape_page(url: str, use_playwright: bool = False, max_chars: int = 20000):
    """
    Scrape a page and return {url, title, text, domain} or {'error': ...}
    If use_playwright=True you'll need playwright installed and configured.
    """
    try:
        if use_playwright:
            # optional: requires playwright installation and browsers installed
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                html = page.content()
                browser.close()
        else:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            html = resp.text

        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        # heuristics to pull main text: prefer <article>, otherwise paragraphs
        article = soup.find("article")
        if article:
            texts = [p.get_text(separator=" ", strip=True) for p in article.find_all(["p", "li"])]
        else:
            texts = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
            # fallback to large <div> blocks if no <p>
            if not texts:
                divs = soup.find_all("div")
                texts = sorted([d.get_text(separator=" ", strip=True) for d in divs], key=len, reverse=True)[:3]

        text = " ".join(t for t in texts if t)
        text = _clean_text(text)
        if not text:
            # fallback: body text
            body = soup.body.get_text(separator=" ", strip=True) if soup.body else ""
            text = _clean_text(body)

        domain = urlparse(url).netloc
        return {
            "url": url,
            "title": title or domain,
            "text": text[:max_chars],
            "domain": domain
        }
    except Exception as e:
        return {"error": str(e)}
