import pygame
from ...utils import mult_color
from ...element import Element

class Image(Element):
    style_defaults = {"color": (0, 0, 0), "rotation": 0, "scale": 1}

    def __init__(self, parent, source, offset = (0, 0), stick = "", *, transparent=True, **kwargs):
        super().__init__(parent, offset, (0, 0), stick, transparent=transparent, **kwargs)

        self.source = source
        self.image = None
        self.transformed_image = None

        self.load_source(source)

    def set_disabled(self, disabled):
        super().set_disabled(disabled)
        if disabled:
            original_color = self.color
            self.transform(color = mult_color(original_color, 0.6))
            self.color = original_color
        else:
            self.transform()

    def on_style_changed(self):
        self.transform()

    def transform(self):
        self.transformed_image = pygame.transform.scale_by(self.image, self.style["scale"])
        self.transformed_image = pygame.transform.rotate(self.transformed_image, (self.style["rotation"] % 360))
        self.transformed_image.fill(self.style["color"], special_flags = pygame.BLEND_RGB_MAX)

        self.set_dimensions(*self.transformed_image.get_size())

    def load_source(self, source):
        self.source = source
        self.image = pygame.image.load(source).convert_alpha()
        self.transform()

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.transformed_image, (x, y))
        self.draw_children(surface)

