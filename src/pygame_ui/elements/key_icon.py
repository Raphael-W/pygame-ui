import pygame

from ..element import Element
from .label import Label
from ..utils import mult_color

class KeyIcon(Element):
    style_defaults = {"size": 1, "color": (100, 100, 100), "font_color": (200, 200, 200), "font_size": 18, "border_radius": 8, "border_weight": 2, "border_color": (150, 150, 150)}

    def __init__(self, parent, key, offset = (0, 0), stick = "", *, show = True, child_index = -1):
        super().__init__(parent, offset, (0, 0), stick, show, child_index)
        self.set_dimensions(30 * self.style["size"], 30 * self.style["size"])
        self.key = key

        Label(self, self._get_key_text(), (0, 0), "nesw", styling={"font_size": self.style["font_size"] * self.style["size"], "font_color": self.style["font_color"]})

    def _get_key_text(self):
        key_symbols = {
            pygame.K_RIGHT: '→',
            pygame.K_LEFT: '←',
            pygame.K_UP: '↑',
            pygame.K_DOWN: '↓',
            pygame.K_RETURN: '↵',
            pygame.K_KP_ENTER: '↵',
            pygame.K_BACKSPACE: '⌫',
            pygame.K_DELETE: '⌦',
            pygame.K_TAB: '⇥',
            pygame.K_LSHIFT: '⇧',
            pygame.K_RSHIFT: '⇧',
            pygame.K_LCTRL: '⌃',
            pygame.K_RCTRL: '⌃',
            pygame.K_LALT: '⌥',
            pygame.K_RALT: '⌥',
            pygame.K_LGUI: '⌘',
            pygame.K_RGUI: '⌘',
            pygame.K_ESCAPE: 'ESC',
            pygame.K_SPACE: '␣'
        }

        if self.key in key_symbols:
            return key_symbols[self.key]

        return pygame.key.name(self.key).upper()


    def draw(self, surface):
        keys = pygame.key.get_pressed()
        color = self.style["color"]
        if keys[self.key]:
            color = (mult_color(color, 0.6))

        x, y = self.get_pos()
        pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, self.style["border_radius"])
        if (border_weight := self.style["border_weight"]) > 0:
            pygame.draw.rect(surface, self.style["border_color"], (x, y, self.width, self.height), border_weight, self.style["border_radius"])
        self.draw_children(surface)