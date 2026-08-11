import pygame
from .button import Button
from ..display import Label

class TextButton(Button):
    style_defaults = {"font_size": 15, "font_color": (200, 200, 200), "text_offset": (0, 0), "text_stick": "nesw"}

    def __init__(self, parent, text, offset = (0, 0), dimensions = (200, 50), stick = "", *, action = None, **kwargs):
        super().__init__(parent, None, offset, dimensions, stick, action=action, **kwargs)
        label = Label(self, text, self.style["text_offset"], self.style["text_stick"])
        self.register_style_mapping(label, {"font_size": "font_size", "color": "font_color"})
        self.set_content_element(label)

    def set_text(self, new_text):
        self.content.set_text(new_text)