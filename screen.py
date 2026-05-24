# screen.py
import cv2
import numpy as np
from mss import mss
import pyautogui

def capture_screen():
    """
    Ambil screenshot seluruh layar utama.
    Mengembalikan gambar dalam format BGR (standar OpenCV).
    """
    with mss() as sct:
        monitor = sct.monitors[1]  # monitor utama
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def capture_region(x, y, w, h):
    """
    Ambil screenshot sebagian layar saja.
    Berguna untuk crop area loot agar OCR lebih cepat.
    """
    with mss() as sct:
        region = {"left": x, "top": y, "width": w, "height": h}
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def find_template(screen, template_path, threshold=0.8):
    """
    Cari gambar template di dalam screenshot.
    
    Return: (center_x, center_y, confidence) jika ditemukan
            None jika tidak ditemukan
    """
    template = cv2.imread(template_path)

    if template is None:
        print(f"[ERROR] Template tidak ditemukan: {template_path}")
        return None

    # Konversi ke grayscale — matching lebih cepat & tidak sensitif warna
    screen_gray   = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = template_gray.shape
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y, max_val)

    return None


def get_screen_size():
    """Ambil ukuran layar — dipakai untuk hitung titik deploy."""
    width, height = pyautogui.size()
    return width, height