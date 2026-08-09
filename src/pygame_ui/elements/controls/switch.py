import pygame
import pygame.gfxdraw
from ...utils import mult_color
from ...element import Element

class Switch (Element):
    style_defaults = {"handle_color": (20, 20, 20), "disabled_handle_color": (50, 50, 50), "on_color": (41, 66, 43), "off_color": (66, 41, 41), "scale": 1}
    def __init__(self, parent, offset = (0, 0), stick = "", *, value = True, action = None, **kwargs):
        super().__init__(parent, offset, (0, 0), stick, **kwargs)
        self.set_dimensions(55 * self.style["scale"], 25 * self.style["scale"])
        self.value = value
        self.action = action

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.set_value(not self.value)

    def set_value(self, value):
        self.value = value
        if self.action is not None:
            self.action(value)

    def draw(self, surface):
        x, y = self.get_pos()
        if self.value:
            circleOffset = (self.width / 2)
            color = self.style["on_color"]
        else:
            circleOffset = 0
            color = self.style["off_color"]

        if self.hovered and (not self.disabled):
            color = mult_color(color, 0.8)

        handle_color = self.style["handle_color"]
        if self.disabled:
            handle_color = self.style["disabled_handle_color"]

        pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, 100)

        pygame.gfxdraw.aacircle(surface, int(x + (self.width / 4) + circleOffset), int(y + (self.height / 2)), int(9 * self.style["scale"]), handle_color)
        pygame.gfxdraw.filled_circle(surface, int(x + (self.width / 4) + circleOffset), int(y + (self.height / 2)), int(9 * self.style["scale"]), handle_color)
        self.draw_children(surface)