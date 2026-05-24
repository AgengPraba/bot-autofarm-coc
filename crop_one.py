# crop_one.py
import cv2
import time
import sys
from screen import capture_screen

nama = sys.argv[1] if len(sys.argv) > 1 else "template"

print(f"Crop template: {nama}")
print(f"Siapkan layar CoC ke scene yang benar...")
print(f"Screenshot dalam 5 detik...")
time.sleep(5)

screen = capture_screen()

# Resize untuk display
display = cv2.resize(screen, (900, 550))
scale_x = screen.shape[1] / 900
scale_y = screen.shape[0] / 550

print("Drag kotak di tombol, tekan SPACE/ENTER untuk simpan...")
roi = cv2.selectROI(nama, display, showCrosshair=True)
cv2.destroyAllWindows()

if roi != (0, 0, 0, 0):
    x = int(roi[0] * scale_x)
    y = int(roi[1] * scale_y)
    w = int(roi[2] * scale_x)
    h = int(roi[3] * scale_y)
    
    cropped = screen[y:y+h, x:x+w]
    path = f"templates/{nama}.png"
    cv2.imwrite(path, cropped)
    print(f"✅ Disimpan: {path} ({w}x{h}px)")
else:
    print("❌ Tidak ada yang dipilih")