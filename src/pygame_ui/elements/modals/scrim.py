import pygame
from ...element import Element

class Scrim(Element):
    def __init__(self, parent, show = True):
        super().__init__(parent, (0, 0), (0, 0), "nesw", show = show)
        self.set_dimensions(*self.parent.get_size())

        self.surface = None
        self.create_surface()

    def get_pos(self):
        #Override method - scrim always draws from 0, 0
        return 0, 0

    def create_surface(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (50, 50, 50, 200), (0, 0, self.width, self.height))

    def on_screen_resize(self):
        self.set_dimensions(*pygame.display.get_surface().get_size())
        self.create_surface()

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))
        self.draw_children(surface)