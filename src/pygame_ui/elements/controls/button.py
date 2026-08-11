import pygame
import pygame.freetype

from ...utils import mult_color
from ...element import Element
from ..display import Label, Image

class Button (Element):
    style_defaults = {"color": (100, 100, 100), "border_radius": 10, "border_weight": 0, "border_color": (100, 100, 100)}

    def __init__(self, parent, content = None, offset = (0, 0), dimensions = (200, 50), stick = "", action = None, **kwargs):
        super().__init__(parent, offset, dimensions, stick, **kwargs)
        self.content = content
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

        color = self.style["color"]
        if is_clicked or self.disabled:
            color = mult_color(color, 0.7)
        elif self.hovered:
            color = mult_color(color, 0.8)

        border_radius = self.style["border_radius"]
        if isinstance(border_radius, tuple) or isinstance(border_radius, list):
            pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0,
                             border_top_left_radius = border_radius[0],
                             border_top_right_radius = border_radius[1],
                             border_bottom_right_radius = border_radius[2],
                             border_bottom_left_radius = border_radius[3])
        else:
            pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, border_radius)
            if (border_weight := self.style["border_weight"]) > 0:
                pygame.draw.rect(surface, self.style["border_color"], (x, y, self.width, self.height), border_weight, border_radius)
        self.draw_children(surface)
