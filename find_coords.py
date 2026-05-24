# find_coords.py
import pyautogui
import time

print("Arahkan mouse ke posisi yang ingin diketahui koordinatnya.")
print("Tekan Ctrl+C untuk berhenti.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x:4d} | Y: {y:4d}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nSelesai.")