from .modal_element import ModalElement
from ..display.label import Label

class LabelModal(ModalElement):

    def __init__(self, parent, text, styling=None):
        super().__init__(parent, (0, 0))
        self._label = Label(self, text, (0, 0), "nesw", styling=styling)
        self._update_dimensions()

    def _update_dimensions(self):
        self.set_dimensions(self._label.width, self._label.height)

    def set_text(self, new_text):
        self._label.set_text(new_text)
        self._update_dimensions()

    def draw(self, surface):
        self._label.draw(surface)