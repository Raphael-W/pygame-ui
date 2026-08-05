import pygame
from ..element import Element
from .text_button import TextButton
from .image import Image
from ..utils import asset_path, mult_color

class Dropdown(Element):
    def __init__(self, parent, options, offset = (0, 0), stick = "nesw", dimensions = (200, 30), index = 0, color = (100, 100, 100), action = None, show = True, disabled = False, layerIndex = -1):
        super().__init__(parent, offset, (dimensions[0], dimensions[1] * (len(options) + 1)), stick, show, disabled, layerIndex)
        self.options = options
        self.index = index
        self.expanded = False

        self.option_height = dimensions[1]

        self.action = action

        main_button = TextButton(self, options[index], (0, 0), (self.width, self.option_height), stick = "nw", rounded = 10, color = color, text_stick = "nsw", text_offset = (self.option_height / 2, 0), action = self.toggle)
        Image(main_button, asset_path("icons", "down.png"), (self.option_height / 2, 0), "nes", color = (200, 200, 200), scale = 0.8, transparent = True)
        for i in range(len(options)):
            rounded = 0
            if i == len(options) - 1:
                rounded = (0, 0, 10, 10)

            TextButton(self, options[i], (0, self.option_height * (i + 1)), (self.width, self.option_height), stick = "nw", rounded = rounded, show = False, color = color, text_stick = "nsw", text_offset = (self.option_height / 2, 0), action = lambda i_snap=i: self.select_option(i_snap))

    def set_expanded(self, expanded):
        self.expanded = expanded
        main_button = self.get_children(only_visible = False)[0]
        if self.expanded:
            self.bring_to_front()
            main_button.rounded = (10, 10, 0, 0)
            main_button.get_children(instance = Image)[0].transform(rotation = 180)
        else:
            main_button.rounded = 10
            main_button.get_children(instance = Image)[0].transform(rotation = 0)

        for option_button in self.get_children(only_visible = False, instance = TextButton)[1:]:
            option_button.set_show(self.expanded)

    def toggle(self):
        self.set_expanded(not self.expanded)

    def deselect(self, up_to = None):
        super().deselect()
        self.set_expanded(False)

    def under_mouse(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        current_height = self.option_height
        if self.expanded:
            current_height = self.option_height * (len(self.options) + 1)
        return (0 <= rel_mouse_x < self.width) and (0 <= rel_mouse_y < current_height)

    def select_option(self, option_index):
        self.set_expanded(False)
        option = self.options[option_index]
        self.get_children(instance = TextButton)[0].set_text(option)
        if self.action is not None:
            self.action(option)

    def draw(self, surface):
        x, y = self.get_pos()
        self.draw_children(surface)
        if self.expanded:
            pygame.draw.line(surface, (90, 90, 90), (x, y + self.option_height), (x + self.width - 1, y + self.option_height), 1)