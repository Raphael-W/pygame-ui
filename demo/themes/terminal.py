"""Terminal — Solarized-flavoured, square corners, bright bordered controls.
The light variant is a warm paper tone rather than plain white, matching
Solarized Light's approach of avoiding pure white/black in both modes."""

from .base import build_theme

NAME = "Terminal"

LIGHT = {
    "bg":      (253, 246, 227),
    "surface": (238, 232, 213),
    "raised":  (220, 212, 186),
    "track":   (180, 168, 140),
    "text":    (50, 60, 60),
    "muted":   (120, 132, 132),
    "accent":  (38, 139, 140),
    "danger":  (190, 60, 50),
    "on":      (60, 140, 80),
    "off":     (190, 120, 60),
}

DARK = {
    "bg":      (0, 20, 26),
    "surface": (7, 36, 46),
    "raised":  (20, 54, 66),
    "track":   (50, 84, 94),
    "text":    (190, 214, 214),
    "muted":   (100, 132, 132),
    "accent":  (60, 200, 200),
    "danger":  (220, 80, 70),
    "on":      (80, 190, 110),
    "off":     (210, 140, 60),
}

SHAPE = dict(radius=2, border_weight=2, key_border_weight=2, title_size=24)

LIGHT_THEME = build_theme(LIGHT, **SHAPE)
DARK_THEME = build_theme(DARK, **SHAPE)