import pygame
import time
from ...element import Element
from .label import Label

class HoverHint(Element):
    style_defaults = {"bg_color": (70, 70, 70), "border_radius": 8, "border_weight": 1,
                      "border_color": (200, 200, 200), "font_color": (200, 200, 200), "font_size": 12,
                      "padding": (10, 8), "margins": (0, 2), "show_delay": 0.8}

    def __init__(self, parent, **kwargs):
        super().__init__(parent, (0, 0), (0, 0), "", show=False, transparent=True, **kwargs)
        self.time_of_initial_hover = None
        self.target = None

        self.hint_label = Label(self, "", offset = self.style["padding"], styling={"wrap_mode": "wrap", "max_width": 300}, transparent = True)
        self.register_style_mapping(self.hint_label, {"color": "font_color", "font_size": "font_size"})

    def trigger_on_style_changed(self):
        super().trigger_on_style_changed()
        self.hint_label.offset_x, self.hint_label.offset_y = self.style["padding"]
        self.hint_label.invalidate_pos()

    def get_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        label_w, label_h = self.hint_label.get_size()
        margin_x, margin_y = self.style["margins"]
        pad_x, pad_y = self.style["padding"]

        x = mouse_x + margin_x
        y = mouse_y - label_h - margin_y - (2 * pad_y)

        screen_width, screen_height = self.get_root().get_size()

        full_width = label_w + (2 * pad_x) + margin_x
        if (mouse_x + full_width) > screen_width:
            x = mouse_x - full_width

        full_height = label_h + (2 * pad_y) + margin_y
        if (mouse_y - full_height) < 0:
            y = mouse_y + margin_y

        return x, y

    def cancel_show_countdown(self):
        self.time_of_initial_hover = None

    def reset_show_countdown(self):
        self.time_of_initial_hover = time.time()

    def set_new_target(self, target):
        self.cancel_show_countdown()
        self.invalidate_styling()
        self.target = target

        if target is None: return
        if target.get_hover_hint() is None: return

        self.reset_show_countdown()
        self.hint_label.set_text(target.get_hover_hint())

    def get_theme(self):
        theme_parent = self.parent
        if self.target is not None:
            theme_parent = self.target

        theme = theme_parent.get_theme()  # UI returns self.theme at the root
        return theme.extended(self.subtree_theme)

    def update(self):
        if self.time_of_initial_hover is None:
            self.set_show(False)
            return

        if self.target is not None and self.target.is_held_down():
            self.reset_show_countdown()

        time_since = time.time() - self.time_of_initial_hover
        self.set_show(time_since >= self.style["show_delay"])

    def draw(self, surface):
        x, y = self.get_pos()
        w, h = self.hint_label.get_size()
        pad_x, pad_y = self.style["padding"]

        hint_rect = pygame.Rect(x, y, w + (2 * pad_x), h + (2 * pad_y))

        pygame.draw.rect(surface, self.style["bg_color"], hint_rect, 0, border_radius = self.style["border_radius"])
        if (border_weight := self.style["border_weight"]) > 0:
            pygame.draw.rect(surface, self.style["border_color"], hint_rect, border_weight, border_radius = self.style["border_radius"])

        self.hint_label.invalidate_pos()
        self.draw_children(surface)
