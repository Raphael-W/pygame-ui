import pygame
from ...utils import mult_color
from ...element import Element

class Image(Element):
    style_defaults = {"color": (0, 0, 0), "rotation": 0, "scale": 1}

    def __init__(self, parent, source, offset = (0, 0), stick = "", *, transparent=True, **kwargs):
        super().__init__(parent, offset, (0, 0), stick, transparent=transparent, **kwargs)

        self.source = source
        self.native_size = None
        self.image = None
        self.transformed_image = None

        self.load_source(source)

    def set_disabled(self, disabled):
        super().set_disabled(disabled)
        self.transform()

    def on_style_changed(self):
        self.transform()

    def transform(self):
        color = self.style["color"]
        if self.disabled:
            color = mult_color(color, 0.6)

        target_size = (max(1, round(self.native_size[0] * self.style["scale"])),
                       max(1, round(self.native_size[1] * self.style["scale"])))
        self.transformed_image = pygame.transform.scale(self.image, target_size)
        self.transformed_image = pygame.transform.rotate(self.transformed_image, (self.style["rotation"] % 360))
        self.transformed_image.fill(color, special_flags = pygame.BLEND_RGB_MAX)

        self.set_dimensions(*self.transformed_image.get_size())

    def load_source(self, source):
        self.source = source
        if str(source).lower().endswith(".svg"):
            self.native_size = pygame.image.load(source).get_size()
            render_size = tuple(max(1, round(d * 4)) for d in self.native_size)
            self.image = pygame.image.load_sized_svg(source, render_size).convert_alpha()
        else:
            self.image = pygame.image.load(source).convert_alpha()
            self.native_size = self.image.get_size()
        self.transform()

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.transformed_image, (x, y))
        self.draw_children(surface)

