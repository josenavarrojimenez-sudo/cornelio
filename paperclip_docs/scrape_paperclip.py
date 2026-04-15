#!/usr/bin/env python3
import requests
import json
import re
import time
from urllib.parse import urljoin

BASE_URL = "https://docs.paperclip.ing"
visited = set()
docs = {}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def fetch_page(url):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.text
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_content(html):
    html_clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html_clean = re.sub(r'<style[^>]*>.*?</style>', '', html_clean, flags=re.DOTALL)
    
    content = []
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        content.append(f"# {title_match.group(1)}")
    
    for pattern in [
        r'<h1[^>]*>([^<]+)</h1>',
        r'<h2[^>]*>([^<]+)</h2>',
        r'<h3[^>]*>([^<]+)</h3>',
        r'<p[^>]*>([^<]+)</p>',
        r'<li[^>]*>([^<]+)</li>',
        r'<code[^>]*>([^<]+)</code>',
    ]:
        matches = re.findall(pattern, html_clean, flags=re.DOTALL)
        for match in matches:
            match = re.sub(r'<[^>]+>', '', match)
            match = match.strip()
            if len(match) > 10:
                content.append(match)
    
    return "\n\n".join(content)

key_paths = [
    "/",
    "/api-reference/introduction",
    "/api-reference/authentication",
    "/api-reference/agents",
    "/guides/permissions",
    "/guides/api-keys",
    "/guides/roles",
]

print("=" * 70)
print("SCRAPING DOCUMENTACION PAPERCLIP")
print("=" * 70)

for path in key_paths:
    url = urljoin(BASE_URL, path)
    if url in visited:
        continue
    visited.add(url)
    
    print(f"\nFetching: {url}")
    html = fetch_page(url)
    
    if html:
        content = extract_content(html)
        docs[path] = {
            "url": url,
            "content": content[:50000] if len(content) > 50000 else content,
            "size": len(content)
        }
        print(f"   Extraido: {len(content)} caracteres")
    else:
        print(f"   No se pudo obtener")
    
    time.sleep(0.5)

with open("/root/.openclaw/workspace/paperclip_docs/scraped_docs.json", "w") as f:
    json.dump(docs, f, indent=2)

print("\n" + "=" * 70)
print(f"COMPLETADO: {len(docs)} paginas extraidas")
print("=" * 70)
