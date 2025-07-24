import csv
import os
import shutil
import re

INPUT = "output/results.csv"
CLEAN_CSV = "output/results_clean.csv"
DEST_DIR = "output/with_text_only_clean"

os.makedirs(DEST_DIR, exist_ok=True)

def looks_like_gibberish(text: str) -> bool:
    t = text.strip()

    # very short -> junk
    if len(t) < 12:
        return True

    # too few spaces (often random tokens)
    if t.count(" ") < 2:
        return True

    letters = sum(ch.isalpha() for ch in t)
    if letters == 0:
        return True

    ratio_letters = letters / len(t)
    if ratio_letters < 0.35:
        return True

    vowels = sum(ch.lower() in "aeiou" for ch in t)
    if vowels / letters < 0.20:  # strings with almost no vowels tend to be junk
        return True

    # lots of repeated same char (#######, ------, etc.)
    if re.search(r"(.)\1{5,}", t):
        return True

    # mostly numbers / punctuation
    digits = sum(ch.isdigit() for ch in t)
    if digits / len(t) > 0.5:
        return True

    return False

kept = 0
with open(INPUT, newline='', encoding='utf-8') as inp, \
     open(CLEAN_CSV, "w", newline='', encoding='utf-8') as outp:
    reader = csv.DictReader(inp)
    writer = csv.writer(outp)
    writer.writerow(["image_path", "detected_text"])

    for row in reader:
        path = row["image_path"]
        text = row["detected_text"]

        if not text.strip():
            continue
        if looks_like_gibberish(text):
            continue
        if not os.path.exists(path):
            continue

        # copy good image
        dest_path = os.path.join(DEST_DIR, os.path.basename(path))
        shutil.copy2(path, dest_path)

        writer.writerow([path, text])
        kept += 1

print(f"✅ Done. Kept {kept} rows. Clean CSV: {CLEAN_CSV}")
print(f"📁 Images copied to: {DEST_DIR}")
