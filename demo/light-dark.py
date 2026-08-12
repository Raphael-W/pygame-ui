"""Light/dark theme demo — every element, switchable at runtime.

Toggle light/dark with the switch in the top-right corner, or press T while
nothing is focused. Press P to cycle between theme packs (see themes/).
Widget state (slider value, input text, dropdown choice, switches) survives
both kinds of theme change.
"""

import os
import pygame

from pygame_ui import *
from pygame_ui import Element
from pygame_ui.utils import asset_path

from themes import THEMES, PACK_NAMES, TAG_TITLE, TAG_SUBTITLE, TAG_HEADING, \
    TAG_ACCENT_ICON, TAG_ACCENT_BUTTON

FILES_DIR = os.path.join(os.path.dirname(__file__), "files")
os.makedirs(FILES_DIR, exist_ok=True)

# --- Widget state that survives theme switches ----------------------------

state = {
    "dark": True,
    "pack_index": 0,
    "volume": 40,
    "name": "",
    "notifications": True,
    "quality": "High",
    "splash": None,     # (LabelModal, close_at_ticks)
}


def current_pack():
    return THEMES[PACK_NAMES[state["pack_index"]]]


def current_theme():
    return current_pack()["dark" if state["dark"] else "light"]


def current_bg():
    return current_pack()["dark_palette" if state["dark"] else "light_palette"]["bg"]

QUALITY_OPTIONS = ["High", "Medium", "Low"]


# --- UI construction ------------------------------------------------------

def build():
    theme = current_theme()
    pack_name = PACK_NAMES[state["pack_index"]]

    ui = UI(screen, theme)
    layer = Layer(ui)

    # Top bar
    Label(layer, pack_name, (40, 30), "nw", tag=TAG_TITLE)
    Label(layer, "T to flip light/dark · P or the dropdown to change theme pack", (40, 66), "nw", tag=TAG_SUBTITLE)

    with Row(layer, spacing=12, stick="ne", offset = (40, 35)) as top_right:
        pack_dropdown = Dropdown(top_right, PACK_NAMES, stick="ns", dimensions=(160, 34), action=set_pack, hover_hint="Choose a theme pack")
        pack_dropdown.select_option(state["pack_index"])
        KeyIcon(top_right, pygame.K_p, stick="ns", hover_hint="Next theme pack")
        KeyIcon(top_right, pygame.K_t, stick="ns")
        Label(top_right, "Dark mode", stick="ns", styling={"font_size": 15})
        Switch(top_right, stick="ns", value=state["dark"], action=set_dark, hover_hint = "This is a long hint, but how long can I make it exactly? I don't think there is a character limit and I don't think there is a size limit either.")

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
    ui.set_theme(current_theme())

def next_pack():
    state["pack_index"] = (state["pack_index"] + 1) % len(PACK_NAMES)
    rebuild()

def set_pack(name):
    # Dropdown.select_option() always fires the action (there's no silent
    # "set initial value" path), and we call it below just to sync the
    # dropdown's displayed label to state on every rebuild — so this must
    # be a no-op when the pack hasn't actually changed, or it would recurse
    # into rebuild() forever.
    index = PACK_NAMES.index(name)
    if index == state["pack_index"]:
        return
    state["pack_index"] = index
    rebuild()

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
    screen.fill(current_bg())

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWRESIZED:
            ui.on_resize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:# and ui.focused is None:
            state["dark"] = not state["dark"]
            reload_theme()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            next_pack()

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
