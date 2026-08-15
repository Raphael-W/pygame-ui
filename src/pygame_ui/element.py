import pygame
import pygame.freetype
from .utils import FONT_PATH
from .node import Node
from .theme import InvalidStylePropertyError

class Element(Node):
    style_defaults = {"cursor": pygame.SYSTEM_CURSOR_ARROW, "font_path": FONT_PATH, "font_name": None}

    def __init__(self, parent, offset, dimensions, stick, *, hover_hint = None, show=True, disabled=False, styling=None, tag=None, child_index=-1, transparent=False):
        super().__init__(parent)
        self.offset_x, self.offset_y = offset
        self._width, self._height = dimensions

        self._x = None
        self._y = None

        self._parts = {}

        self.stick = {s: s.lower() in stick for s in "nesw"}

        self.transparent = transparent #Used to determine whether events should be swallowed

        self._hover_hint_text = hover_hint

        self.show = show
        self.disabled = disabled
        self.selected = False
        self.hovered = False
        self._held_down = False

        self.styling = styling or {}
        self.subtree_theme = {}
        self._style = None

        if tag is None:
            self.style_tags = ()
        elif isinstance(tag, str):
            self.style_tags = (tag,)
        else:
            self.style_tags = tuple(tag)

        parent.add_child(self, child_index)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._held_down = True
            self.on_press()
            return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._held_down:
                self.on_click()
            self._held_down = False
            self.on_release()
            return True

    def on_click(self):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass

    def is_held_down(self):
        return self._held_down

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

    def get_hover_hint(self):
        return self._hover_hint_text

    # Gets run only if element is showing
    def visible_update(self):
        pass

    # Gets run only regardless of whether element is visible or not
    def update(self):
        pass

    def draw(self, surface):
        self.draw_children(surface)

    def remove_child(self, child):
        super().remove_child(child)
        self._parts.pop(child, None)

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
        return self._width, self._height

    @property
    def width(self):
        return self.get_size()[0]

    @width.setter
    def width(self, new_width):
        self.set_dimensions(new_width, self.height)

    @property
    def height(self):
        return self.get_size()[1]

    @height.setter
    def height(self, new_height):
        self.set_dimensions(self.width, new_height)

    def get_cursor(self):
        return self.style["cursor"]

    def set_dimensions(self, new_width, new_height):
        self._width = new_width
        self._height = new_height
        self.invalidate_pos()

    def remove(self):
        self.parent.remove_child(self)

    def update_styling_property(self, prop, new_value):
        self.styling.update({prop: new_value})
        self.trigger_on_style_changed()

    def update_styling(self, rules):
        self.styling.update(rules)
        self.trigger_on_style_changed()

    def invalidate_styling(self):
        self._style = None
        for child in self.get_children():
            child.invalidate_styling()

    def trigger_on_style_changed(self):
        self.invalidate_styling()
        self.on_style_changed()
        for child in self.get_children():
            child.trigger_on_style_changed()

    def on_style_changed(self):
        for child, mapping in self._parts.items():
            self._forward_part_styles(child, mapping)

    def register_style_mapping(self, child, mapping):
        self._parts.setdefault(child, {}).update(mapping)
        self._forward_part_styles(child, mapping)

    def _forward_part_styles(self, child, mapping):
        child.update_styling({child_key: self.style[own_key] for child_key, own_key in mapping.items()})

    @classmethod
    def class_defaults(cls):
        if "_defaults_cache" not in cls.__dict__:  # per-class, not inherited
            merged = {}
            for klass in reversed(cls.__mro__):
                merged.update(klass.__dict__.get("style_defaults", {}))
            cls._defaults_cache = merged
        return cls._defaults_cache

    def get_theme(self):
        theme = self.parent.get_theme()  # UI returns self.theme at the root
        return theme.extended(self.subtree_theme)

    def create_font(self):
        if font_name := self.style.get("font_name"):
            font = pygame.freetype.SysFont(font_name, 0)
        elif font_path := self.style.get("font_path"):
            try:
                font = pygame.freetype.Font(font_path)
            except:
                font = pygame.freetype.SysFont("", 0)
        else:
            font = pygame.freetype.SysFont("", 0)
        return font


    @property
    def style(self):
        if self._style is None:
            resolved = dict(self.class_defaults())
            resolved.update(self.get_theme().resolve(self))
            for prop in self.styling or {}:
                if prop not in resolved:
                    raise InvalidStylePropertyError(prop, set(resolved))
            resolved.update(self.styling or {})
            self._style = resolved
        return self._style

    def update_subtree_theme(self, rules, cls = None):
        if cls is None:
            cls = Element
        self.subtree_theme.update({cls: rules})
        self.trigger_on_style_changed()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
