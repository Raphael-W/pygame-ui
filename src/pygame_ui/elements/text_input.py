import pygame
import pygame.gfxdraw
import pygame.freetype
import time
import re
from ..utils import FONT_PATH, mult_color, asset_path
from ..element import Element
from .image_button import ImageButton

class TextInput(Element):
    def __init__(self, parent, offset = (0, 0), stick = "nesw", *, length = 150, font_size = 15, placeholder = "", text = "", suffix = "", character_whitelist = None, character_blacklist = None, pattern_check = None, verification_function = None, color = (70, 70, 70), action = None, type_action = None, show = True, disabled = False, child_index = -1):
        super().__init__(parent, offset, (length, font_size * 2), stick, show, disabled, child_index, pygame.SYSTEM_CURSOR_IBEAM)

        self.placeholder = placeholder
        self.text = text
        self.suffix = suffix

        self.char_whitelist = set(character_whitelist) if character_whitelist is not None else None
        self.char_blacklist = set(character_blacklist) if character_blacklist is not None else None
        self.pattern_check = pattern_check
        self.verification_function = verification_function

        self.color = color

        self.font = pygame.freetype.Font(FONT_PATH, font_size)
        self.font.origin = True
        self.font_char_width = self.font.get_rect("a").width
        self.font_char_gap = self.font.get_rect("ab").width - (2 * self.font_char_width)

        ImageButton(self, asset_path("icons", "cross.png"), (self.height * 0.15, 0), (self.height * 0.7, self.height * 0.7), "nes", image_color = (200, 200, 200), image_scale = 0.6, action = self.clear)

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
        char_count = len(self.text[:to_index])
        gap_count = max(char_count - 1, 0)

        return (self.font_char_width * char_count) + (self.font_char_gap * gap_count)

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

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.under_mouse():
            rel_mouse_x, rel_mouse_y = self.get_relative_mouse()
            selected_index = (rel_mouse_x - self.font_char_gap - self.text_x_offset + (self.font_char_width / 2)) // (self.font_char_width + self.font_char_gap)
            self.cursor_index = max(min(int(selected_index - 1), len(self.text)), 0)
            self.last_input_time = time.time()
            return True

    def visible_update(self):
        for key, data in self.key_holding.items():
            if data["time"] is not None:
                time_since_press = time.time() - data["time"]
                if time_since_press > self.key_hold_speed:
                    data["action"]()
                    data["time"] = time.time()

    def draw(self, surface):
        x, y = self.get_pos()
        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height), border_radius = 15)
        if self.selected:
            border_color = mult_color(self.color, 1.5)
            if not self.validate_text():
                border_color = (194, 68, 68)
            pygame.draw.rect(surface, border_color, (x - 1, y - 1, self.width + 2, self.height + 2), width = 2, border_radius = 15)

        if self.text == "":
            text_surface, text_rect = self.font.render(self.placeholder,(150, 150, 150))
        else:
            text_surface, text_rect = self.font.render(self.text + self.suffix, (200, 200, 200))

        # --- Handle setting the text x offset ---
        cursor_x = self.x_padding + self.calculate_text_width(self.cursor_index)
        cursor_y = self.height / 2
        inner_width = self.width - (2 * self.x_padding)
        visible_left = self.x_padding
        visible_right = self.width - self.x_padding

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
                pygame.draw.line(surface, (200, 200, 200), (x + cursor_x + self.text_x_offset, y + cursor_y - (self.height * 0.3)), (x + cursor_x + self.text_x_offset, y + cursor_y + (self.height * 0.3)), 2)
        self.draw_children(surface)