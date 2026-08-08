import pygame
from ...utils import mult_color
from ...element import Element

class Image(Element):
    def __init__(self, parent, source, offset = (0, 0), stick = "", *, scale = 1, rotation = 0, color = (0, 0, 0), transparent = False, show = True, disabled = False, layerIndex = -1):
        super().__init__(parent, offset, (0, 0), stick, show, disabled, layerIndex, transparent = transparent)

        self.source = source
        self.scale = scale
        self.rotation = rotation
        self.color = color

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

    def transform(self, scale = None, rotation = None, color = None):
        if scale is None:
            scale = self.scale
        if rotation is None:
            rotation = self.rotation
        if color is None:
             color = self.color

        self.scale = scale
        self.rotation = rotation
        self.color = color

        self.transformed_image = pygame.transform.scale_by(self.image, scale)
        self.transformed_image = pygame.transform.rotate(self.transformed_image, (rotation % 360))
        self.transformed_image.fill(color, special_flags = pygame.BLEND_RGB_MAX)

        self.set_dimensions(*self.transformed_image.get_size())

    def load_source(self, source):
        self.source = source
        self.image = pygame.image.load(source).convert_alpha()
        self.transform()

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.transformed_image, (x, y))
        self.draw_children(surface)

