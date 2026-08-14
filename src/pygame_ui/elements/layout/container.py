from ...element import Element

class Container(Element):
    def __init__(self, parent, offset = (0, 0), stick="", **kwargs):
        self.slots = None
        super().__init__(parent, offset, (0, 0), stick, transparent=True, **kwargs)

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

    def under_mouse(self):
        # Containers are always transparent, so leaf_under_mouse() never
        # resolves to one directly - its bounding box only gates whether to
        # recurse into its children. A child can legitimately have a hit
        # area larger than its reported layout size (e.g. an expanded
        # Dropdown), so always recurse and let the children's own
        # under_mouse() decide instead of gating on this box.
        return True

    def _layout(self):
        pass

    def invalidate_layout(self):
        self.slots = None
        self.invalidate_pos()

