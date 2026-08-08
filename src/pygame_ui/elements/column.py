from ..element import Element
from ..container import Container

class Column(Container):
    def __init__(self, parent, offset = (0, 0), stick="nw", spacing=10, show=True):
        super().__init__(parent, offset, stick, show)

        self.spacing = spacing

    def _layout(self):
        self.slots = {}

        cursor = 0
        max_width = 0
        for child in self.get_children(only_visible = True):
            child_width, child_height = child.get_size()
            self.slots[child] = (child.offset_x, cursor + child.offset_y)
            cursor += (child_height + child.offset_y + self.spacing)
            max_width = max(max_width, child.offset_x + child_width)

        cursor -= self.spacing
        self.set_dimensions(max_width, cursor)

        start_x, start_y = self.get_pos()
        for child in self.slots.keys():
            e, w = child.stick["e"], child.stick["w"]
            x, y = self.slots[child]

            if e and w:  # left and right (should horizontal centre)
                x = ((max_width - child.width) / 2) + x
            elif e:  # right-only
                x = max_width - child.width - x

            self.slots[child] = (x + start_x, y + start_y)