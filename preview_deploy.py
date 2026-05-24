import pyautogui
from PIL import Image, ImageDraw
from screen import capture_screen
from config import get_deploy_points

def preview_deploy():
    screen = capture_screen()          # screenshot layar
    img    = Image.fromarray(screen)
    draw   = ImageDraw.Draw(img)

    pts = get_deploy_points()
    colors = {
        "top":    "red",
        "bottom": "blue", 
        "left":   "green",
        "right":  "yellow"
    }

    for side, color in colors.items():
        for (x, y) in pts[side]:
            draw.ellipse([x-5, y-5, x+5, y+5], fill=color)

    img.save("deploy_preview.png")
    print("Saved: deploy_preview.png")

preview_deploy()