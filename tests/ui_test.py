import pygame
import os
from pygame_ui import *

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
def asset_path(asset_type, file_name):
    return os.path.join(ASSETS_DIR, asset_type, file_name)

# --- PYGAME INIT ---
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE, vsync=1)
clock = pygame.time.Clock()

# --- UI INIT ---
ui = UI(screen)
main_layer = Layer(ui)

Label(main_layer, "This is a label", (30, 50), "nw", font_size = 15, color = (200, 200, 200))
TextButton(main_layer, "This is a button", (200, 30), (200, 50), "nw")
#ImageButton(main_layer, asset_path("icons", "aim.png"), (450, 30), (50, 50), "nw", image_color = (200, 200, 200), disabled = False)
#Slider(main_layer, (0, 100), (550, 50), (150, 10), "nw", bar_color = (180, 180, 180), handle_color = (36, 155, 199), suffix = "%", increment = 2),
Switch(main_layer, (800, 50), 1, "nw")
TextInput(main_layer, (900, 50), "nw", length = 200, font_size = 20, placeholder = "Search")
#Image(main_layer, asset_path("img", "silverstoneExample.jpg"), (30, 120), "nw", scale=0.1)
TextButton(main_layer, "Show message", (450, 200), (200, 50), "nw", action = lambda: Message(main_layer, "Message Test", "This is a message box", ("Okay", None)))
TextButton(main_layer, "Show prompt", (700, 200), (200, 50), "nw", action = lambda: Message(main_layer, "Prompt Test", "This is a prompt message box", ("No", None), ("Yes", None)))
TextButton(main_layer, "Show label modal", (450, 275), (200, 50), "nw", action = lambda: LabelModal(main_layer, "Yh, you may need to restart the game - I haven't quite worked out to automatically close this", max_width = 400))
Dropdown(main_layer, ["Option 1", "Option 2", "Option 3"], (950, 210), "nw")
Accordion(main_layer, "Goodwood Circuit", stick = "se")
TextButton(main_layer, "Save File", (700, 275), (200, 50), "nw", action = lambda: FileSaver(main_layer,
                                                                                            ROOT_PATH + "/tracks",
                                                                                            file_extension = "track",
                                                                                            action = lambda x: print(
                                                                                                f"Saved in {x}"),
                                                                                            placeholder = "Track name"))

KeyIcon(main_layer, pygame.K_w, (1150, 25), 1, "nw")
KeyIcon(main_layer, pygame.K_a, (1115, 60), 1, "nw")
KeyIcon(main_layer, pygame.K_s, (1150, 60), 1, "nw")
KeyIcon(main_layer, pygame.K_d, (1185, 60), 1, "nw")

#FilePicker(main_layer, "Tracks", ROOT_PATH + "/tracks", "track", None, None)
ScrollBar(main_layer, (0, 0), 200, 1000, "nesw")

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
