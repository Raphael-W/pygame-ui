import pygame
from ...element import Element

class Scrim(Element):
    style_defaults = {"tint": (50, 50, 50), "opacity": 0.8}
    def __init__(self, parent, **kwargs):
        super().__init__(parent, (0, 0), (0, 0), "nesw", **kwargs)
        self.set_dimensions(*self.parent.get_size())

        self.surface = None
        self.create_surface()

    def on_style_changed(self):
        super().on_style_changed()
        self.create_surface()

    def get_pos(self):
        #Override method - scrim always draws from 0, 0
        return 0, 0

    def create_surface(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        combined_color = self.style["tint"] + (self.style["opacity"] * 255,)
        pygame.draw.rect(self.surface, combined_color, (0, 0, self.width, self.height))

    def on_screen_resize(self):
        self.set_dimensions(*self.parent.get_size())
        self.create_surface()

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))
        self.draw_children(surface)