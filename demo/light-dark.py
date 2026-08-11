"""Light/dark theme demo — every element, switchable at runtime.

Toggle with the switch in the top-right corner, or press T while nothing is
focused. Widget state (slider value, input text, dropdown choice, switches)
survives the theme change.
"""

import os
import pygame

from pygame_ui import *
from pygame_ui.utils import asset_path

FILES_DIR = os.path.join(os.path.dirname(__file__), "files")
os.makedirs(FILES_DIR, exist_ok=True)

# --- Palettes -------------------------------------------------------------

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


# Tag constants: string-keyed theme selectors for visual *roles* rather than
# element types (the CSS-class equivalent of the type-selector rules below).
# Declaring them as constants turns a typo'd tag into a NameError instead of
# a rule that silently never matches.
TAG_TITLE = "title"
TAG_SUBTITLE = "subtitle"
TAG_HEADING = "heading"
TAG_ACCENT_ICON = "accent-icon"
TAG_ACCENT_BUTTON = "accent-button"


def make_theme(p):
    """Both themes are the same rules over a different palette."""
    return Theme({
        Label:       {"color": p["text"]},
        TAG_TITLE:      {"font_size": 26, "bold": True, "color": p["accent"]},
        TAG_SUBTITLE:   {"font_size": 14, "color": p["muted"]},
        TAG_HEADING:    {"font_size": 13, "bold": True, "color": p["muted"]},
        TAG_ACCENT_ICON: {"color": p["accent"]},
        TAG_ACCENT_BUTTON: {"color": p["accent"], "image_color": p["bg"]},
        Accordion:   {"color": p["surface"] + (230,), "border_radius": 15,
                      "button_color": p["raised"], "icon_color": p["text"]},
        Button:      {"color": p["raised"], "border_radius": 8},
        TextButton:  {"font_color": p["text"]},
        ImageButton: {"image_color": p["text"]},
        Slider:      {"bar_color": p["track"], "handle_color": p["accent"],
                      "font_size": 15, "font_color": p["muted"]},
        Switch:      {"on_color": p["on"], "off_color": p["off"],
                      "handle_color": p["bg"]},
        TextInput:   {"color": p["surface"], "font_color": p["text"],
                      "placeholder_font_color": p["muted"], "border_radius": 10,
                      "button_color": p["raised"], "button_icon_color": p["muted"]},
        Dropdown:    {"color": p["raised"], "font_color": p["text"],
                      "icon_color": p["accent"], "border_radius": 8},
        KeyIcon:     {"color": p["raised"], "border_color": p["accent"],
                      "font_color": p["text"], "border_radius": 6},
        ScrollBar:   {"track_color": p["track"], "handle_color": p["raised"],
                      "border_radius": 5},
        Message:     {"bg_color": p["surface"], "font_color": p["text"],
                      "button1_color": p["raised"], "button2_color": p["danger"]},
        HoverHint:   {"bg_color": p["raised"], "border_color": p["accent"],
                      "font_color": p["text"], "border_radius": 5,
                      "padding": (12, 8), "margins": (0, 6)},
        FileSaver:   {"bg_color": p["surface"], "font_color": p["text"],
                      "button_color": p["raised"]},
        FilePicker:  {"bg_color": p["surface"], "font_color": p["text"],
                      "icon_color": p["text"]},
    })


THEMES = {"light": make_theme(LIGHT), "dark": make_theme(DARK)}

# --- Widget state that survives theme switches ----------------------------

state = {
    "dark": True,
    "volume": 40,
    "name": "",
    "notifications": True,
    "quality": "High",
    "splash": None,     # (LabelModal, close_at_ticks)
}

QUALITY_OPTIONS = ["High", "Medium", "Low"]


# --- UI construction ------------------------------------------------------

