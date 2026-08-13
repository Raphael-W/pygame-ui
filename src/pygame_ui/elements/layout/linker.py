from ...element import Element

class Linker(Element):
    def __init__(self, parent, element, **kwargs):
        super().__init__(parent, (0, 0), dimensions=element.get_size(), stick=element.stick, transparent=True, **kwargs)
        self._element = element

    def get_pos(self):
        return self._element.get_pos()

    def get_theme(self):
        return self._element.get_theme()

    def under_mouse(self):
        return True

    def get_acting_parent(self):
        return self._element