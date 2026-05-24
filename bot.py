# bot.py
import time
import random
import pyautogui
from screen import capture_screen, find_template
from config import (
    TEMPLATES, LOOT_THRESHOLD, LOOT_REGIONS,
    BATTLE_DURATION, TROOP_TRAIN_WAIT,
    CLICK_DELAY_MIN, CLICK_DELAY_MAX,
    get_deploy_points
)
from ocr import read_loot

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.1


class CoCBot:

    def __init__(self):
        self.state        = "HOME"
        self.attacks_done = 0
        self.got_star     = False   # track apakah dapat bintang
        self.deploy_pts   = get_deploy_points()
        print("🤖 Bot initialized")
        print(f"   Threshold gold        : {LOOT_THRESHOLD['gold']:,}")
        print(f"   Threshold elixir      : {LOOT_THRESHOLD['elixir']:,}")
        print(f"   Threshold dark elixir : {LOOT_THRESHOLD['dark_elixir']:,}")
        print()

    # ─────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────
    def click(self, x, y, jitter=4):
        x = x + random.randint(-jitter, jitter)
        y = y + random.randint(-jitter, jitter)
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.3))
        pyautogui.click()
        time.sleep(random.uniform(CLICK_DELAY_MIN, CLICK_DELAY_MAX))

    def click_template(self, template_key, screen):
        pos = find_template(screen, TEMPLATES[template_key])
        if pos:
            print(f"  ✅ '{template_key}' ditemukan, klik...")
            self.click(pos[0], pos[1])
            return True
        return False

    def find(self, template_key, screen):
        """Cari template tanpa klik, return posisi atau None."""
        return find_template(screen, TEMPLATES[template_key])

    def random_wait(self, min_sec, max_sec):
        duration = random.uniform(min_sec, max_sec)
        print(f"  ⏳ Tunggu {duration:.1f} detik...")
        time.sleep(duration)

    def is_loot_worth_attacking(self, screen):
        print("  📊 Membaca loot...")
        loot = read_loot(screen, LOOT_REGIONS)

        gold        = loot.get("gold", 0)
        elixir      = loot.get("elixir", 0)
        dark_elixir = loot.get("dark_elixir", 0)

        layak = (
            gold        >= LOOT_THRESHOLD["gold"]        or
            elixir      >= LOOT_THRESHOLD["elixir"]      or
            dark_elixir >= LOOT_THRESHOLD["dark_elixir"]
        )

        status = "✅ LAYAK" if layak else "❌ SKIP"
        print(f"  {status} — Gold: {gold:,} | Elixir: {elixir:,} | Dark: {dark_elixir:,}")
        return layak

    def deploy_troops(self):
        print("  ⚔️  Deploy pasukan...")
        order = ["top", "right", "bottom", "left"]
        for side in order:
            points = self.deploy_pts[side]
            print(f"    → Sisi {side} ({len(points)} titik)")
            for (x, y) in points:
                self.click(x, y, jitter=6)
                time.sleep(0.12)
        print("  ✅ Semua pasukan ter-deploy")

    def check_star(self, screen):
        """
        Deteksi apakah sudah dapat bintang dari warna
        bintang yang menyala di layar battle.
        Cek keberadaan end_button sebagai indikator dapat bintang.
        """
        pos = self.find("end_button", screen)
        return pos is not None

    # ─────────────────────────────────────
    # STATES
    # ─────────────────────────────────────
    def state_home(self, screen):
        """
        Step 1: Klik tombol Attack di home screen.
        """
        print("[HOME] Mencari tombol Attack...")
        if self.click_template("attack_button", screen):
            self.random_wait(1, 2)
            self.state = "FIND_MATCH"
        else:
            print("[HOME] Tombol Attack tidak ditemukan, tunggu...")
            self.random_wait(2, 3)

    def state_find_match(self, screen):
        """
        Step 2: Klik tombol Find a Match.
        """
        print("[FIND_MATCH] Mencari tombol Find a Match...")
        if self.click_template("find_match", screen):
            self.random_wait(2, 3)
            self.state = "ATTACK_2"
        else:
            print("[FIND_MATCH] Tidak ditemukan, kembali ke HOME...")
            self.state = "HOME"
            self.random_wait(2, 3)

    def state_attack_2(self, screen):
        """
        Step 3: Klik tombol Attack ke-2 (konfirmasi).
        """
        print("[ATTACK_2] Mencari tombol Attack ke-2...")
        if self.click_template("attack_2_button", screen):
            self.random_wait(2, 4)  # tunggu base musuh load
            self.state = "CHECK_LOOT"
        else:
            print("[ATTACK_2] Tidak ditemukan, tunggu...")
            self.random_wait(1, 2)

    def state_check_loot(self, screen):
        """
        Step 4: Cek loot base musuh.
        - Jika layak → deploy troops
        - Jika tidak → klik Next
        """
        print("[CHECK_LOOT] Mengecek loot base musuh...")

        # Pastikan sudah di layar preview base (next_button harus ada)
        if not self.find("next_button", screen):
            print("[CHECK_LOOT] Layar belum siap, tunggu...")
            self.random_wait(1, 2)
            return

        if self.is_loot_worth_attacking(screen):
            self.got_star = False   # reset flag bintang
            self.state    = "DEPLOY"
        else:
            print("[CHECK_LOOT] Loot kurang, cari base lain...")
            self.click_template("next_button", screen)
            self.random_wait(1, 2)
            # Tetap di state CHECK_LOOT untuk base berikutnya

    def state_deploy(self, screen):
        """
        Step 4 (lanjut): Deploy semua pasukan.
        """
        print("[DEPLOY] Mulai deploy pasukan!")
        self.deploy_troops()
        self.random_wait(2, 3)
        self.state = "BATTLE"

    def state_battle(self, screen):
        """
        Step 5: Monitor battle.
        - Jika dapat bintang (end_button muncul) → klik end_button
        - Jika belum dapat bintang setelah timeout → klik surrender
        """
        print("[BATTLE] Monitoring battle...")

        # Cek apakah end_button muncul (dapat bintang)
        if self.check_star(screen):
            print("[BATTLE] ⭐ Dapat bintang! Klik End Battle...")
            self.click_template("end_button", screen)
            self.got_star = True
            self.random_wait(1, 2)
            self.state = "OKAY"
            return

        # Cek apakah surrender_button muncul
        if self.find("surrender_button", screen):
            print("[BATTLE] ⏱️  Belum dapat bintang, surrender...")
            self.click_template("surrender_button", screen)
            self.random_wait(1, 2)
            self.state = "OKAY"
            return

        # Battle masih berjalan, tunggu
        print("[BATTLE] Battle masih berjalan, tunggu 5 detik...")
        time.sleep(5)

    def state_okay(self, screen):
        """
        Step 6: Klik tombol Okay setelah battle.
        """
        print("[OKAY] Mencari tombol Okay...")
        if self.click_template("okay_button", screen):
            self.random_wait(1, 2)
            self.state = "RETURN_HOME"
        else:
            print("[OKAY] Tombol Okay belum muncul, tunggu...")
            self.random_wait(2, 3)

    def state_return_home(self, screen):
        """
        Step 7: Klik Return Home.
        """
        print("[RETURN_HOME] Mencari tombol Return Home...")
        if self.click_template("return_home", screen):
            self.attacks_done += 1
            status = "⭐ dapat bintang" if self.got_star else "❌ surrender"
            print(f"[RETURN_HOME] Serangan ke-{self.attacks_done} selesai ({status})")
            self.random_wait(2, 3)
            self.state = "WAIT_TROOPS"
        else:
            print("[RETURN_HOME] Tombol belum muncul, tunggu...")
            self.random_wait(2, 3)

    def state_wait_troops(self, screen):
        """
        Step 8: Tunggu pasukan di-train sebelum mulai lagi.
        """
        print(f"[WAIT_TROOPS] Tunggu {TROOP_TRAIN_WAIT}s pasukan di-train...")
        time.sleep(TROOP_TRAIN_WAIT)
        self.state = "HOME"
        print("[WAIT_TROOPS] ✅ Siap farming lagi!\n")

    # ─────────────────────────────────────
    # MAIN LOOP
    # ─────────────────────────────────────
    def run(self):
        print("🚀 Bot dimulai! Tekan Ctrl+C untuk berhenti.")
        print("⚠️  Gerakkan mouse ke pojok KIRI ATAS untuk emergency stop!\n")
        time.sleep(3)

        STATE_HANDLERS = {
            "HOME":         self.state_home,
            "FIND_MATCH":   self.state_find_match,
            "ATTACK_2":     self.state_attack_2,
            "CHECK_LOOT":   self.state_check_loot,
            "DEPLOY":       self.state_deploy,
            "BATTLE":       self.state_battle,
            "OKAY":         self.state_okay,
            "RETURN_HOME":  self.state_return_home,
            "WAIT_TROOPS":  self.state_wait_troops,
        }

        while True:
            try:
                screen = capture_screen()
                print(f"\n{'─'*40}")
                print(f"State saat ini: {self.state}")

                handler = STATE_HANDLERS.get(self.state)
                if handler:
                    handler(screen)
                else:
                    print(f"[ERROR] State tidak dikenal: {self.state}")
                    self.state = "HOME"

                time.sleep(0.5)

            except pyautogui.FailSafeException:
                print("\n🛑 Emergency stop! Mouse di pojok kiri atas.")
                break
            except KeyboardInterrupt:
                print(f"\n🛑 Bot dihentikan.")
                print(f"   Total serangan   : {self.attacks_done}")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                self.random_wait(3, 5)