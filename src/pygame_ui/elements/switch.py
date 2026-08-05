import pygame
import pygame.gfxdraw
from ..utils import mult_color
from ..element import Element

class Switch (Element):
    def __init__(self, parent, offset = (0, 0), scale = 1, stick = "nesw", *, value = True, action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, offset, (55 * scale, 25 * scale), stick, show, disabled, child_index)

        self.value = value
        self.scale = scale
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
            color = (41, 66, 43)
        else:
            circleOffset = 0
            color = (66, 41, 41)

        if self.hovered:
            color = mult_color(color, 0.8)

        handle_color = (20, 20, 20)
        if self.disabled:
            handle_color = (43, 33, 33)

        pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, 100)

        pygame.gfxdraw.aacircle(surface, int(x + (self.width / 4) + circleOffset), int(y + (self.height / 2)), int(9 * self.scale), handle_color)
        pygame.gfxdraw.filled_circle(surface, int(x + (self.width / 4) + circleOffset), int(y + (self.height / 2)), int(9 * self.scale), handle_color)
        self.draw_children(surface)