import json
from doctest import register_optionflag

class StyleError(Exception):
    """Base class for style-related errors."""


class InvalidStylePropertyError(StyleError, AttributeError):
    """Raised when a style property name doesn't exist."""

    def __init__(self, prop: str, valid_props: set[str] | None = None):
        self.prop = prop
        self.valid_props = valid_props
        msg = f"Invalid style property: {prop!r}"
        if valid_props:
            msg += f". Valid properties: {sorted(valid_props)}"
        super().__init__(msg)


class InvalidStyleValueError(StyleError, ValueError):
    """Raised when a style property has an invalid value."""

    def __init__(self, prop: str, value, reason: str = ""):
        self.prop = prop
        self.value = value
        msg = f"Invalid value for {prop!r}: {value!r}"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)

class Theme:
    def __init__(self, rules = None, parent = None):
        self.rules = rules or {}  # {ElementClass: {prop: value}}
        self.parent = parent

    def extended(self, rules):
        return Theme(rules, parent = self) if rules else self

    def resolve(self, element):
        resolved = dict(element.class_defaults())
        if self.parent is not None:
            resolved.update(self.parent.resolve(element))
        for cls in reversed(type(element).__mro__):
            for rule in self.rules.get(cls, {}):
                if rule not in resolved:
                    raise InvalidStylePropertyError(rule, set(resolved))

            resolved.update(self.rules.get(cls, {}))
        for tag in element.style_tags:
            for rule in self.rules.get(tag, {}):
                if rule not in resolved:
                    raise InvalidStylePropertyError(rule, set(resolved))
            resolved.update(self.rules.get(tag, {}))
        return resolved
