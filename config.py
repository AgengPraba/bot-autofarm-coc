# config.py

# ─────────────────────────────────────
# WINDOW BLUESTACKS
# ─────────────────────────────────────
GAME_LEFT   = 5
GAME_TOP    = 80
GAME_RIGHT  = 1469
GAME_BOTTOM = 903
GAME_WIDTH  = GAME_RIGHT - GAME_LEFT    # 1464
GAME_HEIGHT = GAME_BOTTOM - GAME_TOP    # 823


# ─────────────────────────────────────
# KOORDINAT LOOT (saat battle screen)
# width & height = seberapa lebar area yang di-crop untuk OCR
# ─────────────────────────────────────
LOOT_REGIONS = {
    "gold": {
        "x": 71,   "y": 197,
        "w": 130,  "h": 25,   # crop ke kanan dari titik gold
    },
    "elixir": {
        "x": 71,   "y": 243,
        "w": 130,  "h": 25,
    },
    "dark_elixir": {
        "x": 71,   "y": 282,
        "w": 130,  "h": 25,
    },
}


# ─────────────────────────────────────
# THRESHOLD LOOT — bot akan attack jika
# salah satu resource melebihi nilai ini
# ─────────────────────────────────────
LOOT_THRESHOLD = {
    "gold":       200_000,
    "elixir":     200_000,
    "dark_elixir": 1_000,
}


# ─────────────────────────────────────
# TITIK DEPLOY PASUKAN (Fixed Edge)
# Dihitung otomatis dari ukuran window
# ─────────────────────────────────────
# Koordinat 4 ujung diamond base (dari screenshot)
DIAMOND_CENTER_X = 696   # tengah layar horizontal
DIAMOND_CENTER_Y = 390   # sedikit di bawah tengah

DIAMOND_RADIUS_X = 620   # jarak dari center ke kiri/kanan
DIAMOND_RADIUS_Y = 310   # jarak dari center ke atas/bawah

DEPLOY_MARGIN = 35       # jarak di luar garis diamond

def get_deploy_points():
    """
    Titik deploy mengikuti 4 sisi diamond isometric CoC.
    Setiap sisi adalah garis diagonal lurus, bukan kotak.
    """
    points = {"top": [], "right": [], "bottom": [], "left": []}
    step = 60  # jarak antar titik (px)

    cx = DIAMOND_CENTER_X
    cy = DIAMOND_CENTER_Y
    rx = DIAMOND_RADIUS_X + DEPLOY_MARGIN
    ry = DIAMOND_RADIUS_Y + DEPLOY_MARGIN

    # Sisi kiri-atas: dari (cx-rx, cy) ke (cx, cy-ry)
    steps = int(rx / step)
    for i in range(1, steps):
        t = i / steps
        x = int(cx - rx + t * rx)
        y = int(cy - t * ry)
        points["top"].append((x, y))

    # Sisi kanan-atas: dari (cx, cy-ry) ke (cx+rx, cy)
    for i in range(1, steps):
        t = i / steps
        x = int(cx + t * rx)
        y = int(cy - ry + t * ry)
        points["right"].append((x, y))

    # Sisi kanan-bawah: dari (cx+rx, cy) ke (cx, cy+ry)
    # for i in range(1, steps):
    #     t = i / steps
    #     x = int(cx + rx - t * rx)
    #     y = int(cy + t * ry)
    #     points["bottom"].append((x, y))

    # # Sisi kiri-bawah: dari (cx, cy+ry) ke (cx-rx, cy)
    # for i in range(1, steps):
    #     t = i / steps
    #     x = int(cx - t * rx)
    #     y = int(cy + ry - t * ry)
    #     points["left"].append((x, y))

    return points
# ─────────────────────────────────────
# PATH TEMPLATE IMAGES
# ─────────────────────────────────────
# Di bagian TEMPLATES, update menjadi:
TEMPLATES = {
    "attack_button":  "templates/attack_button.png",
    "find_match":     "templates/find_match.png",
    "attack_2_button":"templates/attack_2_button.png",
    "next_button":    "templates/next_button.png",
    "surrender_button":"templates/surrender_button.png",
    "end_button":     "templates/end_button.png",
    "okay_button":    "templates/okay_button.png",
    "return_home":    "templates/return_home.png",
}


# ─────────────────────────────────────
# TIMING (detik)
# ─────────────────────────────────────
BATTLE_DURATION     = 180   # tunggu 3 menit setelah deploy
TROOP_TRAIN_WAIT    = 0   # tunggu 2 menit pasukan di-train
CLICK_DELAY_MIN     = 0.2   # jeda minimum antar klik
CLICK_DELAY_MAX     = 0.6   # jeda maximum antar klik