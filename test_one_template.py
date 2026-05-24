# test_one_template.py
import cv2
import time
import sys
from screen import capture_screen
from screen import find_template

if len(sys.argv) < 2:
    print("Usage: python test_one_template.py <nama_template>")
    print("Contoh: python test_one_template.py next_button")
    sys.exit(1)

nama = sys.argv[1]
path = f"templates/{nama}.png"

print(f"Test template: {nama}")
print(f"Siapkan layar CoC ke scene yang benar...")
print(f"Screenshot dalam 5 detik...")
time.sleep(5)

screen = capture_screen()

# Cek manual confidence
template = cv2.imread(path)
if template is None:
    print(f"❌ File tidak ditemukan: {path}")
    sys.exit(1)

screen_gray   = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

print(f"Confidence: {max_val:.3f}")

if max_val >= 0.8:
    h, w = template_gray.shape
    # Tandai di screenshot
    cv2.rectangle(screen, max_loc,
                  (max_loc[0]+w, max_loc[1]+h),
                  (0, 255, 0), 3)
    cx, cy = max_loc[0] + w//2, max_loc[1] + h//2
    cv2.circle(screen, (cx, cy), 8, (0,0,255), -1)
    print(f"✅ DITEMUKAN di X:{cx}, Y:{cy}")
else:
    print(f"❌ Tidak ditemukan — perlu crop ulang")

cv2.imwrite(f"test_{nama}_result.png", screen)
print(f"Hasil disimpan ke test_{nama}_result.png")