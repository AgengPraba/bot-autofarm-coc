# ocr.py
import cv2
import numpy as np
import pytesseract
from PIL import Image

def preprocess_for_ocr(img):
    """
    Proses gambar agar angka lebih mudah dibaca Tesseract.
    """
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Perbesar 2x — Tesseract lebih akurat pada gambar lebih besar
    scaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Threshold — pisahkan angka dari background
    _, thresh = cv2.threshold(scaled, 140, 255, cv2.THRESH_BINARY_INV)
    
    return thresh

def read_number(img):
    """
    Baca angka dari gambar, return integer.
    Return 0 jika gagal dibaca.
    """
    processed = preprocess_for_ocr(img)
    pil_img   = Image.fromarray(processed)
    
    # --psm 7 = satu baris teks, digits = hanya angka
    raw = pytesseract.image_to_string(
        pil_img,
        config="--psm 7 -c tessedit_char_whitelist=0123456789"
    )
    
    cleaned = ''.join(filter(str.isdigit, raw))
    return int(cleaned) if cleaned else 0

def read_loot(screen, loot_regions):
    """
    Baca semua resource (gold, elixir, dark elixir) dari layar.
    Return dict berisi nilai masing-masing.
    """
    result = {}
    
    for resource, region in loot_regions.items():
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        cropped     = screen[y:y+h, x:x+w]
        nilai       = read_number(cropped)
        result[resource] = nilai
        print(f"  {resource:12s}: {nilai:,}")
    
    return result