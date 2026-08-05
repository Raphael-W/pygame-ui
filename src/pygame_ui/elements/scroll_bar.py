import pygame

from ..utils import mult_color
from ..sliding_element import SlidingElement

class ScrollBar(SlidingElement):
    def __init__(self, parent, offset, visible_height, section_height, stick, *, disabled = False):
        super().__init__(parent, 'y', (0, section_height), offset, (15, visible_height), stick, handle_length=visible_height, show=True, disabled=disabled, child_index=-1)

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
        pygame.draw.rect(surface, (100, 100, 100), (x, y, self.width, self.height), 0, 5)

    def draw_handle(self, surface, x, y):
        color = (50, 50, 50)
        if self.under_mouse():
            color = mult_color(color, 0.8)
        pygame.draw.rect(surface, color, ((x - self.width / 2), y, self.width, round(self._get_handle_length())), 0, 5)