# diagnose.py
import cv2
import time
from screen import capture_screen
from config import TEMPLATES

print("Screenshot dalam 3 detik, pindah ke home screen CoC...")
time.sleep(3)

screen = capture_screen()
cv2.imwrite("diagnose_screen.png", screen)
print("Screenshot layar disimpan ke diagnose_screen.png")
print()

# Cek setiap template
for nama, path in TEMPLATES.items():
    template = cv2.imread(path)
    if template is None:
        print(f"❌ {nama} — file tidak bisa dibaca!")
        continue

    th, tw = template.shape[:2]
    sh, sw = screen.shape[:2]
    print(f"📋 {nama}")
    print(f"   Template ukuran : {tw} x {th} px")
    print(f"   Screen ukuran   : {sw} x {sh} px")

    # Coba matching dengan threshold sangat rendah dulu
    screen_gray   = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"   Confidence terbaik: {max_val:.3f}  ← minimal 0.8 untuk match")

    if max_val > 0.5:
        print(f"   ⚠️  Hampir match di X:{max_loc[0]}, Y:{max_loc[1]}")
        # Tandai di screenshot
        h, w = template_gray.shape
        top_left = max_loc
        bottom_right = (max_loc[0]+w, max_loc[1]+h)
        cv2.rectangle(screen, top_left, bottom_right, (0,255,0), 2)
    elif max_val > 0.3:
        print(f"   ⚠️  Match lemah — kemungkinan ukuran/resolusi berbeda")
    else:
        print(f"   ❌ Tidak match sama sekali — template mungkin salah gambar")
    print()

cv2.imwrite("diagnose_result.png", screen)
print("Hasil disimpan ke diagnose_result.png")