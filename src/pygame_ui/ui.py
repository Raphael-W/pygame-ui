import pygame

from .element import Element
from .node import Node
from .elements.modals import ModalLayer
from .elements.display import HoverHint
from .elements.layout import Layer
from .theme import Theme

class UI(Node):
    def __init__(self, surface, theme = None):
        if theme is None:
            theme = Theme()

        super().__init__()
        self.surface = surface
        self.theme = theme

        with Layer(self) as elements_on_top:
            self.modals = ModalLayer(elements_on_top)
            self.popovers = Layer(elements_on_top)
            self.hover_hint = HoverHint(elements_on_top)

        self.focused = None
        self.hovered = None

    def get_modal_layer(self):
        return self.modals

    def get_popover_layer(self):
        return self.popovers

    def get_theme(self):
        return self.theme

    def set_theme(self, theme):
        self.theme = theme
        for child in self.get_children():
            child.trigger_on_style_changed()

    def add_child(self, child, index = -1):
        super().add_child(child, index - 1)

    def handle_events(self, events):
        mouse_events = [e for e in events if e.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL)]
        keyboard_events = [e for e in events if e.type in (pygame.KEYDOWN, pygame.KEYUP, pygame.TEXTINPUT)]

        node = self.focused
        if node is not None:
            for event in keyboard_events:
                while (not node.handle_keyboard_event(event)) and (node.parent is not self) and (node.parent.is_selected()):
                    node = node.parent

        child = self.leaf_under_mouse()
        for event in mouse_events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if child is not None:
                    self.set_focus(child)
                else:
                    self.clear_focus()

            # Every element must receive button releases, whether hovered or not
            if event.type == pygame.MOUSEBUTTONUP:
                for child in self.get_descendants(True, True):
                    child.handle_mouse_event(event)
            else:
                if (child is not None) and (not child.disabled):
                    child.handle_mouse_event(event)

    def draw(self):
        self.invalidate_hovered()

        set_cursor = pygame.SYSTEM_CURSOR_ARROW
        element_under_mouse = None

        for child in reversed(self.get_children(only_visible = True)):
            element_under_mouse = child.leaf_under_mouse()

            if element_under_mouse is not None:
                element_under_mouse.mark_hovered()
                if not element_under_mouse.disabled:
                    set_cursor = element_under_mouse.get_cursor()
                break

        if element_under_mouse is not self.hovered:
            self.hovered = element_under_mouse
            self.hover_hint.set_new_target(element_under_mouse)

        pygame.mouse.set_cursor(set_cursor)

        self.draw_children(self.surface)

    def on_resize(self):
        for child in self.get_children():
            child.on_screen_resize()
            child.invalidate_pos()

    def get_size(self):
        return self.surface.get_size()

    def get_pos(self):
        return 0, 0

    def set_focus(self, element):
        node = self.focused
        if node is not None:
            ancestors = element.get_ancestors()
            while (node is not None) and (node not in ancestors):
                node.deselect()
                node = node.parent

        node = element
        while (node is not self) and (not node.is_selected()):
            node.select()
            node = node.parent

        self.focused = element

    def clear_focus(self):
        node = self.focused
        while (node is not self) and (node is not None):
            node.deselect()
            node = node.parent

        self.focused = None

    def invalidate_hovered(self):
        for child in self.get_children():
            child.invalidate_hovered()