"""Palette Studio — a small colour-palette editor built entirely with pygame_ui.

Mix a colour with the RGB sliders, name it, and collect it into a palette.
Generate whole palettes from colour-harmony rules, save them to disk as JSON,
and load them back later.

Controls:
    - Left-click a palette chip to load it back into the mixer
    - Right-click a palette chip to remove it
    - Press R (while nothing is focused) to randomise the mix
"""

import colorsys
import json
import os
import random

import pygame

from pygame_ui import *
from pygame_ui.utils import asset_path

PALETTES_DIR = os.path.join(os.path.dirname(__file__), "palettes")
os.makedirs(PALETTES_DIR, exist_ok=True)

# --- Palette-studio colour scheme ("Inkwell & Ember") ---
BG      = (24, 22, 28)      # window background
PANEL   = (38, 36, 44)      # dialogs / inputs
RAISED  = (56, 53, 63)      # buttons
TRACK   = (74, 70, 82)      # slider tracks, borders
INK     = (235, 230, 224)   # text
MUTED   = (140, 134, 148)   # secondary text
EMBER   = (226, 110, 72)    # accent
DANGER  = (140, 45, 45)     # destructive actions

MAX_CHIPS = 12


# --- Custom elements ------------------------------------------------------

class Swatch(Element):
    """A large preview of the colour currently being mixed."""

    style_defaults = {"border_radius": 16, "border_color": TRACK, "border_weight": 2}

    def __init__(self, parent, offset, dimensions, stick="nw", *, styling=None):
        super().__init__(parent, offset, dimensions, stick, styling=styling)
        self.color = (0, 0, 0)

    def draw(self, surface):
        x, y = self.get_pos()
        radius = self.style["border_radius"]
        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height), 0, radius)
        if (weight := self.style["border_weight"]) > 0:
            pygame.draw.rect(surface, self.style["border_color"],
                             (x, y, self.width, self.height), weight, radius)
        self.draw_children(surface)


class PaletteChip(Element):
    """One saved colour in the palette. Left-click loads it, right-click removes it."""

    style_defaults = {"border_radius": 10, "hover_color": INK,
                      "cursor": pygame.SYSTEM_CURSOR_HAND}

    def __init__(self, parent, name, rgb, app):
        super().__init__(parent, (0, 0), (40, 40), "")
        self.name = name
        self.rgb = tuple(rgb)
        self.app = app

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.app.load_chip(self)
            elif event.button == 3:
                self.app.remove_chip(self)
            return True
        return False

    def draw(self, surface):
        x, y = self.get_pos()
        radius = self.style["border_radius"]
        pygame.draw.rect(surface, self.rgb, (x, y, self.width, self.height), 0, radius)
        if self.hovered:
            pygame.draw.rect(surface, self.style["hover_color"],
                             (x, y, self.width, self.height), 2, radius)
        self.draw_children(surface)


# --- Theme ----------------------------------------------------------------

THEME = Theme({
    Label:       {"color": INK},
    Button:      {"color": RAISED, "border_radius": 8},
    TextButton:  {"font_color": INK},
    ImageButton: {"image_color": INK},
    Slider:      {"bar_color": TRACK, "handle_color": EMBER,
                  "font_size": 15, "font_color": MUTED},
    Switch:      {"on_color": (74, 96, 78), "off_color": (96, 66, 66),
                  "handle_color": BG},
    TextInput:   {"color": PANEL, "font_color": INK, "placeholder_font_color": MUTED,
                  "border_radius": 10, "button_color": RAISED, "button_icon_color": MUTED},
    Dropdown:    {"color": RAISED, "text_color": INK, "icon_color": EMBER,
                  "border_radius": 8},
    KeyIcon:     {"color": RAISED, "border_color": EMBER, "font_color": INK,
                  "border_radius": 6},
    Message:     {"bg_color": PANEL, "font_color": INK,
                  "button1_color": RAISED, "button2_color": DANGER},
    FileSaver:   {"bg_color": PANEL, "font_color": INK, "button_color": RAISED},
    FilePicker:  {"bg_color": PANEL, "font_color": INK, "icon_color": INK},
    Swatch:      {"border_color": TRACK},
    PaletteChip: {"hover_color": INK},
})


