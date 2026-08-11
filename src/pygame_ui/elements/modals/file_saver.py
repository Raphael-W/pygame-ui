import pygame
import os
from .modal_element import ModalElement
from ..display import Label
from ..controls import TextButton, TextInput, ImageButton
from ...utils import asset_path

class FileSaver(ModalElement):
    style_defaults = {"bg_color": (70, 70, 70), "button_color": (120, 120, 120), "border_radius": 15, "font_color": (200, 200, 200)}

    def __init__(self, layer, directory, file_extension, action, title = "Save", *, placeholder = "File name", value = "", **kwargs):
        super().__init__(layer, (350, 175), **kwargs)

        self.directory = directory
        self.file_extension = file_extension
        self.title = title
        self.action = action

        self.existing_files = [name for name in os.listdir(self.directory)]

        Label(self, self.title, (0, 20), "new", styling={"font_size": 28, "bold": True, "color": self.style["font_color"]})
        self.name_input = TextInput(self, (0, 70), "sew", styling={"length": self.width - 30, "font_size": 21, "color": (50, 50, 50), "font_color": self.style["font_color"]}, placeholder = placeholder, text = value, character_blacklist = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"], pattern_check = r'.+', verification_function = self.check_name, action = self.save_file)
        self.save_button = TextButton(self, self.title, (0, 15), (self.width - 30, 40), "sew", styling={"font_size": 18, "color": self.style["button_color"], "font_color": self.style["font_color"]}, action = self.save_file)
        ImageButton(self, asset_path("icons", "cross.png"), (15, 15), (30, 30), "ne", styling={"color": self.style["button_color"], "image_color": (200, 200, 200), "image_scale": 0.8}, action = self.close)

        self.get_root().set_focus(self.name_input)

    def _get_file_name(self):
        return self.name_input.get_value() + "." + self.file_extension

    def check_name(self, *args):
        return self._get_file_name() not in self.existing_files

    def save_file(self, *args):
        file_path = os.path.join(self.directory, self._get_file_name())
        self.action(file_path)
        self.close()

    def visible_update(self):
        self.save_button.set_disabled(not self.name_input.validate_text())

    def draw(self, surface):
        x, y = self.get_pos()
        pygame.draw.rect(surface, self.style["bg_color"], (x, y, self.width, self.height), border_radius = self.style["border_radius"])
        self.draw_children(surface)
