import pygame
from ..element import Element
from .label import Label
from .image_button import ImageButton
from ..utils import asset_path

class Accordion(Element):
    style_defaults = {}

    def __init__(self, parent, title, offset = (30, 30), dimensions = (300, 400), stick = "se", *, show = True, disabled = False, styling = None, child_index = -1):
        super().__init__(parent, offset, dimensions, stick, show, disabled, child_index, styling = styling)

        self.expanded_width, self.expanded_height = dimensions
        self.expanded = True

        Label(self, title, (0, 25), "new", styling = {"font_size": 18, "min_font_size": 12, "max_width": self.width - 120, "wrap_mode": "ellipse"})
        self.toggle_button = ImageButton(self, asset_path("icons", "minus.png"), (15, 15), (30, 30), "ne", styling={"image_color": (200, 200, 200), "border_radius": 100}, image_scale = 0.8, action = self.toggle)

    def set_expanded(self, expanded):
        self.expanded = expanded

        if expanded:
            self.toggle_button.set_source(asset_path("icons", "minus.png"))
            self.set_dimensions(self.expanded_width, self.expanded_height)
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
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (50, 50, 50, 200), (0, 0, self.width, self.height), border_radius = 15)
        surface.blit(transparent_surface, (x, y))
        self.draw_children(surface)