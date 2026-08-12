from .modal_element import ModalElement
from ..display import Label

class LabelModal(ModalElement):
    style_defaults = dict(Label.style_defaults)

    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, (0, 0), **kwargs)
        self._label = Label(self, text, (0, 0), "nesw")
        self.register_style_mapping(self._label, {key: key for key in self.style_defaults})
        self._update_dimensions()

    def on_style_changed(self):
        super().on_style_changed()
        self._update_dimensions()

    def _update_dimensions(self):
        self.set_dimensions(self._label.width, self._label.height)

    def set_text(self, new_text):
        self._label.set_text(new_text)
        self._update_dimensions()

    def draw(self, surface):
        self._label.draw(surface)