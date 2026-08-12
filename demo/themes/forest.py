"""Forest — earthy greens and browns, medium-round controls with a heavier
panel radius. Sits between Inkwell's warmth and Glacier's restraint."""

from .base import build_theme

NAME = "Forest"

LIGHT = {
    "bg":      (240, 236, 222),
    "surface": (250, 248, 238),
    "raised":  (214, 206, 178),
    "track":   (180, 170, 138),
    "text":    (46, 42, 30),
    "muted":   (120, 112, 90),
    "accent":  (90, 124, 66),
    "danger":  (168, 70, 48),
    "on":      (94, 140, 80),
    "off":     (196, 150, 110),
}

DARK = {
    "bg":      (24, 28, 20),
    "surface": (34, 40, 28),
    "raised":  (52, 60, 42),
    "track":   (72, 82, 58),
    "text":    (224, 222, 206),
    "muted":   (140, 142, 120),
    "accent":  (140, 184, 100),
    "danger":  (200, 100, 76),
    "on":      (124, 172, 100),
    "off":     (184, 136, 84),
}

SHAPE = dict(radius=14, border_weight=0, title_size=26)

LIGHT_THEME = build_theme(LIGHT, **SHAPE)
DARK_THEME = build_theme(DARK, **SHAPE)