import pygame

from app.button import Button, Toggle
from app.events import EVENT_CONFIRM, EVENT_CANCEL, EVENT_DIRECTION, EVENT_ZOOM_MINUS, EVENT_ZOOM_PLUS


class MainMenuBar():
    def __init__(self, app) -> None:
        self.app = app
        self.rect = pygame.Rect((0, 0), (self.app.scene.get_rect().width, 32))
        self.button_confirm = Button(self.app.scene, x = 0, y = 0, img=self.app.textures.confirm)
        self.button_confirm.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CONFIRM))
        self.button_cancel = Button(self.app.scene, x = 32+4, y = 0, img=self.app.textures.cancel)
        self.button_cancel.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_CANCEL))
        self.button_direction = Toggle(self.app.scene, x = 2*(32+4), y = 0, images=[self.app.textures.vertical, self.app.textures.horizontal])
        self.button_direction.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_DIRECTION))
        self.button_zoom_minus = Button(self.app.scene, x = 3*(32+4), y = 0, img=self.app.textures.zoom_minus)
        self.button_zoom_minus.on_click = lambda: pygame.event.post(pygame.event.Event(EVENT_ZOOM_MINUS))
        self.button_zoom_plus = Button(self.app.scene, x = 4*(32+4), y = 0, img=self.app.textures.zoom_plus)
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

