"""Glacier — cool, crisp, Nordic. Small corner radii and thin outlined
buttons instead of filled ones, for a quieter, more reserved feel."""

from .base import build_theme

NAME = "Glacier"

LIGHT = {
    "bg":      (235, 238, 242),
    "surface": (250, 251, 253),
    "raised":  (214, 222, 230),
    "track":   (184, 196, 208),
    "text":    (35, 42, 50),
    "muted":   (110, 122, 134),
    "accent":  (58, 102, 148),
    "danger":  (176, 64, 64),
    "on":      (84, 140, 132),
    "off":     (180, 150, 150),
}

DARK = {
    "bg":      (18, 22, 28),
    "surface": (28, 34, 43),
    "raised":  (42, 50, 62),
    "track":   (62, 73, 88),
    "text":    (222, 228, 236),
    "muted":   (132, 142, 156),
    "accent":  (112, 170, 216),
    "danger":  (198, 92, 92),
    "on":      (90, 168, 158),
    "off":     (150, 110, 110),
}

SHAPE = dict(radius=4, border_weight=1, key_border_weight=1, title_size=24,
             switch_radius=6, scrim_tint=(14, 20, 28), scrim_opacity=0.72,
             font_name="verdana,arial,sans-serif")

LIGHT_THEME = build_theme(LIGHT, **SHAPE)
DARK_THEME = build_theme(DARK, **SHAPE)