import pygame
from ..modal_element import ModalElement
from .label import Label
from .image_button import ImageButton
from .text_button import TextButton
from ..utils import asset_path

class Message(ModalElement):
    def __init__(self, parent, title, message, button1, button2 = None, *, padding = 15, title_font_size = 25, message_font_size = 15, close_action = None):
        super().__init__(parent, (400, 0))

        self.title = Label(self, title, (0, (2 * padding)), "new", font_size = title_font_size, max_width = self.width - 30 - (2 * padding))
        self.message = Label(self, message, (0, self.title.height + self.title.offset_y + (1.5 * padding)), "new", font_size = message_font_size, max_width = self.width - (4 * padding))
        self.set_dimensions(400, self.message.height + self.message.offset_y + 30 + (2.5 * padding))

        self.close_action = close_action

        self.close_button = ImageButton(self, asset_path("icons", "cross.png"), (padding, padding), (30, 30), "ne", action = self.close_message, color = (120, 120, 120), image_color = (200, 200, 200), image_scale = 1)

        if button2 is None:
            center_button = TextButton(self, button1[0], (0, padding), (self.width - (2 * padding), 30), "esw", action = lambda: self.button_action(button1[1]), color = (120, 120, 120))
            self.buttons = [center_button]
        else:
            left_button = TextButton(self, button1[0], (padding, padding), ((self.width / 2) - (padding * 1.5), 30), "sw", action = lambda: self.button_action(button1[1]), color = (120, 120, 120))
            right_button = TextButton(self, button2[0], (padding, padding), ((self.width / 2) - (padding * 1.5), 30), "se", action = lambda: self.button_action(button2[1]), color = (95, 25, 25))
            self.buttons = [left_button, right_button]

    def close_message(self):
        if self.close_action is not None:
            self.close_action()
        self.close()

    def button_action(self, action):
        if action is not None:
            action()
        self.close_message()

    def draw(self, surface):
        x, y = self.get_pos()

        pygame.draw.rect(surface, (70, 70, 70), (x, y, self.width, self.height), border_radius = 15)
        self.draw_children(surface)
