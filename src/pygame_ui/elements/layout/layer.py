import pygame

from ...element import Element

class Layer(Element):
    def __init__(self, parent, offset = (0, 0), show = True):
        super().__init__(parent, offset, parent.get_size(), "", show = show, transparent = True)

    def on_resize(self):
        for child in self.get_children():
            child.on_screen_resize()
            child.invalidate_pos()

    def get_size(self):
        return self.parent.get_size()

    def get_head(self):
        if len(self.children) > 0:
            return self.children[-1]

    def get_tail(self):
        if len(self.children) > 0:
            return self.children[:-1]
