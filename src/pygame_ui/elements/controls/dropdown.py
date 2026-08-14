import pygame
from ...element import Element
from .text_button import TextButton
from ..display import Image
from ...utils import asset_path, mult_color
from ...theme import Theme
from ..layout import Linker

class Dropdown(Element):
    style_defaults = {"color": (100, 100, 100), "border_radius": 10, "font_color": (200, 200, 200), "icon_color": (200, 200, 200)}

    def __init__(self, parent, options, offset = (0, 0), stick = "", dimensions = (200, 30), action = None, **kwargs):
        super().__init__(parent, offset, dimensions, stick, **kwargs)
        self.options = options
        self.index = 0
        self.expanded = False
        self.action = action

        self.main_button = TextButton(self, options[self.index], (0, 0), (self.width, self.height), stick = "nw", styling={"text_stick": "nsw", "text_offset": (self.height / 2, 0), "padding": 0}, action = self.toggle)
        down_image = Image(self.main_button, asset_path("icons", "down.png"), (self.height / 2, 0), "nes", styling={"scale": 0.8}, transparent = True)
        self.register_style_mapping(down_image, {"color": "icon_color"})

        self.option_buttons = []
        with Linker(self.get_root().get_popover_layer(), self) as linker:
            for i in range(len(options)):
                option_button = TextButton(linker, options[i], (0, self.height * (i + 1)), (self.width, self.height), stick = "nw",
                                           styling={"text_stick": "nsw", "text_offset": (self.height / 2, 0), "padding": 0},
                                           show = False, action = lambda i_snap=i: self.select_option(i_snap))
                self.option_buttons.append(option_button)

        self._restyle_parts()
        self.update_subtree_theme({"border_weight": 0}, TextButton)

    def on_style_changed(self):
        super().on_style_changed()  # re-forwards the registered down_image mapping
        self._restyle_parts()

    def _restyle_parts(self):
        r = min(self.style["border_radius"], self.height // 2)
        common = {"color": self.style["color"], "font_color": self.style["font_color"]}

        self.main_button.update_styling({**common, "border_radius": (r, r, 0, 0) if self.expanded else r})
        for i, button in enumerate(self.option_buttons):
            button.update_styling({**common,"border_radius": (0, 0, r, r) if i == len(self.option_buttons) - 1 else 0})

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

        for option_button in self.option_buttons:
            option_button.set_show(self.expanded)

    def toggle(self):
        self.set_expanded(not self.expanded)

    def deselect(self, up_to = None):
        super().deselect()
        self.set_expanded(False)

    # def under_mouse(self):
    #     rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
    #     current_height = self.height
    #     if self.expanded:
    #         current_height = self.height * (len(self.options) + 1)
    #     return (0 <= rel_mouse_x < self.width) and (0 <= rel_mouse_y < current_height)

    def select_option(self, option_index):
        self.set_expanded(False)
        option = self.options[option_index]
        self.main_button.set_text(option)
        if self.action is not None:
            self.action(option)

    def draw(self, surface):
        x, y = self.get_pos()
        self.draw_children(surface)
        if self.expanded:
            weight = 1
            pygame.draw.line(surface, (90, 90, 90), (x, y + self.height - weight), (x + self.width - 1, y + self.height - weight), weight)