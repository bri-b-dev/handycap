import os
from PIL import Image, ImageDraw, ImageFont
import zipfile

# Eingabe
ICON_PATH = "icon.png"
APP_NAME = "Score Differential Calculator"
SPLASH_BG_COLOR = (47, 47, 58)  # Grau
OUTPUT_ZIP = "android_app_assets.zip"

# Launcher Icon Größen
launcher_sizes = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

# Splashscreen Auflösungen
splash_res = {
    "drawable-port-mdpi": (320, 480),
    "drawable-port-hdpi": (480, 800),
    "drawable-port-xhdpi": (720, 1280),
    "drawable-port-xxhdpi": (960, 1600),
    "drawable-port-xxxhdpi": (1280, 1920),
    "drawable-land-mdpi": (480, 320),
    "drawable-land-hdpi": (800, 480),
    "drawable-land-xhdpi": (1280, 720),
    "drawable-land-xxhdpi": (1600, 960),
    "drawable-land-xxxhdpi": (1920, 1280),
}

# Temporärer Arbeitsordner
base_path = "res_temp"

def make_dirs():
    for density in launcher_sizes.keys():
        os.makedirs(f"{base_path}/mipmap-{density}", exist_ok=True)
    for folder in splash_res.keys():
        os.makedirs(f"{base_path}/{folder}", exist_ok=True)
    os.makedirs(f"{base_path}/mipmap-anydpi-v26", exist_ok=True)

def generate_icons(icon):
    for density, size in launcher_sizes.items():
        icon_resized = icon.resize((size, size), Image.LANCZOS)
        icon_resized.save(f"{base_path}/mipmap-{density}/ic_launcher.png")
        icon_resized.save(f"{base_path}/mipmap-{density}/ic_launcher_round.png")
        icon_resized.save(f"{base_path}/mipmap-{density}/ic_launcher_foreground.png")

def generate_splashscreens(icon):
    for folder, (w, h) in splash_res.items():
        splash = Image.new("RGB", (w, h), SPLASH_BG_COLOR)
        icon_resized = icon.resize((int(h * 0.3), int(h * 0.3)), Image.LANCZOS)
        icon_x = (w - icon_resized.width) // 2
        icon_y = (h - icon_resized.height) // 2 - 40
        splash.paste(icon_resized, (icon_x, icon_y), icon_resized.convert("RGBA"))

        draw = ImageDraw.Draw(splash)
        try:
            font = ImageFont.truetype("arial.ttf", size=24)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), APP_NAME, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        draw.text(((w - text_w) / 2, icon_y + icon_resized.height + 20), APP_NAME, fill="white", font=font)
        splash.save(f"{base_path}/{folder}/splash.png")

def write_xmls():
    launcher_xml = '''<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>'''
    with open(f"{base_path}/mipmap-anydpi-v26/ic_launcher.xml", "w") as f:
        f.write(launcher_xml)
    with open(f"{base_path}/mipmap-anydpi-v26/ic_launcher_round.xml", "w") as f:
        f.write(launcher_xml)

def zip_folder():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), base_path))

if __name__ == "__main__":
    icon = Image.open(ICON_PATH).convert("RGBA")
    make_dirs()
    generate_icons(icon)
    generate_splashscreens(icon)
    write_xmls()
    zip_folder()
    print(f"✅ Fertiges ZIP erstellt: {OUTPUT_ZIP}")
