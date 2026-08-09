from ...element import Element

class Container(Element):
    def __init__(self, parent, offset = (0, 0), stick="", show=True):
        super().__init__(parent, offset, (0, 0), stick, show, transparent = True)

        self.slots = None

    def add_child(self, child, index = -1):
        super().add_child(child, index)
        self.invalidate_layout()

    def remove_child(self, child):
        super().remove_child(child)
        self.invalidate_layout()

    def move_child(self, child, index):
        self.children.remove(child)
        self.children.insert(index, child)

    def place_child(self, child):
        if self.slots is None:
            self._layout()
        x, y = self.get_pos()
        rel_x, rel_y = self.slots[child]
        return int(x + rel_x), int(y + rel_y)

    def get_size(self):
        if self.slots is None:
            self._layout()
        return super().get_size()

    def _layout(self):
        pass

    def invalidate_layout(self):
        self.slots = None
        self.invalidate_pos()

