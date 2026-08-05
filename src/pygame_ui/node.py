import pygame

class Node:
    def __init__(self, parent = None):
        self.parent = parent
        self.children = []

    def add_child(self, child, index = -1):
        if index < 0:
            index = len(self.children)

        self.children.insert(index, child)

    def remove_child(self, child):
        grandchildren = child.get_children(only_visible = False, only_enabled = False)
        for grandchild in grandchildren:
            child.remove_child(grandchild)
        self.children.remove(child)

    def bring_child_to_front(self, child):
        if child in self.children:
            self.children.remove(child)
            self.children.append(child)

    def get_children(self, only_visible = False, only_enabled = False, instance = None):
        elements = self.children
        if instance is not None:
            elements = list(filter(lambda e: isinstance(e, instance), elements))
        if only_visible:
            elements = list(filter(lambda e: e.show, elements))
        if only_enabled:
            elements = list(filter(lambda e: not e.disabled, elements))
        return elements

    def leaf_under_mouse(self, only_visible = True, only_enabled = False):
        for child in reversed(self.get_children(only_visible, only_enabled)):
            if not child.under_mouse():
                continue
            inner = child.leaf_under_mouse(only_visible, only_enabled)
            if inner is not None:
                return inner
            if not child.transparent:
                return child
        return None

    def draw_children(self, surface):
        for element in self.get_children():
            element.update()

            if element.show:
                if not element.disabled:
                    element.visible_update()
                element.draw(surface)

    def get_ancestors(self):
        ancestors = [self]
        while ancestors[-1].parent is not None:
            ancestors.append(ancestors[-1].parent)
        return ancestors

    def get_descendants(self, only_visible = True, only_enabled = False):
        descendants = []
        for child in self.get_children(only_visible, only_enabled):
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_root(self):
        return self.get_ancestors()[-1]

    def print_tree(self, prefix = "", is_last = True, is_root = True):
        if is_root:
            print(type(self).__name__)
        else:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + type(self).__name__)

        for i, child in enumerate(self.children):
            if is_root:
                extension = ""
            else:
                extension = "    " if is_last else "│   "
            child.print_tree(prefix + extension, i == len(self.children) - 1, is_root=False)