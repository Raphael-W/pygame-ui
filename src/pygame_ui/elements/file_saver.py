import pygame
import os
from ..modal_element import ModalElement
from .label import Label
from .text_button import TextButton
from .text_input import TextInput
from .image_button import ImageButton
from ..utils import asset_path

class FileSaver(ModalElement):
    def __init__(self, layer, directory, file_extension, action, title = "save", *, placeholder = "File name", value = ""):
        super().__init__(layer, (350, 175))

        self.directory = directory
        self.file_extension = file_extension
        self.title = title
        self.action = action

        self.existing_files = [name for name in os.listdir(self.directory)]

        Label(self, self.title, (0, 20), "new", font_size = 28, bold = True)
        self.name_input = TextInput(self, (0, 70), "sew", length = self.width - 30, font_size = 21, color = (50, 50, 50), placeholder = placeholder, text = value, character_blacklist = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"], pattern_check = r'.+', verification_function = self.check_name, action = self.save_file)
        self.save_button = TextButton(self, self.title, (0, 15), (self.width - 30, 40), "sew", font_size = 18, action = self.save_file, color = (120, 120, 120))
        ImageButton(self, asset_path("icons", "cross.png"), (15, 15), (30, 30), "ne", color = (120, 120, 120), image_color = (200, 200, 200), image_scale = 0.8, action = self.close)

        layer.select_child(self.name_input)

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
        pygame.draw.rect(surface, (70, 70, 70), (x, y, self.width, self.height), border_radius = 15)
        self.draw_children(surface)
