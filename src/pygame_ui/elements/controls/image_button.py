import pygame
from .button import Button
from ..display.image import Image

class ImageButton(Button):
    style_defaults = {"image_color": (200, 200, 200), "image_scale": 1, "image_rotation": 0}

    def __init__(self, parent, source, offset = (0, 0), dimensions = (100, 30), stick = "", image_offset = (0, 0), action = None, **kwargs):
        super().__init__(parent, None, offset, dimensions, stick, action=action, **kwargs)
        image = Image(self, source, image_offset, "nesw", transparent = True)
        self.register_style_mapping(image, {"color": "image_color", "scale": "image_scale", "rotation": "image_rotation"})
        self.set_content_element(image)

    def set_source(self, new_source):
        self.content.load_source(new_source)

