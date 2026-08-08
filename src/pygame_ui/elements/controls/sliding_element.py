import pygame
import pygame.gfxdraw
from ...element import Element
from ..display.label import Label
from ...utils import get_precision, mult_color

class SlidingElement (Element):
    def __init__(self, parent, axis = 'x', value_range = (1, 100), offset = (0, 0), dimensions = (200, 30), stick = "nesw", *, handle_length = 0, value = 0, increment = 1, action = None, finished_action = None, show = True, disabled = False, styling=None, child_index = -1):
        super().__init__(parent, offset, dimensions, stick, show, disabled, child_index, styling=styling)
        if axis not in ('x', 'y'):
            raise ValueError("Axis must be either 'x' or 'y'")

        self.axis = axis
        self.value_range = value_range
        self.value = value
        self.handle_length = handle_length
        self.increment = increment

        if self.axis == "x":
            self.bar_length, self.bar_thickness = dimensions
        else: #self.axis == "y"
            self.bar_thickness, self.bar_length = dimensions

        self.change_action = action
        self.finished_change_action = finished_action

        self.handle_selected = False
        self.mouse_handle_offset = (0, 0)
        self._from_value = value

    def _value_to_axis(self, value):
        if (self.value_range[1] - self.value_range[0]) == 0:
            return 0
        pixel_per_value = self.bar_length / (self.value_range[1] - self.value_range[0])
        return (value - self.value_range[0]) * pixel_per_value

    def _axis_to_value(self, rel_axis):
        value_per_pixel = (self.value_range[1] - self.value_range[0]) / self.bar_length
        return round(int(((rel_axis * value_per_pixel) + self.value_range[0]) / self.increment) * self.increment, get_precision(self.increment))

    def _get_rel_handle_pos(self):
        if self.axis == 'x':
            return self._value_to_axis(self.value), self.bar_thickness / 2
        else:  #self.axis == 'y'
            return self.bar_thickness / 2, self._value_to_axis(self.value)

    def under_mouse(self):
        return True

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_selected = True
            self._from_value = self.value

            rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
            rel_handle_x, rel_handle_y = self._get_rel_handle_pos()
            self.mouse_handle_offset = (rel_mouse_x - rel_handle_x, rel_mouse_y - rel_handle_y)
            return True

    def visible_update(self):
        if not pygame.mouse.get_pressed()[0] and self.handle_selected:
            self.handle_selected = False
            if self.finished_change_action is not None:
                self.finished_change_action(self._from_value, self.value)

        if self.handle_selected:
            if self.change_action is not None:
                self.change_action(self.value)

            if self.axis == 'x':
                mouse_axis = self.get_relative_mouse()[0] - self.mouse_handle_offset[0]
            else: #self.axis == 'y'
                mouse_axis = self.get_relative_mouse()[1] - self.mouse_handle_offset[1]

            self.set_value(self._axis_to_value(mouse_axis))

    def set_value(self, value):
        min_value = self.value_range[0]
        max_value = self.value_range[1] - self.handle_length
        self.value = max(min(value, max_value), min_value)

    def get_value(self):
        return self.value

    def draw_handle(self, surface, x, y):
        pass

    def draw_track(self, surface, x, y):
        pass

    def draw(self, surface):
        x, y = self.get_pos()
        self.draw_track(surface, round(x), round(y))

        handle_rel_x, handle_rel_y = self._get_rel_handle_pos()
        self.draw_handle(surface, round(x + handle_rel_x), round(y + handle_rel_y))