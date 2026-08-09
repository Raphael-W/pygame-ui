import pygame
import pygame.freetype
from ...element import Element
from ...utils import FONT_PATH, mult_color

class Label(Element):
    style_defaults = {"font_size": 15, "min_font_size": None, "max_width": -1, "wrap_mode": "wrap", "color": (200, 200, 200), "bold": False}

    def __init__(self, parent, text, offset = (0, 0), stick = "", *, show = True, styling = None, child_index = -1):
        super().__init__(parent, offset, (0, 0), stick, show = show, child_index = child_index, styling = styling, transparent = True)

        self.text = text
        self.text_surface = None

        self._render_text()


    def _render_text(self, color = None):
        if color is None:
            color = self.style["color"]

        split_text = self.text.split(' ')
        font_size = self.style["font_size"]
        min_font_size = self.style["min_font_size"] or font_size
        max_width = float('inf') if self.style["max_width"] < 0 else self.style["max_width"]
        font = self._create_font(font_size)

        line = []
        lines = []
        for word in split_text:
            potential_line = " ".join(line + [word])
            while (font.get_rect(potential_line).width > max_width) and font_size > min_font_size:
                font_size -= 1
                font = self._create_font(font_size)

            if font.get_rect(potential_line).width > max_width:
                if self.style["wrap_mode"] == "ellipse":
                    potential_line = " ".join(line + ["..."])
                    while font.get_rect(potential_line).width > max_width:
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

        self.width = max_width
        if max_width == float('inf'):
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
            self._render_text(mult_color(self.style["color"], 0.6))
        else:
            self._render_text()

    def set_text(self, new_text):
        self.text = new_text
        self._render_text()

    def _create_font(self, size, bold = None):
        if bold is None: bold = self.style["bold"]
        font = pygame.freetype.Font(self.style["font_path"], size)
        font.strong = bold
        return font

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.text_surface, (x, y))
        self.draw_children(surface)
