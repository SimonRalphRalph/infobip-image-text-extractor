from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

def crawl_site(start_url, max_pages=100):
    visited = set()
    to_visit = [start_url]
    all_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            try:
                page.goto(url, timeout=15000)
                page_content = page.content()
                visited.add(url)
                all_urls.append(url)
                soup = BeautifulSoup(page_content, "lxml")

                for link in soup.find_all("a", href=True):
                    full_url = urljoin(url, link["href"])
                    if is_valid_url(full_url, start_url) and full_url not in visited:
                        to_visit.append(full_url)

            except Exception as e:
                print(f"❌ Failed to crawl {url}: {e}")

        browser.close()

    return all_urls

def is_valid_url(url, base):
    return url.startswith(base) and urlparse(url).scheme in ["http", "https"]
