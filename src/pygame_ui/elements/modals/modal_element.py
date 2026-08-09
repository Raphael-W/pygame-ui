from ...element import Element

class ModalElement(Element):
    def __init__(self, opener, dimensions, **kwargs):
        root = opener.get_root()
        modal_layer = root.get_modal_layer()

        super().__init__(modal_layer, (0, 0), dimensions, stick="nesw", show=True, disabled=False, **kwargs)

    def close(self):
        self.remove()
