import pygame
import pygame.freetype
import shutil
from pathlib import Path
import os
from send2trash import send2trash

from .modal_element import ModalElement
from ..controls import TextButton, ImageButton, TextInput, ScrollBar
from .message import Message
from .file_saver import FileSaver
from ..display import Label
from ..layout import Row
from ...utils import asset_path, FONT_PATH

class FilePicker(ModalElement):
    style_defaults = {"font_color": (200, 200, 200), "icon_color": (200, 200, 200), "bg_color": (70, 70, 70),
                      "action_button_color": (120, 120, 120), "delete_button_color": (95, 25, 25),
                      "search_bg": (50, 50, 50), "search_font_color": (200, 200, 200), "file_selected_bg_color": (90, 90, 90),
                      "file_hover_bg_color": (50, 50, 50)}

    def __init__(self, layer, title, directory, extension, action, file_validation = None, **kwargs):
        super().__init__(layer, (350, 395), **kwargs)

        self.directory = directory
        self.extension = extension
        self.files = {}

        self.filtered_files = {}
        self.selected_file = None

        self.action = action
        self.perform_action = False
        self.file_validation = file_validation

        title = Label(self, title, (0, 25), "new", styling = {"font_size": 25, "bold": True})
        self.register_style_mapping(title, {"color": "font_color"})

        ImageButton(self, asset_path("icons", "cross.png"), (15, 15), (30, 30), "ne", styling = {"color": (120, 120, 120), "image_color": self.style["icon_color"], "image_scale": 0.8}, action = self.close)

        self.file_search = TextInput(self, (0, 70), "new", styling={"font_size": 18, "length": self.width - 30}, placeholder = "Search", type_action = self._render_files)
        self.register_style_mapping(self.file_search, {"font_color": "search_font_color", "color": "search_bg"})

        with Row(self, offset = (15, 15), stick="s", spacing = 10) as bottom_row:
            self.open_track_button = TextButton(bottom_row, "Open", dimensions=(self.width - 130, 40), action = self.open_file)
            self.register_style_mapping(self.open_track_button, {"font_color": "font_color", "color": "action_button_color"})

            self.delete_track_button = ImageButton(bottom_row, asset_path("icons", "bin.png"), dimensions=(40, 40), styling={"image_scale": 0.8}, action = self.delete_file)
            self.register_style_mapping(self.delete_track_button, {"image_color": "icon_color", "color": "delete_button_color"})

            self.rename_track_button = ImageButton(bottom_row, asset_path("icons", "rename.png"), dimensions=(40, 40), styling={"color": (120, 120, 120), "image_scale": 0.8}, action = self.rename_file)
            self.register_style_mapping(self.rename_track_button, {"image_color": "icon_color", "color": "action_button_color"})

        self.font = None
        self.filename_font_size = 18
        self.files_surface = None
        self.selection_surface = None
        self.scroll_bar = ScrollBar(self, self.height - 191, self.height - 191, (30, 121), "ne")
        self._load_files()

        self.on_style_changed()

    def on_style_changed(self):
        super().on_style_changed()
        self._render_files()
        self.font = None

    def get_font(self):
        if self.font is None:
            self.font = self.create_font()
        return self.font

    def _load_files(self):
        self.files = {}

        all_files = os.listdir(self.directory)
        all_files = list(sorted(all_files, key = lambda item: Path(item).stem))
        for i in range(len(all_files)):
            file = all_files[i]
            full_path = os.path.join(self.directory, file)
            is_file = os.path.isfile(full_path)
            has_expected_extension = os.path.splitext(full_path)[1][1:] == self.extension

            is_valid = True
            if self.file_validation is not None:
                is_valid = self.file_validation(full_path)

            if is_file and has_expected_extension and is_valid:
                self.files[i] = Path(full_path)

        self._render_files()

    def _render_files(self):
        self.filtered_files = self.files

        search = self.file_search.get_value()
        if len(search) > 0:
            self.filtered_files = {}
            for index, path in self.files.items():
                if path.stem[:len(search)].lower() == search.lower():
                    self.filtered_files[index] = path

        self.files_surface = pygame.Surface((self.width, len(self.filtered_files) * (self.get_font().get_sized_glyph_height(self.filename_font_size) + 10)), pygame.SRCALPHA)
        self.selection_surface = pygame.Surface((self.width, len(self.filtered_files) * (self.get_font().get_sized_glyph_height(self.filename_font_size) + 10)), pygame.SRCALPHA)

        paths = list(self.filtered_files.values())
        for i in range(len(paths)):
            self.get_font().render_to(self.files_surface, (0, 10 + (i * (self.get_font().get_sized_glyph_height(self.filename_font_size) + 10))), paths[i].stem, self.style["font_color"], size=self.filename_font_size)

        self.scroll_bar.set_section_height(self.files_surface.height)
        self.selected_file = None

    def _get_file_hovered(self):
        x_rel_mouse, y_rel_mouse = self.get_relative_mouse()
        list_top = 121
        if (15 <= x_rel_mouse < 290) and (list_top <= y_rel_mouse < list_top + self.height - 191) and self.hovered:
            row_height = self.get_font().get_sized_glyph_height(self.filename_font_size) + 10
            item_index = (y_rel_mouse - list_top + self.scroll_bar.get_value()) // row_height
            if item_index < len(self.filtered_files):
                return list(self.filtered_files.keys())[item_index]
        return None

    def open_file(self):
        if self.action is not None:
            self.action(self.files[self.selected_file])
            self.close()

    def rename_file(self):
        def rename_action(new_path):
            shutil.move(self.files[self.selected_file], new_path)
            self.files[self.selected_file] = Path(new_path)
            self._render_files()

        FileSaver(self.parent, self.directory, self.extension, rename_action, "Rename",
                  value = self.files[self.selected_file].stem)

    def delete_file(self):
        def delete_action():
            send2trash(self.files[self.selected_file])
            self.files.pop(self.selected_file)
            self.selected_file = None
            self._render_files()

        Message(self.parent, "Delete File?", "The file will be recoverable from trash", ("Cancel", None), ("Delete", delete_action))

    def visible_update(self):
        file_selected = self.selected_file is not None
        self.open_track_button.set_disabled(not file_selected)
        self.rename_track_button.set_disabled(not file_selected)
        self.delete_track_button.set_disabled(not file_selected)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            new_value = self.scroll_bar.get_value() + ((event.y * -1) * 10)
            self.scroll_bar.set_value(new_value)
            return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            item_index = self._get_file_hovered()
            if item_index is not None:
                self.selected_file = item_index
            return True

    def draw(self, surface):
        x, y = self.get_pos()

        pygame.draw.rect(surface, self.style["bg_color"], (x, y, self.width, self.height), 0, 15)

        row_height = self.get_font().get_sized_glyph_height(self.filename_font_size) + 10
        scroll_y = self.scroll_bar.get_value()

        self.selection_surface.fill((0, 0, 0, 0))
        item_index = self._get_file_hovered()

        if item_index is not None:
            pos_index = list(self.filtered_files.keys()).index(item_index)
            pygame.draw.rect(self.selection_surface, self.style["file_selected_bg_color"], (0, (pos_index * row_height), 275, row_height), 0, 15)

        if self.selected_file is not None:
            selected_pos_index = list(self.filtered_files.keys()).index(self.selected_file)
            pygame.draw.rect(self.selection_surface, self.style["file_hover_bg_color"], (0, (selected_pos_index * row_height), 275, row_height), 0,15)

        surface.blit(self.selection_surface, (x + 15, y + 121), area = (0, scroll_y, self.width, self.height - 191))
        surface.blit(self.files_surface, (x + 30, y + 121), area = (0, scroll_y, self.width, self.height - 191))
        self.draw_children(surface)
