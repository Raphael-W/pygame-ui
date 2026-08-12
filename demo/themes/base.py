"""Shared machinery for the theme packs in this directory.

A theme *pack* is a light/dark pair that share a "shape language" (corner
radii, border weights, control scale) but swap out a colour palette. Each
pack module (inkwell.py, glacier.py, ...) supplies a LIGHT and DARK palette
dict plus a SHAPE dict of overrides, and calls `build_theme(palette, **shape)`
to produce the actual Theme objects.

Palette keys (all required):
    bg       window background
    surface  dialogs / inputs / panels
    raised   buttons, chips
    track    slider tracks, scrollbar tracks, quiet borders
    text     primary text
    muted    secondary text
    accent   the theme's signature colour
    danger   destructive actions
    on       switch "on" colour
    off      switch "off" colour

Shape keys (all optional, see defaults below):
    radius          base corner radius for buttons/inputs/dropdowns
    panel_radius    accordions, message boxes, file dialogs
    key_radius      KeyIcon corners
    scrollbar_radius
    hint_radius     hover-hint tooltip corners
    border_weight   outline weight on buttons/keys (0 = filled, no outline)
    switch_scale    Switch control scale
    key_size        KeyIcon scale
    cursor          pygame cursor constant used on clickable controls
"""

import pygame

from pygame_ui import *

# Tag constants: string-keyed theme selectors for visual *roles* rather than
# element types. Shared across every pack so demo code can tag elements once
# and have it map correctly whichever pack is active.
TAG_TITLE = "title"
TAG_SUBTITLE = "subtitle"
TAG_HEADING = "heading"
TAG_ACCENT_ICON = "accent-icon"
TAG_ACCENT_BUTTON = "accent-button"


def build_theme(p, *, radius=10, panel_radius=None, key_radius=None,
                 scrollbar_radius=5, hint_radius=None, border_weight=0,
                 key_border_weight=2, switch_scale=1, key_size=1,
                 cursor=pygame.SYSTEM_CURSOR_HAND, title_size=26):
    if panel_radius is None:
        panel_radius = radius + 5
    if key_radius is None:
        key_radius = max(radius - 2, 0)
    if hint_radius is None:
        hint_radius = max(radius - 4, 0)

    return Theme({
        Label:       {"color": p["text"]},
        TAG_TITLE:      {"font_size": title_size, "bold": True, "color": p["accent"]},
        TAG_SUBTITLE:   {"font_size": 14, "color": p["muted"]},
        TAG_HEADING:    {"font_size": 13, "bold": True, "color": p["muted"]},
        TAG_ACCENT_ICON: {"color": p["accent"]},
        TAG_ACCENT_BUTTON: {"color": p["accent"], "image_color": p["bg"]},
        Accordion:   {"color": p["surface"] + (230,), "border_radius": panel_radius,
                      "button_color": p["raised"], "icon_color": p["text"]},
        Button:      {"color": p["raised"], "border_radius": radius,
                      "border_weight": border_weight, "border_color": p["track"],
                      "cursor": cursor},
        TextButton:  {"font_color": p["text"]},
        ImageButton: {"image_color": p["text"]},
        Slider:      {"bar_color": p["track"], "handle_color": p["accent"],
                      "font_size": 15, "font_color": p["muted"]},
        Switch:      {"on_color": p["on"], "off_color": p["off"],
                      "handle_color": p["bg"], "scale": switch_scale},
        TextInput:   {"color": p["surface"], "font_color": p["text"],
                      "placeholder_font_color": p["muted"], "border_radius": radius,
                      "button_color": p["raised"], "button_border_radius": radius,
                      "button_icon_color": p["muted"]},
        Dropdown:    {"color": p["raised"], "font_color": p["text"],
                      "icon_color": p["accent"], "border_radius": radius,
                      "cursor": cursor},
        KeyIcon:     {"color": p["raised"], "border_color": p["accent"],
                      "font_color": p["text"], "border_radius": key_radius,
                      "border_weight": key_border_weight, "size": key_size},
        ScrollBar:   {"track_color": p["track"], "handle_color": p["raised"],
                      "border_radius": scrollbar_radius},
        Message:     {"bg_color": p["surface"], "font_color": p["text"],
                      "border_radius": panel_radius,
                      "button1_color": p["raised"], "button1_font_color": p["text"],
                      "button2_color": p["danger"], "button2_font_color": p["text"]},
        HoverHint:   {"bg_color": p["raised"], "border_color": p["accent"],
                      "font_color": p["text"], "border_radius": hint_radius,
                      "padding": (12, 8), "margins": (0, 6)},
        FileSaver:   {"bg_color": p["surface"], "font_color": p["text"],
                      "border_radius": panel_radius,
                      "button_color": p["raised"], "text_input_bg": p["bg"],
                      "text_input_font_color": p["text"]},
        LabelModal:  {"color": p["text"]},
        FilePicker:  {"bg_color": p["surface"], "font_color": p["text"],
                      "border_radius": panel_radius,
                      "icon_color": p["text"], "action_button_color": p["raised"],
                      "delete_button_color": p["danger"], "search_bg": p["bg"],
                      "search_font_color": p["text"], "file_selected_bg_color": p["raised"],
                      "file_hover_bg_color": p["bg"]},
    })