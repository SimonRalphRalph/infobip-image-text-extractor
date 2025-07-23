from utils.crawler import crawl_site
from utils.image_downloader import download_images
from utils.ocr import process_images
import os

BASE_URL = "https://www.infobip.com"
OUTPUT_FOLDER = "output"
IMAGES_FOLDER = os.path.join(OUTPUT_FOLDER, "images")
RESULT_CSV = os.path.join(OUTPUT_FOLDER, "results.csv")

def main():
    print("[1] Crawling site...")
    urls = crawl_site(BASE_URL)

    print(f"[2] Found {len(urls)} pages. Downloading images...")
    all_images = download_images(urls, IMAGES_FOLDER)

    print(f"[3] Running OCR on {len(all_images)} images...")
    process_images(all_images, RESULT_CSV)

    print(f"[✓] Done. Results saved to: {RESULT_CSV}")

if __name__ == "__main__":
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    main()
