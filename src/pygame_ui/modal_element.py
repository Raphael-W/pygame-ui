from .element import Element

class ModalElement(Element):
    def __init__(self, opener, dimensions):
        root = opener.get_root()
        super().__init__(root, (0, 0), dimensions, "nesw", True, False, -1)

        layer.add_modal(self)

    def close(self):
        self.remove()
        self.parent.remove_modal(self)
