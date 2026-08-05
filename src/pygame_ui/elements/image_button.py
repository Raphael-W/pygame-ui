import pygame
from .button import Button
from .image import Image

class ImageButton(Button):
    def __init__(self, parent, source, offset = (0, 0), dimensions = (100, 30), stick = "nesw", *, image_scale = 1, image_rotation = 0, image_color = (0, 0, 0), color = (100, 100, 100), image_offset = (0, 0), rounded = 10, action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, None, offset, dimensions, stick, color=color, rounded=rounded, action=action, show=show, disabled=disabled, child_index=child_index)
        self.set_content_element(Image(self, source, image_offset, "nesw", scale = image_scale, rotation = image_rotation, color = image_color, transparent = True))

    def set_source(self, new_source):
        self.content.load_source(new_source)

