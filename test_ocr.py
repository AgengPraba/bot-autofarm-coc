# test_ocr.py
import cv2
import time
from screen import capture_screen
from config import LOOT_REGIONS
from ocr import read_loot

print("Buka layar battle CoC (yang ada angka loot), lalu...")
print("Screenshot diambil dalam 5 detik...")
time.sleep(5)

screen = capture_screen()
print("\nMembaca loot:")
loot = read_loot(screen, LOOT_REGIONS)
print(f"\nHasil:")
print(f"  Gold        : {loot.get('gold', 0):,}")
print(f"  Elixir      : {loot.get('elixir', 0):,}")
print(f"  Dark Elixir : {loot.get('dark_elixir', 0):,}")