from ..layout.layer import Layer
from .scrim import Scrim

class ModalLayer(Layer):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, show=False, **kwargs)
        self.scrim = None # Used as a check to avoid scrim being added as a modal
        self.scrim = Scrim(self)

    def add_child(self, child, child_index = -1):
        super().add_child(child, child_index)
        if self.scrim is None:  # the scrim being attached
            return
        self.bring_child_to_front(self.scrim)
        self.bring_child_to_front(child)
        self.set_show(True)

    def remove_child(self, child):
        super().remove_child(child)
        if len(self.children) == 1: # Only scrim left
            self.set_show(False)
        elif self.children[-1] is self.scrim:  # top modal was removed
            self.bring_child_to_front(self.children[-2])