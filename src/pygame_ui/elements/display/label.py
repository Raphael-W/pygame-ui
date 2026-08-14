import pygame
import pygame.freetype
from ...element import Element
from ...utils import FONT_PATH, mult_color

class Label(Element):
    style_defaults = {"font_size": 15, "min_font_size": None, "max_width": -1, "wrap_mode": "wrap", "color": (200, 200, 200), "bold": False}

    def __init__(self, parent, text, offset = (0, 0), stick = "", transparent=True, **kwargs):
        super().__init__(parent, offset, (0, 0), stick, transparent=transparent, **kwargs)

        self.text = text
        self.text_surface = None
        self.font = None

        self._render_text()

    def _render_text(self):
        color = self.style["color"]
        if self.disabled:
            color = mult_color(color, 0.6)

        font_size = self.style["font_size"]
        min_font_size = self.style["min_font_size"] or font_size
        max_width = float('inf') if self.style["max_width"] < 0 else self.style["max_width"]
        wrap_mode = self.style["wrap_mode"]
        font = self.get_font()
        font.strong = self.style["bold"]

        def width(text):
            return font.get_rect(text, size=font_size).width

        def shrink_to_fit(text):
            nonlocal font_size
            while width(text) > max_width and font_size > min_font_size:
                font_size -= 1

        def ellipsize(words):
            words = list(words)
            candidate = words + ["..."]
            while width(" ".join(candidate)) > max_width and len(words) > 1:
                words.pop()
                candidate = words + ["..."]
            return candidate

        lines = []
        line = []
        for word in self.text.split(" "):
            candidate = line + [word]
            shrink_to_fit(" ".join(candidate))

            if width(" ".join(candidate)) <= max_width or not line:
                line = candidate
                continue

            if wrap_mode == "ellipse":
                lines.append(" ".join(ellipsize(line)))
                line = []
                break

            lines.append(" ".join(line))
            line = [word]

        if line:
            lines.append(" ".join(ellipsize(line) if wrap_mode == "ellipse" else line))

        longest_line = max([width(l) for l in lines] + [0])
        if len(lines) > 1:
            longest_line = max_width
        self.width = min(longest_line, max_width)

        self.height = font.get_sized_height(font_size) * (len(lines) - 1) + font.get_rect(lines[-1], size=font_size).height
        self.invalidate_pos()

        self.text_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i, l in enumerate(lines):
            line_offset_x = (self.width - width(l)) / 2
            font.render_to(self.text_surface, (line_offset_x, i * font.get_sized_height(font_size)), l, color, size = font_size)

    def set_disabled(self, disabled):
        super().set_disabled(disabled)
        self._render_text()

    def set_text(self, new_text):
        self.text = new_text
        self._render_text()

    def get_font(self) -> pygame.freetype.Font:
        if self.font is None:
            self.font = self.create_font()
        return self.font

    def on_style_changed(self):
        self.font = None
        self._render_text()

    def draw(self, surface):
        x, y = self.get_pos()
        surface.blit(self.text_surface, (x, y))
        self.draw_children(surface)
