import pygame
import os
from pygame_ui import *

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
def asset_path(asset_type, file_name):
    return os.path.join(ASSETS_DIR, asset_type, file_name)

# --- PYGAME INIT ---
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE, vsync=1)
clock = pygame.time.Clock()

# --- UI INIT ---
theme = Theme()

ui = UI(screen, theme)
main_layer = Layer(ui)

FileSaver(main_layer, "/Users/raphael/Documents/Code/Projects/pygame-ui/src/pygame_ui/elements", "py", None)

# --- Game Logic ---
running = True
while running:
    screen.fill((15, 15, 15))

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWRESIZED:
            ui.on_resize()

    # Any events not used up by the UI is available to handle after
    available_events = ui.handle_events(events)
    ui.draw()

    try:
        pygame.display.flip()
        clock.tick()
    except KeyboardInterrupt:
        running = False

pygame.quit()
