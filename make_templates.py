# make_templates.py
import cv2
import time
from screen import capture_screen

def select_roi(window_name, img):
    """
    Buka jendela, user drag-select area template.
    Tekan SPACE atau ENTER untuk konfirmasi, C untuk cancel.
    """
    print(f"  → Drag kotak di area '{window_name}'")
    print(f"     Tekan SPACE/ENTER untuk simpan, C untuk ulangi\n")
    
    # Resize tampilan agar muat di layar (tapi crop tetap dari ukuran asli)
    display = cv2.resize(img, (900, 550))
    scale_x = img.shape[1] / 900
    scale_y = img.shape[0] / 550
    
    roi = cv2.selectROI(window_name, display, showCrosshair=True)
    cv2.destroyAllWindows()
    
    if roi == (0, 0, 0, 0):
        return None
    
    # Konversi koordinat display balik ke koordinat asli
    x = int(roi[0] * scale_x)
    y = int(roi[1] * scale_y)
    w = int(roi[2] * scale_x)
    h = int(roi[3] * scale_y)
    
    return img[y:y+h, x:x+w]

# ─────────────────────────────────────
# MULAI
# ─────────────────────────────────────
templates_needed = [
    ("attack_button", "HOME SCREEN — Crop tombol 'Attack!'"),
    ("find_match",    "ATTACK SCREEN — Crop tombol 'Find a Match'"),
    ("next_button",   "BATTLE SCREEN — Crop tombol 'Next'"),
    ("return_home",   "RESULT SCREEN — Crop tombol 'Return Home'"),
]

print("=" * 50)
print("TOOL PEMBUATAN TEMPLATE")
print("=" * 50)
print()
print("Cara pakai:")
print("1. Script akan ambil screenshot")
print("2. Jendela terbuka — drag kotak di sekitar tombol")
print("3. Tekan SPACE atau ENTER untuk simpan")
print("4. Ulangi untuk setiap tombol")
print()

for filename, instruksi in templates_needed:
    print(f"{'─'*50}")
    print(f"Template  : {filename}.png")
    print(f"Instruksi : {instruksi}")
    print()
    
    input(f"Siapkan layar CoC ke posisi yang benar, lalu tekan ENTER...")
    
    print("Screenshot dalam 3 detik...")
    time.sleep(3)
    
    screen = capture_screen()
    
    cropped = select_roi(filename, screen)
    
    if cropped is not None and cropped.size > 0:
        path = f"templates/{filename}.png"
        cv2.imwrite(path, cropped)
        h, w = cropped.shape[:2]
        print(f"✅ Disimpan ke {path} ({w}x{h}px)\n")
    else:
        print(f"❌ Tidak ada area yang dipilih, skip.\n")

print("=" * 50)
print("Selesai! Jalankan python diagnose.py untuk verifikasi.")