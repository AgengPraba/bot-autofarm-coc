# Di bot.py, update method deploy_troops():

TROOP_ICON_POS = (106, 794)  # koordinat icon Valkyrie

def deploy_troops(self):
    """
    1. Klik icon Valkyrie 1x untuk select
    2. Klik semua titik deploy di belah ketupat
    """
    print("  ⚔️  Deploy Valkyrie...")

    # ── Step 1: Klik icon Valkyrie 1x ──
    valk_x, valk_y = TROOP_ICON_POS
    print(f"  → Select Valkyrie di ({valk_x}, {valk_y})")
    self.click(valk_x, valk_y)
    time.sleep(1)  # tunggu icon ter-select (biasanya ada animasi)

    # ── Step 2: Klik semua titik deploy ──
    order = ["top_left", "top_right", "bottom_left", "bottom_right"]

    for side in order:
        points = self.deploy_pts[side]
        print(f"    → Deploy sisi {side} ({len(points)} titik)")
        for (x, y) in points:
            self.click(x, y, jitter=6)
            time.sleep(0.12)

    print("  ✅ Valkyrie ter-deploy")