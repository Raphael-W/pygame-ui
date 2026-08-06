import pygame

from ..element import Element

class Layer(Element):
    def __init__(self, parent, offset = (0, 0), show = True):
        super().__init__(parent, offset, parent.get_size(), "", transparent = True, show = show)

    def on_resize(self):
        for child in self.get_children():
            child.on_screen_resize()
            child.invalidate_pos()

    def draw(self, surface, debug = False):
        self.draw_children(surface)
        if debug:
            self.draw_debug_boxes()

    def draw_debug_boxes(self, surface):
        for child in self.get_descendants(only_visible=True, only_enabled=False):
            x, y = child.get_pos()
            width, height = child.get_size()
            pygame.draw.rect(surface, (200, 0, 0), (x, y, width, height), 1)

    def get_size(self):
        return self.parent.get_size()

    def get_head(self):
        if len(self.children) > 0:
            return self.children[-1]

    def get_tail(self):
        if len(self.children) > 0:
            return self.children[:-1]
