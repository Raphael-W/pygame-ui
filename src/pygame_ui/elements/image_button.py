import pygame
from .button import Button
from .image import Image

class ImageButton(Button):
    style_defaults = {"image_color": (200, 200, 200)}

    def __init__(self, parent, source, offset = (0, 0), dimensions = (100, 30), stick = "nesw", *, image_scale = 1, image_rotation = 0, image_offset = (0, 0), action = None, show = True, disabled = False, styling = None, child_index = -1):
        super().__init__(parent, None, offset, dimensions, stick, action=action, show=show, disabled=disabled, child_index=child_index, styling = styling)
        self.set_content_element(Image(self, source, image_offset, "nesw", scale = image_scale, rotation = image_rotation, color = self.style["image_color"], transparent = True))

    def set_source(self, new_source):
        self.content.load_source(new_source)