# --- The application ------------------------------------------------------

class PaletteStudio:
    def __init__(self, layer):
        self.layer = layer

        # Left panel: the mixer
        Label(layer, "Palette Studio", (40, 30), "nw",
              styling={"font_size": 30, "bold": True, "color": EMBER})
        Label(layer, "mix - collect - save", (40, 72), "nw",
              styling={"font_size": 14, "color": MUTED})

        self.preview = Swatch(layer, (40, 110), (300, 150))
        self.hex_label = Label(layer, "#000000", (40, 280), "nw",
                               styling={"font_size": 24, "bold": True})

        slider_column = Column(layer, (40, 330), "nw", spacing=18)
        self.sliders = []
        for channel, handle_color in (("R", (211, 84, 84)),
                                      ("G", (96, 176, 106)),
                                      ("B", (94, 138, 211))):
            row = Row(slider_column, spacing=12)
            Label(row, channel, stick="ns", styling={"bold": True, "color": handle_color})
            slider = Slider(row, (0, 255), bar_dimensions=(200, 12), stick="ns",
                            value=0, increment=1, action=lambda _v: self.refresh(),
                            styling={"handle_color": handle_color})
            self.sliders.append(slider)

        self.name_input = TextInput(layer, (40, 462), "nw", placeholder="colour name",
                                    styling={"length": 300, "font_size": 18},
                                    action=lambda _text: self.add_current())
        buttons = Row(layer, (40, 515), "nw", spacing=10)
        TextButton(buttons, "Add to palette", dimensions=(170, 40), action=self.add_current)
        TextButton(buttons, "Randomise", dimensions=(120, 40), action=self.randomise)

        websafe_row = Row(layer, (40, 572), "nw", spacing=12)
        Label(websafe_row, "Web-safe colours", stick="ns", styling={"font_size": 14})
        Switch(websafe_row, stick="ns", value=False, action=self.set_websafe)

        # Right panel: the palette
        Label(layer, "PALETTE", (430, 30), "nw", styling={"font_size": 20, "bold": True})
        self.stats_label = Label(layer, "", (430, 58), "nw",
                                 styling={"font_size": 13, "color": MUTED})
        self.chip_row = Row(layer, (430, 85), "nw", spacing=8)

        Label(layer, "Harmony generator", (430, 155), "nw",
              styling={"font_size": 14, "color": MUTED})
        Dropdown(layer, ["Complement", "Analogous", "Triad", "Shades"],
                 (430, 180), "nw", dimensions=(220, 32), action=self.generate_harmony)

        file_buttons = Row(layer, (430, 250), "nw", spacing=10)
        TextButton(file_buttons, "Save", dimensions=(100, 40), action=self.save_palette)
        TextButton(file_buttons, "Load", dimensions=(100, 40), action=self.load_palette)
        ImageButton(file_buttons, asset_path("icons", "bin.png"), dimensions=(40, 40),
                    image_scale=0.8, styling={"color": DANGER}, action=self.clear_palette)

        # Help panel, pinned to the bottom-right corner
        help_panel = Accordion(layer, "Help", dimensions=(320, 210), stick="se")
        Label(help_panel, "left-click a chip to load it", (20, 70), "nw",
              styling={"font_size": 13})
        Label(help_panel, "right-click a chip to remove it", (20, 95), "nw",
              styling={"font_size": 13})
        KeyIcon(help_panel, pygame.K_r, (20, 125), "nw")
        Label(help_panel, "randomise the mix", (60, 132), "nw", styling={"font_size": 13})
        Label(help_panel, "palettes are saved as .json files", (20, 170), "nw",
              styling={"font_size": 13, "color": MUTED})

        self.websafe = False
        self.set_rgb(EMBER)
        self.refresh()

    # --- current mix ---

    def rgb(self):
        return tuple(int(slider.get_value()) for slider in self.sliders)

    def set_rgb(self, color):
        for slider, channel in zip(self.sliders, color):
            slider.set_value(int(channel))
        self.refresh()

    def refresh(self):
        color = self.rgb()
        self.preview.color = color
        self.hex_label.set_text("#{:02X}{:02X}{:02X}".format(*color))

    def randomise(self):
        color = [random.randint(0, 255) for _ in range(3)]
        if self.websafe:
            color = [round(c / 51) * 51 for c in color]
        self.set_rgb(color)

    def set_websafe(self, on):
        self.websafe = on
        for slider in self.sliders:
            slider.increment = 51 if on else 1
        if on:
            self.set_rgb([round(c / 51) * 51 for c in self.rgb()])

    # --- palette chips ---

    def chips(self):
        return self.chip_row.get_children(only_visible=False)

    def add_current(self):
        name = self.name_input.get_value().strip() or self.hex_label.text
        self.add_chip(name, self.rgb())

    def add_chip(self, name, rgb):
        if len(self.chips()) >= MAX_CHIPS:
            Message(self.layer, "Palette full",
                    f"A palette holds up to {MAX_CHIPS} colours. "
                    "Right-click a chip to make room.", ("Okay", None))
            return
        PaletteChip(self.chip_row, name, rgb, self)
        self.update_stats()

    def load_chip(self, chip):
        self.set_rgb(chip.rgb)
        self.name_input.text = chip.name
        self.name_input.cursor_index = len(chip.name)

    def remove_chip(self, chip):
        chip.remove()
        self.update_stats()

    def clear_palette(self):
        if not self.chips():
            return
        def do_clear():
            for chip in list(self.chips()):
                chip.remove()
            self.update_stats()
        Message(self.layer, "Clear palette?",
                "This removes every colour from the current palette.",
                ("Cancel", None), ("Clear", do_clear))

    def update_stats(self):
        count = len(self.chips())
        self.stats_label.set_text(f"{count}/{MAX_CHIPS} colours" if count else
                                  "empty - mix a colour and add it")

    # --- harmony generation ---

    def generate_harmony(self, rule):
        r, g, b = (c / 255 for c in self.rgb())
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        s, v = max(s, 0.35), max(v, 0.35)   # keep generated colours visible

        if rule == "Complement":
            hsvs = [(h, s, v), (h, s * 0.55, v), ((h + 0.5) % 1, s, v), ((h + 0.5) % 1, s * 0.55, v)]
        elif rule == "Analogous":
            hsvs = [((h + off) % 1, s, v) for off in (-1/6, -1/12, 0, 1/12, 1/6)]
        elif rule == "Triad":
            hsvs = [((h + off) % 1, s, v) for off in (0, 1/3, 2/3)]
        else:  # Shades
            hsvs = [(h, s, v * fade) for fade in (1.0, 0.8, 0.6, 0.4, 0.25)]

        for chip in list(self.chips()):
            chip.remove()
        for i, hsv in enumerate(hsvs):
            rgb = tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(*hsv))
            self.add_chip(f"{rule.lower()} {i + 1}", rgb)

    # --- saving and loading ---

    def save_palette(self):
        if not self.chips():
            Message(self.layer, "Nothing to save", "Add some colours first!", ("Okay", None))
            return
        def write(file_path):
            data = {"colors": [{"name": c.name, "rgb": list(c.rgb)} for c in self.chips()]}
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        FileSaver(self.layer, PALETTES_DIR, "json", write, "Save palette",
                  placeholder="palette name")

    def load_palette(self):
        def read(path):
            with open(path) as f:
                data = json.load(f)
            for chip in list(self.chips()):
                chip.remove()
            for entry in data["colors"][:MAX_CHIPS]:
                self.add_chip(entry["name"], entry["rgb"])
        FilePicker(self.layer, "Load palette", PALETTES_DIR, "json", read,
                   file_validation=self._is_palette_file)

    @staticmethod
    def _is_palette_file(path):
        try:
            with open(path) as f:
                return "colors" in json.load(f)
        except (OSError, json.JSONDecodeError):
            return False


# --- Boilerplate ----------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((1100, 680), pygame.RESIZABLE, vsync=1)
pygame.display.set_caption("Palette Studio")
clock = pygame.time.Clock()

ui = UI(screen, THEME)
main_layer = Layer(ui)
app = PaletteStudio(main_layer)

running = True
while running:
    screen.fill(BG)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.WINDOWRESIZED:
            ui.on_resize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and ui.focused is None:
            app.randomise()

    ui.handle_events(events)

    pygame.draw.line(screen, TRACK, (395, 30), (395, screen.get_height() - 30), 2)
    ui.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
