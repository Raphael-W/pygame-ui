import pygame
import pygame.freetype

from ..utils import mult_color
from ..element import Element
from .label import Label
from .image import Image

class Button (Element):
    def __init__(self, parent, content, offset = (0, 0), dimensions = (200, 50), stick = "nesw", *, color = (100, 100, 100), rounded = 10, action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, offset, dimensions, stick, show, disabled, child_index)
        self.content = content

        self.color = color
        self.rounded = rounded

        self.action = action

        self._captured = False

    def get_content_element(self):
        return self.content

    def set_content_element(self, element):
        self.content = element
        self.set_disabled(self.disabled)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._captured = True
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._captured and self.action is not None:
                self.action()
            self._captured = False
            return False

        return False

    def draw(self, surface):
        x, y = self.get_pos()
        is_clicked = self.hovered and pygame.mouse.get_pressed()[0]

        color = self.color
        if is_clicked or self.disabled:
            color = mult_color(color, 0.7)
        elif self.hovered:
            color = mult_color(color, 0.8)

        if isinstance(self.rounded, tuple) or isinstance(self.rounded, list):
            pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0,
                             border_top_left_radius = self.rounded[0],
                             border_top_right_radius = self.rounded[1],
                             border_bottom_right_radius = self.rounded[2],
                             border_bottom_left_radius = self.rounded[3])
        else:
            pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, self.rounded)
        self.draw_children(surface)
