import pygame
from ...element import Element
from .text_button import TextButton
from ..display import Image
from ...utils import asset_path, mult_color
from ...theme import Theme

class Dropdown(Element):
    style_defaults = {"color": (100, 100, 100), "border_radius": 10, "font_color": (200, 200, 200), "icon_color": (200, 200, 200)}

    def __init__(self, parent, options, offset = (0, 0), stick = "", dimensions = (200, 30), action = None, **kwargs):
        super().__init__(parent, offset, (dimensions[0], dimensions[1] * (len(options) + 1)), stick, **kwargs)
        self.options = options
        self.index = 0
        self.expanded = False

        self.option_height = dimensions[1]

        self.action = action

        main_button = TextButton(self, options[self.index], (0, 0), (self.width, self.option_height), stick = "nw", styling={"text_stick": "nsw", "text_offset": (self.option_height / 2, 0)}, action = self.toggle)
        down_image = Image(main_button, asset_path("icons", "down.png"), (self.option_height / 2, 0), "nes", styling={"scale": 0.8}, transparent = True)
        self.register_style_mapping(down_image, {"color": "icon_color"})

        for i in range(len(options)):
            TextButton(self, options[i], (0, self.option_height * (i + 1)), (self.width, self.option_height), stick = "nw",
                       styling={"text_stick": "nsw", "text_offset": (self.option_height / 2, 0)},
                       show = False, action = lambda i_snap=i: self.select_option(i_snap))

        self._restyle_parts()
        self.update_subtree_theme({"border_weight": 0}, TextButton)

    def on_style_changed(self):
        super().on_style_changed()  # re-forwards the registered down_image mapping
        self._restyle_parts()

    def _restyle_parts(self):
        r = self.style["border_radius"]
        common = {"color": self.style["color"], "font_color": self.style["font_color"]}

        buttons = self.get_children(only_visible = False, instance = TextButton)
        main, options = buttons[0], buttons[1:]

        main.update_styling({**common, "border_radius": (r, r, 0, 0) if self.expanded else r})
        for i, button in enumerate(options):
            button.update_styling({**common,"border_radius": (0, 0, r, r) if i == len(options) - 1 else 0})

    def set_expanded(self, expanded):
        self.expanded = expanded
        self._restyle_parts()

        main_button = self.get_children(only_visible = False)[0]
        arrow_icon = main_button.get_children(instance = Image)[0]

        if self.expanded:
            self.bring_to_front()
            arrow_icon.update_styling_property("rotation", 180)
        else:
            arrow_icon.update_styling_property("rotation", 0)

        for option_button in self.get_children(only_visible = False, instance = TextButton)[1:]:
            option_button.set_show(self.expanded)

    def get_size(self):
        return self.width, self.option_height

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