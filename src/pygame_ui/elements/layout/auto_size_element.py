from ...element import Element

class AutoSizeElement(Element):
    style_defaults = {"padding": (0, 0)}

    def __init__(self, parent, offset=(0, 0), dimensions=None, stick="", **kwargs):
        dimensions = dimensions or (None, None)
        self.fit_width_to_content = dimensions[0] is None
        self.fit_height_to_content = dimensions[1] is None

        self.user_dimensions = dimensions

        super().__init__(parent, offset, (0, 0), stick, **kwargs)
        self.set_auto_dimensions()

    def get_size(self):
        auto_width, auto_height = self.get_auto_size()
        user_width, user_height = self.user_dimensions

        if self.fit_width_to_content:
            width = auto_width
        else:
            width = user_width

        if self.fit_height_to_content:
            height = auto_height
        else:
            height = user_height

        return width, height

    def get_auto_size(self):
        children = self.get_children(only_visible=True)
        if len(children) == 0:
            return 100, 100

        width = height = 0
        for child in children:
            child_width, child_height = self._child_extent(child)
            width = max(width, child_width)
            height = max(height, child_height)

        return self._apply_padding((width, height))

    def _child_extent(self, child):
        # How much content-box size this one child needs
        stick = child.stick
        n, e, s, w = stick["n"], stick["e"], stick["s"], stick["w"]

        width = child.width if (e and w) else child.offset_x + child.width
        height = child.height if (n and s) else child.offset_y + child.height

        return width, height

    def set_auto_dimensions(self):
        # Apply the computed size directly; bypass set_dimensions() so this
        # internal recompute doesn't get mistaken for a user-set explicit
        # dimension and clobber fit_width/height_to_content.
        Element.set_dimensions(self, *self.get_size())

    def set_dimensions(self, new_width, new_height):
        self.fit_width_to_content = new_width is None
        self.fit_height_to_content = new_height is None
        self.user_dimensions = (new_width, new_height)

        user_width, user_height = self.user_dimensions
        if not self.fit_width_to_content:
            user_width = new_width
        if not self.fit_height_to_content:
            user_height = new_height
        self.user_dimensions = (user_width, user_height)

        super().set_dimensions(new_width, new_height)

    def _normalised_padding(self) -> tuple:
        padding = self.style["padding"]

        if isinstance(padding, int) or isinstance(padding, float):
            return (padding,) * 4
        elif isinstance(padding, tuple) or isinstance(padding, list):
            if len(padding) == 2:
                return padding[1], padding[0], padding[1], padding[0]
            elif len(padding) >= 4:
                return tuple(padding[:4])

    def _apply_padding(self, dimensions):
        width, height = dimensions
        padding = self._normalised_padding()
        return width + padding[1] + padding[3], height + padding[0] + padding[2]

    def place_child(self, child):
        parent_x, parent_y = self.get_pos()
        parent_width, parent_height = self.get_size()
        top, right, bottom, left = self._normalised_padding()

        inner_x = parent_x + left
        inner_y = parent_y + top
        inner_width = parent_width - left - right
        inner_height = parent_height - top - bottom

        stick = child.stick
        n, e, s, w = stick["n"], stick["e"], stick["s"], stick["w"]

        if e and w:
            x = inner_x + ((inner_width - child.width) / 2) + child.offset_x
        elif e:
            x = inner_x + inner_width - child.width - child.offset_x
        else:
            x = inner_x + child.offset_x

        if n and s:
            y = inner_y + ((inner_height - child.height) / 2) + child.offset_y
        elif s:
            y = inner_y + inner_height - child.height - child.offset_y
        else:
            y = inner_y + child.offset_y

        return int(x), int(y)

    def add_child(self, child, index = -1):
        super().add_child(child, index)
        self.set_auto_dimensions()

    def remove_child(self, child):
        super().remove_child(child)
        self.set_auto_dimensions()