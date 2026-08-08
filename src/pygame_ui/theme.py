import json

class Theme:
    def __init__(self, rules = None, parent = None):
        self.rules = rules or {}  # {ElementClass: {prop: value}}
        self.parent = parent

    def extended(self, rules):
        return Theme(rules, parent = self) if rules else self

    def resolve(self, element):
        resolved = {}
        if self.parent is not None:
            resolved.update(self.parent.resolve(element))
        for cls in reversed(type(element).__mro__):
            resolved.update(self.rules.get(cls, {}))
        return resolved
