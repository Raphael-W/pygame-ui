"""Sunset Pop — vibrant coral and violet, pill-shaped controls, oversized
switches and key icons. The playful, maximal end of the range."""

from .base import build_theme

NAME = "Sunset Pop"

LIGHT = {
    "bg":      (255, 244, 235),
    "surface": (255, 255, 255),
    "raised":  (255, 214, 197),
    "track":   (255, 186, 158),
    "text":    (74, 36, 54),
    "muted":   (168, 120, 132),
    "accent":  (232, 84, 110),
    "danger":  (200, 60, 80),
    "on":      (96, 176, 150),
    "off":     (255, 158, 140),
}

DARK = {
    "bg":      (36, 20, 38),
    "surface": (50, 28, 54),
    "raised":  (78, 40, 72),
    "track":   (108, 54, 92),
    "text":    (255, 232, 238),
    "muted":   (196, 150, 176),
    "accent":  (255, 110, 140),
    "danger":  (224, 96, 116),
    "on":      (96, 200, 168),
    "off":     (198, 100, 124),
}

SHAPE = dict(radius=22, border_weight=0, switch_scale=1.15, key_size=1.1, title_size=28,
             scrim_tint=(52, 18, 32), scrim_opacity=0.75)

LIGHT_THEME = build_theme(LIGHT, **SHAPE)
DARK_THEME = build_theme(DARK, **SHAPE)