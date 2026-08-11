import pygame
from .modal_element import ModalElement
from ..display.label import Label
from ..controls.image_button import ImageButton
from ..controls.text_button import TextButton
from ...utils import asset_path

class Message(ModalElement):
    style_defaults = {"title_font_size": 25, "message_font_size": 15, "padding": 15, "border_radius": 15, "bg_color": (70, 70, 70), "font_color": (200, 200, 200), "button1_color": (120, 120, 120), "button1_font_color": (200, 200, 200), "button2_color": (95, 25, 25), "button2_font_color": (200, 200, 200)}

    def __init__(self, parent, title, message, button1, button2 = None, *, close_action = None, **kwargs):
        super().__init__(parent, (400, 0), **kwargs)
        padding =  self.style["padding"]

        self.title = Label(self, title, (0, (2 * padding)), "new", styling={"font_size": self.style["title_font_size"], "color": self.style["font_color"], "max_width": self.width - 30 - (2 * padding)})
        self.message = Label(self, message, (0, self.title.height + self.title.offset_y + (1.5 *  padding)), "new", styling={"font_size": self.style["message_font_size"], "color": self.style["font_color"], "max_width": self.width - (4 *  padding)})
        self.set_dimensions(400, self.message.height + self.message.offset_y + 30 + (2.5 *  padding))

        self.close_action = close_action

        self.close_button = ImageButton(self, asset_path("icons", "cross.png"), (padding, padding), (30, 30), "ne", action = self.close_message, styling={"color": (120, 120, 120), "image_color": (200, 200, 200), "image_scale": 1})

        if button2 is None:
            center_button = TextButton(self, button1[0], (0,  padding), (self.width - (2 * padding), 30), "esw", action = lambda: self.button_action(button1[1]), styling={"color": self.style["button1_color"], "font_color": self.style["button1_font_color"]})
            self.buttons = [center_button]
        else:
            left_button = TextButton(self, button1[0], (padding, padding), ((self.width / 2) - (padding * 1.5), 30), "sw", action = lambda: self.button_action(button1[1]), styling={"color": self.style["button1_color"], "font_color": self.style["button1_font_color"]})
            right_button = TextButton(self, button2[0], (padding, padding), ((self.width / 2) - (padding * 1.5), 30), "se", action = lambda: self.button_action(button2[1]), styling={"color": self.style["button2_color"], "font_color": self.style["button2_font_color"]})
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

        pygame.draw.rect(surface, self.style["bg_color"], (x, y, self.width, self.height), border_radius = self.style["border_radius"])
        self.draw_children(surface)
