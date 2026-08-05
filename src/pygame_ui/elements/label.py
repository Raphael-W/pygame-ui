import pygame
import pygame.freetype
from ..element import Element
from ..utils import FONT_PATH, mult_color

class Label (Element):
    def __init__(self, parent, text, offset = (0, 0), stick = "nesw", *, max_width = float('inf'), wrap_mode = "wrap", font_size = 15, min_font_size = None, color = (200, 200, 200), bold = False, show = True, child_index = -1):
        self.text = text
        self.font_size = font_size
        self.min_font_size = min_font_size if min_font_size is not None else font_size
        self.max_width = max_width
        self.wrap_mode = wrap_mode
        self.bold = bold
        self.color = color

        self.text_surface = None

        super().__init__(parent, offset, (0, 0), stick, show = show, child_index = child_index, transparent = True)

        self._render_text()

    def _render_text(self, color = None):
        if color is None:
            color = self.color

        split_text = self.text.split(' ')
        font_size = self.font_size
        font = self._create_font(font_size)

        line = []
        lines = []
        for word in split_text:
            potential_line = " ".join(line + [word])
            while (font.get_rect(potential_line).width > self.max_width) and font_size > self.min_font_size:
                font_size -= 1
                font = self._create_font(font_size)

            if font.get_rect(potential_line).width > self.max_width:
                if self.wrap_mode == "ellipse":
                    potential_line = " ".join(line + ["..."])
                    while font.get_rect(potential_line).width > self.max_width:
                        line.pop()
                        potential_line = " ".join(line + ["..."])
                    line.append("...")
                    break

                lines.append(" ".join(line))
                line = [word]
            else:
                line.append(word)
        if line:
            lines.append(" ".join(line))

        self.width = self.max_width
        if self.max_width == float('inf'):
            self.width = font.get_rect(lines[0], size = font_size).width
        self.height = font.get_sized_height() * (len(lines) - 1) + font.get_rect(lines[-1]).height
        self.invalidate_pos()


        self.text_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(len(lines)):
            line_width = font.get_rect(lines[i]).width
            line_offset_x = (self.width - line_width) / 2
            font.render_to(self.text_surface, (line_offset_x, i * font.get_sized_height()), lines[i], color)

    def set_disabled(self, disabled):
        super().set_disabled(disabled)
        if disabled:
            self._render_text(mult_color(self.color, 0.6))
        else:
            self._render_text()

    def set_text(self, new_text):
        self.text = new_text
        self._render_text()

    def update_font(self, size = None, bold = None, color = None):
        if size is None: size = self.font_size
        if bold is None: bold = self.bold
        if color is None: color = self.color

        self.bold = bold
        self.font_size = size
        self.color = color

        self._render_text()

    def _create_font(self, size, bold = None):
        if bold is None: bold = self.bold
        font = pygame.freetype.Font(FONT_PATH, size)
        font.strong = bold
        return font

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.text_surface, (x, y))
        self.draw_children(surface)
