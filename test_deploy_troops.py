# test_deploy_troops.py
import time
import pyautogui
from bot import CoCBot

print("Test deploy dalam 5 detik...")
print("Pastikan kamu sudah di layar battle (setelah klik attack)!")
time.sleep(5)

bot = CoCBot()
bot.deploy_troops()
print("Selesai!")