import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from playwright.sync_api import sync_playwright

def download_images(urls, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    downloaded = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in tqdm(urls, desc="Downloading images from pages"):
            try:
                page.goto(url, timeout=15000)
                html = page.content()
                soup = BeautifulSoup(html, "lxml")
                img_tags = soup.find_all("img")

                for img in img_tags:
                    img_url = img.get("src")

                    # ✅ SKIP base64 images right away
                    if not img_url:
                        continue
                    if img_url.startswith("data:") or img_url.startswith("blob:") or img_url.startswith("javascript:") or "://" not in img_url:
                        continue

                    full_url = urljoin(url, img_url)
                    filename = get_filename_from_url(full_url)

                    try:
                        img_data = requests.get(full_url, timeout=10).content
                        filepath = os.path.join(output_folder, filename)
                        with open(filepath, "wb") as f:
                            f.write(img_data)
                        downloaded.append(filepath)
                    except Exception as e:
                        print(f"❌ Failed to download {full_url}: {e}")

            except Exception as e:
                print(f"❌ Error loading page {url}: {e}")

        browser.close()

    return downloaded

def get_filename_from_url(url):
    path = urlparse(url).path
    return os.path.basename(path) or "image.jpg"
