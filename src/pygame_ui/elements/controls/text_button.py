import pygame
from .button import Button
from ..display.label import Label

class TextButton(Button):
    style_defaults = {"font_size": 15, "font_color": (200, 200, 200), "text_offset": (0, 0), "text_stick": "nesw"}

    def __init__(self, parent, text, offset = (0, 0), dimensions = (200, 50), stick = "", *, action = None, show = True, disabled = False, styling=None, child_index = -1):
        super().__init__(parent, None, offset, dimensions, stick, action=action, show=show, disabled=disabled, styling=styling, child_index=child_index)
        self.set_content_element(Label(self, text, self.style["text_offset"], self.style["text_stick"], styling = {"font_size": self.style["font_size"], "color": self.style["font_color"]}))

    def set_text(self, new_text):
        self.content.set_text(new_text)