import pygame
import pygame.gfxdraw
import pygame.freetype
import time
import re

from ...utils import mult_color, asset_path
from ...element import Element
from ..display import Label
from .image_button import ImageButton

class TextInput(Element):
    style_defaults = {"length": 50, "font_size": 20, "font_color": (200, 200, 200), "placeholder_font_color": (150, 150, 150), "color": (70, 70, 70), "border_radius": 15, "button_color": (100, 100, 100), "button_border_radius": 15, "button_icon_color": (200, 200, 200)}

    def __init__(self, parent, offset = (0, 0), stick = "", *, placeholder = "", text = "", suffix = "", character_whitelist = None, character_blacklist = None, pattern_check = None, verification_function = None, action = None, type_action = None, **kwargs):
        super().__init__(parent, offset, (0, 0), stick, **kwargs)

        self.set_dimensions(self.style["length"], self.style["font_size"] * 2)

        self.placeholder = placeholder
        self.text = text
        self.suffix = suffix

        self.char_whitelist = set(character_whitelist) if character_whitelist is not None else None
        self.char_blacklist = set(character_blacklist) if character_blacklist is not None else None
        self.pattern_check = pattern_check
        self.verification_function = verification_function

        self.font = None

        self.clear_button = ImageButton(self, asset_path("icons", "cross.png"), (self.height * 0.15, 0), (self.height * 0.7, self.height * 0.7), "nes", styling={"image_scale": 0.04 * self.style["font_size"]}, action = self.clear)
        self.register_style_mapping(self.clear_button, {"color": "button_color", "border_radius": "button_border_radius", "image_color": "button_icon_color"})

        self.action = action
        self.type_action = type_action

        self.cursor_index = 0
        self.cursor_blink_speed = 0.7
        self.last_input_time = time.time()

        self.x_padding = 15

        self.text_x_offset = 0
        self.text_x_offset_stick = "r"
        self.anchor_char_index = None

        self.initial_key_hold_wait = 0.5
        self.key_hold_speed = 0.05
        self.key_holding = {pygame.K_BACKSPACE: {"time": None, "action": self._backspace},
                            pygame.K_LEFT:      {"time": None, "action": self._left_cursor},
                            pygame.K_RIGHT:     {"time": None, "action": self._right_cursor}}

        self.update_subtree_theme({"cursor": pygame.SYSTEM_CURSOR_IBEAM}, cls=TextInput)
        self.on_style_changed()

    def on_style_changed(self):
        super().on_style_changed()
        self.clear_button.update_styling_property("image_scale", 0.04 * self.style["font_size"])
        self.font = pygame.freetype.Font(self.style["font_path"], self.style["font_size"])
        self.font.origin = True

        self.set_dimensions(self.style["length"], self.style["font_size"] * 2)

    def _backspace(self):
        if self.cursor_index > 0:
            self.text = self.text[:self.cursor_index - 1] + self.text[self.cursor_index:]
        self.anchor_char_index = self.cursor_index
        self._left_cursor()
        self.text_x_offset_stick = "r"

    def _left_cursor(self):
        self.cursor_index = max(self.cursor_index - 1, 0)
        self.last_input_time = time.time()
        self.text_x_offset_stick = "l"

    def _right_cursor(self):
        self.cursor_index = min(self.cursor_index + 1, len(self.text) + 1)
        self.last_input_time = time.time()
        self.text_x_offset_stick = "r"

    def calculate_text_width(self, to_index = -1):
        if to_index < 0:
            to_index = len(self.text)
        return sum(m[4] for m in self.font.get_metrics(self.text[:to_index]))

    def index_at_x(self, text_x):
        advance = 0
        for i, m in enumerate(self.font.get_metrics(self.text)):
            if text_x < advance + m[4] / 2:  # nearer the left edge of this char
                return i
            advance += m[4]
        return len(self.text)

    def clear(self):
        self.text = ""
        self.cursor_index = 0
        if self.type_action is not None:
            self.type_action()

    def get_value(self):
        return self.text

    def select(self):
        super().select()
        self.cursor_index = len(self.text)

    def deselect(self):
        super().deselect()
        self.cursor_index = 0

    def validate_text(self):
        pattern = True
        if self.pattern_check is not None:
            pattern = bool(re.fullmatch(self.pattern_check, self.text))

        verification = True
        if self.verification_function is not None:
            verification = self.verification_function(self.text)

        return pattern and verification

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_holding:
                hold_data = self.key_holding[event.key]
                hold_data["action"]()
                hold_data["time"] = time.time() + self.initial_key_hold_wait

            elif event.key == pygame.K_RETURN:
                if (self.action is not None) and self.validate_text():
                    self.action(self.text)

            if self.type_action is not None:
                self.type_action()
            return True

        elif event.type == pygame.KEYUP:
            if event.key in self.key_holding:
                hold_data = self.key_holding[event.key]
                hold_data["time"] = None
            return True


        elif event.type == pygame.TEXTINPUT:
            char = event.text
            char_allowed_white = ((self.char_whitelist is not None) and (char in self.char_whitelist)) or self.char_whitelist is None
            char_allowed_black = ((self.char_blacklist is not None) and (char not in self.char_blacklist)) or self.char_blacklist is None
            if char_allowed_white and char_allowed_black:
                self.text = self.text[:self.cursor_index] + char + self.text[self.cursor_index:]
                self._right_cursor()
            if self.type_action is not None:
                self.type_action()
            return True

        return False

    def on_click(self):
        rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
        self.cursor_index = self.index_at_x(rel_mouse_x - self.x_padding - self.text_x_offset)
        self.last_input_time = time.time()

    def visible_update(self):
        for key, data in self.key_holding.items():
            if data["time"] is not None:
                time_since_press = time.time() - data["time"]
                if time_since_press > self.key_hold_speed:
                    data["action"]()
                    data["time"] = time.time()

    def draw(self, surface):
        x, y = self.get_pos()
        pygame.draw.rect(surface, self.style["color"], (x, y, self.width, self.height), border_radius = self.style["border_radius"])
        if self.selected:
            border_color = mult_color(self.style["color"], 1.5)
            if not self.validate_text():
                border_color = (194, 68, 68)
            pygame.draw.rect(surface, border_color, (x - 1, y - 1, self.width + 2, self.height + 2), width = 2, border_radius = self.style["border_radius"])

        if self.text == "":
            text_surface, text_rect = self.font.render(self.placeholder,self.style["placeholder_font_color"])
        else:
            text_surface, text_rect = self.font.render(self.text + self.suffix, self.style["font_color"])

        # --- Handle setting the text x offset ---
        cursor_x = self.x_padding + self.calculate_text_width(self.cursor_index)
        cursor_y = self.height / 2

        close_button_width = self.height * 0.7 + (2 * self.height * 0.15)
        inner_width = self.width - self.x_padding - close_button_width

        visible_left = self.x_padding
        visible_right = self.width - self.x_padding - close_button_width

        if self.anchor_char_index is not None:
            self.text_x_offset = self.anchor_char_index - (self.x_padding + self.calculate_text_width(self.anchor_char_index))
            self.anchor_char_index = None

        else:
            out_of_view = (cursor_x + self.text_x_offset > visible_right or
                           cursor_x + self.text_x_offset < visible_left)

            if out_of_view:
                if self.text_x_offset_stick == "r":
                    self.text_x_offset = visible_right - cursor_x
                else:  # "l"
                    self.text_x_offset = visible_left - cursor_x

        text_width = self.calculate_text_width()
        min_offset = min(0, inner_width - text_width)
        self.text_x_offset = min(max(self.text_x_offset, min_offset), 0)

        # --- Handle blitting the correct portion of the text to the screen---
        area = pygame.Rect(-self.text_x_offset, 0, inner_width, text_surface.get_height())

        dest_x = x + self.x_padding  # text_x_offset is now baked into area, not dest
        dest_y = y - text_rect.y + (self.height * 0.7)

        surface.blit(text_surface, (dest_x, dest_y), area)

        if self.selected:
            show_typing_cursor = (time.time() - self.last_input_time) % (self.cursor_blink_speed * 2) <= self.cursor_blink_speed
            if show_typing_cursor:
                pygame.draw.line(surface, self.style["font_color"], (x + cursor_x + self.text_x_offset, y + cursor_y - (self.height * 0.3)), (x + cursor_x + self.text_x_offset, y + cursor_y + (self.height * 0.3)), 2)
        self.draw_children(surface)