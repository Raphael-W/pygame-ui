import io
import pygame
from .image import Image

class InlineSVG(Image):
    def __init__(self, parent, svg, offset = (0, 0), stick="", *, transparent=True, **kwargs):
        super().__init__(parent, svg, offset=offset, stick=stick, transparent=transparent, **kwargs)

    def load_source(self, source):
        self.source = source

        self.native_size = pygame.image.load(io.BytesIO(source.encode()), "icon.svg").get_size()
        render_size = tuple(max(1, round(d * 4)) for d in self.native_size)
        self.image = pygame.image.load_sized_svg(io.BytesIO(source.encode()), render_size).convert_alpha()

        self.transform()