def build():
    theme = THEMES["dark" if state["dark"] else "light"]

    ui = UI(screen, theme)
    layer = Layer(ui)

    # Top bar
    Label(layer, "Every element, two themes", (40, 30), "nw", tag=TAG_TITLE)
    Label(layer, "flip the switch, or press T", (40, 66), "nw", tag=TAG_SUBTITLE)

    top_right = Row(layer, spacing=12, stick="ne", offset = (40, 35))
    KeyIcon(top_right, pygame.K_t, stick="ns")
    Label(top_right, "Dark mode", stick="ns", styling={"font_size": 15})
    Switch(top_right, stick="ns", value=state["dark"], action=set_dark, hover_hint = "This is a long hint")

    # --- Display column ---
    Label(layer, "DISPLAY", (40, 120), "nw", tag=TAG_HEADING)
    Label(layer, "Labels wrap onto multiple lines when you give them a "
                 "max width, like this one.", (40, 150), "nw",
          styling={"font_size": 15, "max_width": 280})
    Image(layer, asset_path("icons", "down.png"), (40, 220), "nw",
          tag=TAG_ACCENT_ICON, styling={"scale": 1.2})
    keys = Row(layer, (40, 280), "nw", spacing=6)
    key_hints = {pygame.K_w: "Move up", pygame.K_a: "Move left",
                 pygame.K_s: "Move down", pygame.K_d: "Move right"}
    for key, hint in key_hints.items():
        KeyIcon(keys, key, hover_hint=hint)

    # --- Controls column ---
    Label(layer, "CONTROLS", (400, 120), "nw", tag=TAG_HEADING)

    buttons = Row(layer, (400, 150), "nw", spacing=10)
    TextButton(buttons, "Button", dimensions=(110, 40),
               action=lambda: print("clicked"))
    TextButton(buttons, "Disabled", dimensions=(110, 40), disabled=True)
    ImageButton(buttons, asset_path("icons", "plus.png"), dimensions=(40, 40),
                tag=TAG_ACCENT_BUTTON, styling={"image_scale": 0.8},
                hover_hint="Add a new item")

    Slider(layer, (0, 100), (400, 225), (180, 10), "nw", value=state["volume"],
           suffix="%", action=lambda v: state.update(volume=v))

    notif_row = Row(layer, (400, 265), "nw", spacing=12)
    Switch(notif_row, stick="ns", value=state["notifications"],
           action=lambda v: state.update(notifications=v))
    Label(notif_row, "Notifications", stick="ns", styling={"font_size": 15})

    name_input = TextInput(layer, (400, 315), "nw", placeholder="Your name",
                           text=state["name"],
                           styling={"length": 250, "font_size": 17})
    name_input.type_action = lambda: state.update(name=name_input.get_value())

    dropdown = Dropdown(layer, QUALITY_OPTIONS, (400, 375), "nw",
                        dimensions=(250, 34),
                        action=lambda option: state.update(quality=option))
    if state["quality"] != QUALITY_OPTIONS[0]:
        dropdown.select_option(QUALITY_OPTIONS.index(state["quality"]))

    ScrollBar(layer, 140, 420, (700, 150), "nw", hover_hint="Drag to scroll")

    # --- Modals column ---
    Label(layer, "MODALS", (790, 120), "nw", tag=TAG_HEADING)
    modal_col = Column(layer, (790, 150), "nw", spacing=10)
    TextButton(modal_col, "Message box", dimensions=(180, 40), action=lambda:
               Message(layer, "Delete everything?", "Just kidding — this is only a demo.",
                       ("Cancel", None), ("Delete", None)))
    TextButton(modal_col, "Splash text", dimensions=(180, 40),
               action=lambda: show_splash(layer))
    TextButton(modal_col, "Save a file", dimensions=(180, 40), action=lambda:
               FileSaver(layer, FILES_DIR, "txt", save_note, "Save note"))
    TextButton(modal_col, "Pick a file", dimensions=(180, 40), action=lambda:
               FilePicker(layer, "Pick a note", FILES_DIR, "txt",
                          lambda path: Message(layer, "You picked",
                                               path.name, ("Nice", None))))

    # Accordion pinned bottom-right
    panel = Accordion(layer, "Extras", dimensions=(300, 180), stick="se",
                       hover_hint="Click the corner button to collapse")
    Label(panel, "Accordions collapse into a corner button.", (20, 70), "nw",
          styling={"font_size": 13, "max_width": 260})
    extra_row = Row(panel, (20, 120), "nw", spacing=12)
    Switch(extra_row, stick="ns")
    Label(extra_row, "A switch in a panel", stick="ns", styling={"font_size": 13})

    return ui


def save_note(file_path):
    with open(file_path, "w") as f:
        f.write("Saved from the light-dark demo.\n")


def show_splash(layer):
    modal = LabelModal(layer, "Modals sit above a scrim",
                       styling={"font_size": 30, "bold": True})
    state["splash"] = (modal, pygame.time.get_ticks() + 1500)


def set_dark(value):
    state["dark"] = value
    reload_theme()

def reload_theme():
    state["splash"] = None
    new_theme = make_theme(DARK if state["dark"] else LIGHT)
    ui.set_theme(new_theme)

def rebuild():
    global ui
    state["splash"] = None
    ui = build()

# --- Boilerplate ----------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((1180, 700), pygame.RESIZABLE, vsync=1)
pygame.display.set_caption("Light / Dark")
clock = pygame.time.Clock()

ui = build()

running = True
while running:
    screen.fill((DARK if state["dark"] else LIGHT)["bg"])

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWRESIZED:
            ui.on_resize()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_t
              and ui.focused is None):
            state["dark"] = not state["dark"]
            reload_theme()

    ui.handle_events(events)

    # Auto-close the splash modal after its timer
    if state["splash"] is not None:
        modal, close_at = state["splash"]
        if pygame.time.get_ticks() >= close_at:
            modal.close()
            state["splash"] = None

    ui.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
