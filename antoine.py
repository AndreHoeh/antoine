import pygame
import os

from os.path import isfile, dirname, basename
from typing import List
from PIL import Image

from app.textures import Textures
from app.main_menue_bar import MainMenuBar
from app.export import merge_vertical, merge_horizontal
from app.events import EVENT_CONFIRM, EVENT_CANCEL

SUPPORTED_IMAGE_TYPES = (".JPG", ".jpg", ".png")
APPLICATION_NAME = "Antoine"


class App:
    def __init__(self, window, textures: Textures):
        self.scene = window
        self.textures: Textures = textures
        self.clock = pygame.time.Clock()
        self.running = True
        self.events = []

        self.surfaces: List[pygame.Surface] = []
        self.images = []
        self.output_path: str = ""
        self.filename: str = ""

        self.main_menu_bar = MainMenuBar(self)

    def update(self):
        self.main_menu_bar.update()

    def draw(self):
        self.scene.fill((20, 20, 25))
        current_height: int = 32
        current_width: int = 0
        for surf in self.surfaces:
            img = pygame.transform.scale_by(surf, self.main_menu_bar.data.render_scale)
            self.scene.blit(img, (current_width, current_height))
            if self.main_menu_bar.data.direction_vertical:
                current_height += img.get_height()
            else:
                current_width += img.get_width()
        self.main_menu_bar.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.events = pygame.event.get()
            self.handle_basic_events()
            self.update()
            self.draw()
            self.clock.tick(30)
            pygame.display.set_caption(f"{APPLICATION_NAME} | FPS: {self.clock.get_fps():.0f}")

    def handle_basic_events(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.DROPFILE:
                self.handle_drop_file_path(event.file)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.clear_images()
                elif event.key == pygame.K_RETURN:
                    print("DEBUG: Key Press Return")
                    self.merge()
                    self.clear_images()
            elif event.type == EVENT_CONFIRM:
                print("DEBUG: Merge Button")
                self.merge()
                self.clear_images()
            elif event.type == EVENT_CANCEL:
                print("DEBUG: Cancel Button")
                self.clear_images()


    def handle_drop_file_path(self, path: str):
        if not self.is_valid_source(path):
            return
        self.add_img(path)
        self.output_path = self.output_path if self.output_path else dirname(path)  # first element will set outputpath
        # first element will set filename and strip file type
        self.filename = self.filename if self.filename else basename(path).split(".")[0]

    def is_valid_source(self, path: str) -> bool:
        if not isfile(path):
            print("ERROR: Please provide a file, not a directory!")
            return False
        if not path.endswith(SUPPORTED_IMAGE_TYPES):
            print(f"ERROR: This tool only supports {SUPPORTED_IMAGE_TYPES}")
            return False
        return True

    def add_img(self, path: str):
        print("Import:", path)
        img = Image.open(path)
        self.images.append(img)
        self.surfaces.append(self.img_to_surface(img))

    def img_to_surface(self, img) -> pygame.Surface:
        mode = img.mode
        size = img.size
        data = img.tobytes()
        return pygame.image.fromstring(data, size, mode)

    def merge(self):
        if len(self.images) < 2:  # nothing to merge
            return
        if self.main_menu_bar.data.direction_vertical:
            merge_vertical(self.images, self.output_path, self.filename, self.main_menu_bar.data.export_type)
        else:
            merge_horizontal(self.images, self.output_path, self.filename, self.main_menu_bar.data.export_type)

    def clear_images(self):
        print("DEBUG: Clear images")
        self.images.clear()
        self.surfaces.clear()
        self.output_path = ""
        self.filename = ""


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"  # center window
    os.environ["pg_BLEND_ALPHA_SDL2 "] = "1"  # faster blitting when using SDL2
    window = pygame.display.set_mode((550, 950), pygame.RESIZABLE)
    Textures.setup(path)
    textures = Textures.get_shared()
    pygame.display.set_icon(textures.logo)

    app = App(window, textures)
    app.run()
