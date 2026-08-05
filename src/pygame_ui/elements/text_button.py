import pygame
from .button import Button
from .label import Label

class TextButton(Button):
    def __init__(self, parent, text, offset = (0, 0), dimensions = (200, 50), stick = "nesw", *, font_size = 15, color = (100, 100, 100), font_color = (200, 200, 200), text_offset = (0, 0), text_stick = "nesw", rounded = 10, action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, None, offset, dimensions, stick, color=color, rounded=rounded, action=action, show=show, disabled=disabled, child_index=child_index)
        self.set_content_element(Label(self, text, text_offset, text_stick, font_size = font_size, color = font_color))

    def set_text(self, new_text):
        self.content.set_text(new_text)