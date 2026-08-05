from ..modal_element import ModalElement
from .label import Label

class LabelModal(ModalElement):
    def __init__(self, parent, text, *, max_width = float('inf'), font_size = 15, color = (200, 200, 200), bold = False):
        super().__init__(parent, (0, 0))
        self._label = Label(self, text, (0, 0), "nesw", max_width = max_width, font_size = font_size, color = color, bold = bold)
        self._update_dimensions()

    def _update_dimensions(self):
        self.set_dimensions(self._label.width, self._label.height)

    def set_text(self, new_text):
        self._label.set_text(new_text)
        self._update_dimensions()

    def draw(self, surface):
        self._label.draw(surface)