import pygame

from .node import Node

class Element(Node):
    def __init__(self, parent, offset, dimensions, stick, show = True, disabled = False, child_index = -1, cursor = pygame.SYSTEM_CURSOR_ARROW, transparent = False):
        super().__init__(parent)
        self.offset_x, self.offset_y = offset
        self.width, self.height = dimensions

        self._x = None
        self._y = None

        self.stick = {s: s.lower() in stick for s in "nesw"}

        self.transparent = transparent #Used to determine whether events should be swallowed

        self.show = show
        self.disabled = disabled
        self.selected = False
        self.hovered = False

        self.cursor = cursor

        parent.add_child(self, child_index)

    def handle_mouse_event(self, event):
        pass

    def handle_keyboard_event(self, event):
        pass

    def on_screen_resize(self):
        pass

    def set_disabled(self, disabled):
        self.disabled = disabled
        for child in self.children:
            child.set_disabled(disabled)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def mark_hovered(self):
        self.hovered = True

    def invalidate_hovered(self):
        self.hovered = False
        for child in self.get_children():
            child.invalidate_hovered()

    def bring_to_front(self):
        self.parent.bring_child_to_front(self)

    def set_show(self, value):
        self.show = value

    # Gets run only if element is showing
    def visible_update(self):
        pass

    # Gets run only regardless of whether element is visible or not
    def update(self):
        pass

    def draw(self, surface):
        self.draw_children(surface)

    def draw_debug_boxes(self, surface):
        for child in self.get_descendants(only_visible=False, only_enabled=False):
            x, y = child.get_pos()
            width, height = child.get_size()
            pygame.draw.rect(surface, (200, 0, 0), (x, y, width, height), 1)

    def get_relative_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.get_pos()
        return mouse_x - x, mouse_y - y

    def under_mouse(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        return (0 <= rel_mouse_x < self.width) and (0 <= rel_mouse_y < self.height)

    def invalidate_pos(self):
        self._x = self._y = None
        for child in self.children:
            child.invalidate_pos()

    def get_pos(self):
        if (self._x is None) or (self._y is None):
            self._x, self._y = self.parent.place_child(self)

        return self._x, self._y

    def get_size(self):
        return self.width, self.height

    def get_cursor(self):
        return self.cursor

    def set_dimensions(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.invalidate_pos()

    def remove(self):
        self.parent.remove_child(self)
