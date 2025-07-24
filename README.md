# Infobip Image Text Extractor

This tool crawls a website, downloads all visible images, runs OCR on them, and saves the results for review and translation.

## 🔧 Features

- Crawls all linked pages from a given base URL
- Downloads image assets, skipping invalid or base64 blobs
- Uses Tesseract OCR to extract any visible text from images
- Outputs a CSV (`output/results.csv`) with detected text
- Optional script to isolate images containing text only

## 📁 Folder Structure

- `utils/` – contains the main scripts
  - `crawler.py` – crawls the site
  - `image_downloader.py` – handles image scraping
  - `ocr.py` – runs text extraction with Tesseract
- `output/` – contains downloaded images and final results
- `filter_text_images.py` – optional script to copy only images with OCR-detected text

## 🚀 How to Run

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
