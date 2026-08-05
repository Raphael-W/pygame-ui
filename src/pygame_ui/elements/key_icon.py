import pygame

from ..element import Element
from .label import Label
from ..utils import mult_color

class KeyIcon(Element):
    def __init__(self, parent, key, offset, size, stick, *, color = (100, 100, 100), show = True, child_index = -1):
        super().__init__(parent, offset, (30 * size, 30 * size), stick, show, child_index)

        self.key = key
        self.color = color
        Label(self, self._get_key_text(), (0, 0), "nesw", font_size = 18 * size)

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
        color = self.color
        if keys[self.key]:
            color = (mult_color(color, 0.6))

        x, y = self.get_pos()
        pygame.draw.rect(surface, color, (x, y, self.width, self.height), 0, 8)
        self.draw_children(surface)