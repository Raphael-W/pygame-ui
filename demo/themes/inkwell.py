"""Inkwell & Ember — warm, softly rounded, filled controls. The original
palette from the light-dark demo, moved here as the baseline pack."""

from .base import build_theme

NAME = "Inkwell"

LIGHT = {
    "bg":      (238, 235, 229),
    "surface": (255, 253, 248),
    "raised":  (214, 209, 199),
    "track":   (191, 185, 173),
    "text":    (45, 42, 38),
    "muted":   (130, 124, 114),
    "accent":  (196, 92, 54),
    "danger":  (168, 58, 48),
    "on":      (118, 152, 122),
    "off":     (188, 146, 138),
}

DARK = {
    "bg":      (24, 22, 28),
    "surface": (38, 36, 44),
    "raised":  (56, 53, 63),
    "track":   (74, 70, 82),
    "text":    (235, 230, 224),
    "muted":   (140, 134, 148),
    "accent":  (226, 110, 72),
    "danger":  (140, 45, 45),
    "on":      (74, 96, 78),
    "off":     (96, 66, 66),
}

SHAPE = dict(radius=8, border_weight=0)

LIGHT_THEME = build_theme(LIGHT, **SHAPE)
DARK_THEME = build_theme(DARK, **SHAPE)