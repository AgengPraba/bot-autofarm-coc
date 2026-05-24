# test_bot.py
import time
import cv2
from screen import capture_screen, find_template
from config import TEMPLATES

print("Screenshot dalam 3 detik, pindah ke home screen CoC...")
time.sleep(3)

screen = capture_screen()

for nama, path in TEMPLATES.items():
    pos = find_template(screen, path)
    if pos:
        print(f"✅ {nama:15s} → ditemukan di X:{pos[0]}, Y:{pos[1]} (confidence: {pos[2]:.2f})")
        # Tandai posisi di screenshot
        cv2.circle(screen, (pos[0], pos[1]), 15, (0,255,0), 3)
    else:
        print(f"❌ {nama:15s} → TIDAK ditemukan")

cv2.imwrite("test_template_result.png", screen)
print("\nHasil disimpan ke test_template_result.png")