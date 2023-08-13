import pygame
import os

from os.path import isfile, join, dirname, basename
from typing import List
from PIL import Image
from app.textures import Textures
from app.button import Button, Toggle

SUPPORTED_IMAGE_TYPES = (".JPG", ".jpg", ".png")

EVENT_CONFIRM = pygame.USEREVENT + 1
EVENT_CANCEL = pygame.USEREVENT + 2
EVENT_DIRECTION = pygame.USEREVENT + 3
EVENT_ZOOM_MINUS = pygame.USEREVENT + 4
EVENT_ZOOM_PLUS = pygame.USEREVENT + 5

class MainMenuBar():
    def __init__(self, app) -> None:
        self.app = app
        self.rect = pygame.Rect((0, 0), (self.app.scene.get_rect().width, 32))
        self.button_confirm = Button(self.app.scene, x = 0, y = 0, img=self.app.textures.confirm)
        self.button_confirm.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CONFIRM))
        self.button_cancel = Button(self.app.scene, x = 32, y = 0, img=self.app.textures.cancel)
        self.button_cancel.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CANCEL))
        self.button_direction = Toggle(self.app.scene, x = 64, y = 0, images=[self.app.textures.vertical, self.app.textures.horizontal])
        self.button_direction.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_DIRECTION))
        self.button_zoom_minus = Button(self.app.scene, x = 96, y = 0, img=self.app.textures.zoom_minus)
        self.button_zoom_minus.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_ZOOM_MINUS))
        self.button_zoom_plus = Button(self.app.scene, x = 128, y = 0, img=self.app.textures.zoom_plus)
        self.button_zoom_plus.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_ZOOM_PLUS))

    def update(self):
        self.button_confirm.update()
        self.button_cancel.update()
        self.button_direction.update()
        self.button_zoom_minus.update()
        self.button_zoom_plus.update()

    def draw(self):
        bar_width = self.app.scene.get_rect().width
        self.rect.update(self.rect.topleft, (bar_width, self.rect.height))
        pygame.draw.rect(self.app.scene, (50, 50, 50), self.rect)
        self.button_confirm.draw()
        self.button_cancel.draw()
        self.button_direction.draw()
        self.button_zoom_minus.draw()
        self.button_zoom_plus.draw()



class App:
    def __init__(self, window, textures):
        self.scene = window
        self.textures = textures
        self.clock = pygame.time.Clock()
        self.running = True
        self.events = []

        self.surfaces: List[pygame.Surface] = []
        self.images = []
        self.output_path: str = ""
        self.filename: str = ""
        self.direction_vertical = True
        self.scale = 1

        self.main_menu_bar = MainMenuBar(self)


    def update(self):
        self.main_menu_bar.update()

    def draw(self):
        self.scene.fill((20, 20, 25))
        current_height: int = 32
        current_width: int = 0
        for surf in self.surfaces:
            img = pygame.transform.scale_by(surf, self.scale)
            self.scene.blit(img, (current_width, current_height))
            if self.direction_vertical:
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
            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.0f}")

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
                elif event.key == pygame.K_m:
                    print("DEBUG: scale minus")
                    self.scale /= 2
                elif event.key == pygame.K_p:
                    print("DEBUG: scale plus")
                    self.scale *= 2
            elif event.type == EVENT_CONFIRM:
                    print("DEBUG: Merge Button")
                    self.merge()
                    self.clear_images()
            elif event.type == EVENT_CANCEL:
                    print("DEBUG: Cancel Button")
                    self.clear_images()
            elif event.type == EVENT_DIRECTION:
                    print("DEBUG: Direction Button")
                    self.direction_vertical = not self.direction_vertical
            elif event.type == EVENT_ZOOM_MINUS:
                    print("DEBUG: scale minus")
                    self.scale /= 2
            elif event.type == EVENT_ZOOM_PLUS:
                    print("DEBUG: scale plus")
                    self.scale *= 2


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
        if self.direction_vertical:
            self.merge_vertical()
        else:
            self.merge_horizontal()

    def merge_vertical(self):
        width = max([image.size[0] for image in self.images])
        height = sum([image.size[1] for image in self.images])
        current_height: int = 0
        combined_image = Image.new("RGB", (width, height), color=(255, 255, 255))
        for image in self.images:
            combined_image.paste(image, (0, current_height))
            current_height += image.size[1]
        combined_image.save(join(self.output_path, f"{self.filename}_combined.png"), "PNG")

    def merge_horizontal(self):
        final_width = sum([image.size[0] for image in self.images])
        final_height = max([image.size[1] for image in self.images])
        current_width: int = 0
        combined_image = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))
        for image in self.images:
            combined_image.paste(image, (current_width, 0))
            current_width += image.size[0]
        combined_image.save(join(self.output_path, f"{self.filename}_combined.png"), "PNG")

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
