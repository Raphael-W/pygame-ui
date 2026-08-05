import pygame
import pygame.gfxdraw
from ..sliding_element import SlidingElement
from .label import Label
from ..utils import get_precision, mult_color

class Slider (SlidingElement):
    def __init__(self, parent, value_range = (1, 100), offset = (0, 0), bar_dimensions = (100, 10), handle_size = 2.5, stick = "nesw", *, bar_color = (200, 200, 200), handle_color = (36, 155, 199), font_size = 18, value = 0, increment = 1, suffix = "", action = None, finished_action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, 'x', value_range, offset, bar_dimensions, stick, value=value, increment=increment, action=action, finished_action=finished_action, show=show, disabled=disabled)

        self.label_suffix = suffix

        self.handle_diameter = int(handle_size * self.bar_thickness)

        self.bar_color = bar_color
        self.handle_color = handle_color

        larger_text = self.value_range[0]
        if len(str(self.value_range[1])) > len(str(self.value_range[0])):
            larger_text = self.value_range[1]

        self.label = Label(self, f"{larger_text}{self.label_suffix}", (self.bar_length + 20, 0), "ns", font_size = font_size, color = (200, 200, 200))
        self.set_dimensions(self.bar_length + 20 + self.label.width, self.height)

    def under_mouse(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        rel_handle_x, rel_handle_y = self._get_rel_handle_pos()
        x_collide = (rel_handle_x - (self.handle_diameter / 2)) <= rel_mouse_x <= (rel_handle_x + (self.handle_diameter / 2))
        y_collide = (rel_handle_y - (self.handle_diameter / 2)) <= rel_mouse_y <= (rel_handle_y + (self.handle_diameter / 2))
        return x_collide and y_collide

    def draw_handle(self, surface, x, y):
        handle_color = self.handle_color
        if self.hovered or self.handle_selected or self.disabled:
            handle_color = mult_color(handle_color, 0.6)

        pygame.gfxdraw.aacircle(surface, x, y, int(self.handle_diameter / 2), handle_color)
        pygame.gfxdraw.filled_circle(surface, x, y, int(self.handle_diameter / 2), handle_color)

    def draw_track(self, surface, x, y):
        bar_color = self.bar_color
        if self.disabled:
            bar_color = mult_color(bar_color, 0.6)

        bar = pygame.Rect(x, y, self.bar_length, self.bar_thickness)
        pygame.draw.rect(surface, bar_color, bar, 0, 100)


    def draw(self, surface):
        super().draw(surface)

        self.label.set_text(f"{self.get_value()}{self.label_suffix}")
        self.draw_children(surface)