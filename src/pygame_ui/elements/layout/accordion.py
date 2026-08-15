import pygame
from ...element import Element
from ..display import Label
from ..layout import AutoSizeElement
from ..controls import ImageButton
from ...utils import asset_path

class Accordion(AutoSizeElement):
    style_defaults = {"color": (50, 50, 50, 200), "border_radius": 15, "button_color": (100, 100, 100), "icon_color": (200, 200, 200), "padding": (15, 15)}

    def __init__(self, parent, title, offset = (30, 30), dimensions = (300, 400), stick = "se", **kwargs):
        super().__init__(parent, offset, dimensions, stick, **kwargs)
        self.expanded_dimensions = dimensions
        self.expanded = True

        Label(self, title, (0, 10), "new", styling = {"font_size": 18, "min_font_size": 12, "max_width": self.width - 120, "wrap_mode": "ellipse"})

        self.toggle_button = ImageButton(self, asset_path("icons", "minus.png"), dimensions=(30, 30), stick="ne", styling={"image_scale": 0.8, "border_radius": 100}, action = self.toggle)
        self.register_style_mapping(self.toggle_button, {"color": "button_color", "image_color": "icon_color"})

    def set_expanded(self, expanded):
        self.expanded = expanded

        if expanded:
            self.toggle_button.set_source(asset_path("icons", "minus.png"))
            self.set_dimensions(*self.expanded_dimensions)
        else:
            self.toggle_button.set_source(asset_path("icons", "plus.png"))
            self.set_dimensions(60, 60)

        for element in self.get_children(only_visible = False, only_enabled = False):
            if element is not self.toggle_button:
                element.show = self.expanded

    def toggle(self):
        self.set_expanded(not self.expanded)

    def handle_mouse_event(self, event) -> bool:
        return False

    def draw(self, surface):
        x, y = self.get_pos()
        width, height = self.get_size()
        transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, self.style["color"], (0, 0, width, height), border_radius = self.style["border_radius"])
        surface.blit(transparent_surface, (x, y))
        self.draw_children(surface)