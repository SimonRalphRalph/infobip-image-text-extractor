import pytesseract
from PIL import Image
import os
import csv

def process_images(image_paths, output_csv):
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["image_path", "detected_text"])

        for path in image_paths:
            try:
                img = Image.open(path)
                text = pytesseract.image_to_string(img)
                text = text.strip()
                if text:
                    writer.writerow([path, text])
            except Exception as e:
                print(f"❌ Failed to process {path}: {e}")
