from ...element import Element
from .container import Container

class Row(Container):
    def __init__(self, parent, offset = (0, 0), stick="", spacing=10, **kwargs):

        self.spacing = spacing
        super().__init__(parent, offset, stick, **kwargs)

    def _layout(self):
        # TODO: Allow for a width (& height?) rather than always making it based on the size of content
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

        for child in self.slots.keys():
            n, s = child.stick["n"], child.stick["s"]
            x, y = self.slots[child]
            _, child_height = child.get_size()

            if n and s:  # top and bottom (should vertically centre)
                y = ((max_height - child_height) / 2) + y
            elif s:  # bottom-only
                y = max_height - child_height - y

            self.slots[child] = (x, y)