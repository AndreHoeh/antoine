import pygame

from dataclasses import dataclass
from typing import Dict

from app.button import Button, Toggle, DropDown
from app.events import EVENT_CONFIRM, EVENT_CANCEL

@dataclass
class MainMenuData:
    direction_vertical: bool = True
    render_scale: float = 1.0

file_type_mapper: Dict[int, str] = {
    0: "PNG",
    1: "JPEG"
}


class MainMenuBar:
    def __init__(self, app) -> None:
        self.app = app
        self.rect = pygame.Rect((0, 0), (self.app.scene.get_rect().width, 32))
        self.button_confirm = Button(self.app.scene, x=0, y=0, img=self.app.textures.confirm)
        self.button_confirm.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CONFIRM))
        self.button_cancel = Button(self.app.scene, x=32 + 4, y=0, img=self.app.textures.cancel)
        self.button_cancel.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CANCEL))
        self.button_direction = Toggle(self.app.scene, x=2 * (32 + 4), y=0, images=[self.app.textures.vertical, self.app.textures.horizontal])
        self.button_direction.on_click = self.callback_direction_toggle
        self.button_zoom_minus = Button(self.app.scene, x=3 * (32 + 4), y=0, img=self.app.textures.zoom_minus)
        self.button_zoom_minus.on_click = self.callback_zoom_minus
        self.button_zoom_plus = Button(self.app.scene, x=4 * (32 + 4), y=0, img=self.app.textures.zoom_plus)
        self.button_zoom_plus.on_click = self.callback_zoom_plus
        self.button_filetype = DropDown(self.app.scene, x=5 * (32 + 4), y=0, images=[self.app.textures.filetype_png, self.app.textures.filetype_jpg])
        # self.dropdown = DropDown(
        #     self.app.scene,
        #     x=6 * (32 + 4),
        #     y=0,
        #     images=[
        #         self.app.textures.alpha,
        #         self.app.textures.beta,
        #         self.app.textures.gamma,
        #         self.app.textures.delta,
        #     ],
        # )
        # self.dropdown.on_click = self.callback_filetype_toggle

        self.data = MainMenuData()

    def update(self):
        self.button_confirm.update()
        self.button_cancel.update()
        self.button_direction.update()
        self.button_zoom_minus.update()
        self.button_zoom_plus.update()
        self.button_filetype.update()
        # self.dropdown.update()

    def draw(self):
        bar_width = self.app.scene.get_rect().width
        self.rect.update(self.rect.topleft, (bar_width, self.rect.height))
        pygame.draw.rect(self.app.scene, (40, 40, 45), self.rect)
        self.button_confirm.draw()
        self.button_cancel.draw()
        self.button_direction.draw()
        self.button_zoom_minus.draw()
        self.button_zoom_plus.draw()
        self.button_filetype.draw()
        # self.dropdown.draw()

    def callback_direction_toggle(self):
        self.data.direction_vertical = not self.data.direction_vertical

    def callback_zoom_minus(self):
        self.data.render_scale /= 2

    def callback_zoom_plus(self):
        self.data.render_scale *= 2

    def get_filetype_value(self) -> str:
        return file_type_mapper[self.button_filetype.index]

