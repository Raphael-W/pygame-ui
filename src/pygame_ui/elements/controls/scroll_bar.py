import pygame

from ...utils import mult_color
from .sliding_element import SlidingElement

class ScrollBar(SlidingElement):
    style_defaults = {"track_color": (100, 100, 100), "border_radius": 5, "handle_color": (50, 50, 50)}

    def __init__(self, parent, visible_height, section_height, offset = (0, 0), stick = "", **kwargs):
        super().__init__(parent, 'y', (0, section_height), offset, (15, visible_height), stick, handle_length=visible_height, **kwargs)

        self.section_height = section_height
        self.visible_height = visible_height
        self.set_value(0)

    def set_section_height(self, value):
        self.section_height = value
        self.value_range = (0, value)
        self.set_value(0)

    def _get_handle_length(self):
        if self.section_height == 0:
            return 0
        height = (self.visible_height / self.section_height) * self.visible_height
        return min(height, self.visible_height)

    def under_mouse(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        rel_handle_x, rel_handle_y = self._get_rel_handle_pos()
        x_collide = (rel_handle_x - (self.width / 2)) <= rel_mouse_x <= (rel_handle_x + (self.width / 2))
        y_collide = (rel_handle_y <= rel_mouse_y <= (rel_handle_y + self._get_handle_length()))
        return x_collide and y_collide

    def draw_track(self, surface, x, y):
        pygame.draw.rect(surface, self.style["track_color"], (x, y, self.width, self.height), 0, self.style["border_radius"])

    def draw_handle(self, surface, x, y):
        color = self.style["handle_color"]
        if self.handle_selected:
            color = mult_color(color, 0.8)
        pygame.draw.rect(surface, color, ((x - self.width / 2), y, self.width, round(self._get_handle_length())), 0, self.style["border_radius"])