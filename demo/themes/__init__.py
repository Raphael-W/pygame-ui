"""Registry of theme packs. Each pack is a light/dark pair sharing a shape
language over a different palette — see base.py for the pack contract.

    from themes import PACK_NAMES, THEMES, TAG_TITLE, ...
    theme = THEMES[PACK_NAMES[0]]["dark"]
"""

from .base import TAG_TITLE, TAG_SUBTITLE, TAG_HEADING, TAG_ACCENT_ICON, TAG_ACCENT_BUTTON
from . import inkwell, glacier, sunset, terminal, forest

_PACKS = [inkwell, glacier, sunset, terminal, forest]

PACK_NAMES = [pack.NAME for pack in _PACKS]

THEMES = {
    pack.NAME: {"light": pack.LIGHT_THEME, "dark": pack.DARK_THEME,
                "light_palette": pack.LIGHT, "dark_palette": pack.DARK}
    for pack in _PACKS
}

__all__ = ["PACK_NAMES", "THEMES", "TAG_TITLE", "TAG_SUBTITLE", "TAG_HEADING",
           "TAG_ACCENT_ICON", "TAG_ACCENT_BUTTON"]