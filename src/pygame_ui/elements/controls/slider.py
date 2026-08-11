import pygame
import pygame.gfxdraw

from .sliding_element import SlidingElement
from ..display import Label
from ...utils import get_precision, mult_color

class Slider (SlidingElement):
    style_defaults = {"handle_size": 1.7, "bar_color": (200, 200, 200), "handle_color": (36, 155, 199), "font_size": 18, "font_color": (200, 200, 200)}

    def __init__(self, parent, value_range = (1, 100), offset = (0, 0), bar_dimensions = (200, 10), stick = "", *, value = 0, increment = 1, suffix = "", action = None, finished_action = None, **kwargs):
        super().__init__(parent, 'x', value_range, offset, bar_dimensions, stick, value=value, increment=increment, action=action, finished_action=finished_action, **kwargs)

        self.label_suffix = suffix
        self.handle_diameter = int(self.style["handle_size"] * self.bar_thickness)

        larger_text = self.value_range[0]
        if len(str(self.value_range[1])) > len(str(self.value_range[0])):
            larger_text = self.value_range[1]

        self.label = Label(self, f"{larger_text}{self.label_suffix}", (self.bar_length + 20, 0), "ns")
        self.register_style_mapping(self.label, {"font_size": "font_size", "color": "font_color"})
        self.set_dimensions(self.bar_length + 20 + self.label.width, self.height)

        self.set_value(value)

    def under_mouse(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        rel_handle_x, rel_handle_y = self._get_rel_handle_pos()
        x_collide = (rel_handle_x - (self.handle_diameter / 2)) <= rel_mouse_x <= (rel_handle_x + (self.handle_diameter / 2))
        y_collide = (rel_handle_y - (self.handle_diameter / 2)) <= rel_mouse_y <= (rel_handle_y + (self.handle_diameter / 2))
        return x_collide and y_collide

    def draw_handle(self, surface, x, y):
        handle_color = self.style["handle_color"]
        if self.hovered or self.handle_selected or self.disabled:
            handle_color = mult_color(handle_color, 0.6)

        pygame.gfxdraw.aacircle(surface, x, y, int(self.handle_diameter / 2), handle_color)
        pygame.gfxdraw.filled_circle(surface, x, y, int(self.handle_diameter / 2), handle_color)

    def draw_track(self, surface, x, y):
        bar_color = self.style["bar_color"]
        if self.disabled:
            bar_color = mult_color(bar_color, 0.6)

        bar = pygame.Rect(x, y, self.bar_length, self.bar_thickness)
        pygame.draw.rect(surface, bar_color, bar, 0, 100)

    def set_value(self, value):
        super().set_value(value)
        self.label.set_text(f"{self.get_value()}{self.label_suffix}")
