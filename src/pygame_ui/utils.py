import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "MonoFont.ttf")

def asset_path(asset_type, file_name):
    return os.path.join(ASSETS_DIR, asset_type, file_name)

def get_precision(value):
    str_value = str(value)
    split_value = str_value.split('.')
    if len(split_value) == 2:
        return len(split_value[1])
    return 1

def mult_color(color, mult):
    return tuple(max(0, min(int(c * mult), 255)) for c in color)