from ...element import Element
from .container import Container

class Row(Container):
    def __init__(self, parent, offset = (0, 0), stick="nw", spacing=10, show=True):
        super().__init__(parent, offset, stick, show)

        self.spacing = spacing

    def _layout(self):
        self.slots = {}

        cursor = 0
        max_height = 0
        for child in self.get_children(only_visible = True):
            child_width, child_height = child.get_size()
            self.slots[child] = (cursor + child.offset_x, child.offset_y)
            cursor += (child_width + child.offset_x + self.spacing)
            max_height = max(max_height, child.offset_y + child_height)

        cursor -= self.spacing
        self.set_dimensions(cursor, max_height)

        start_x, start_y = self.get_pos()
        for child in self.slots.keys():
            n, s = child.stick["n"], child.stick["s"]
            x, y = self.slots[child]

            if n and s:  # top and bottom (should vertically centre)
                y = ((max_height - child.height) / 2) + y
            elif s:  # bottom-only
                y = max_height - child.height - y

            self.slots[child] = (x + start_x, y + start_y)