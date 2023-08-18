import pygame
from typing import Callable, List

class Wydget():

    COLOR_FILL = (100, 100, 100)
    COLOR_STROKE = (180, 180, 180)
    RADIUS = 7
    STROKE_WIDTH = 1

    def __init__(self, scene, x: float, y: float, w: float, h: float) -> None:
        self._scene: pygame.Surface = scene
        self.rect = pygame.Rect((x, y), (w, h))
        self._hidden: bool = False
        self._active: bool = True
        self._pressed: bool = False
        self._hovered: bool = False
        self._scale: int = 1
        # Event callbacks
        self.on_click: Callable | None = None
        self.on_click_params = []
        self.on_release: Callable | None = None
        self.on_release_params = []
        self.on_entry: Callable | None = None
        self.on_entry_params = []
        self.on_leave: Callable | None = None
        self.on_leave_params = []

    def update(self):
        if not self._active:
            return
        left_click_pressed = pygame.mouse.get_pressed()[0]
        x, y = pygame.mouse.get_pos()
        if self.contains(x, y):
            if not self._hovered:
                self._hovered = True
                self.handle_on_entry()
            if left_click_pressed and not self._pressed:
                self._pressed = True
                self.handle_on_click()
            elif not left_click_pressed and self._pressed:
                self._pressed = False
                self.handle_on_release()
        elif self._hovered:
            self._hovered = False
            self._pressed = False
            # if not left_click_pressed:
            self.handle_on_leave()
            # evtl needs else release hgere

    def draw(self):
        if self._hidden:
            return

        if self._hovered:
            pygame.draw.rect(self._scene, self.COLOR_FILL, self.rect, border_radius=self.RADIUS)

    def handle_on_click(self):
        print("click")
        if self.on_click:
            self.on_click(*self.on_click_params)

    def handle_on_release(self):
        print("release")
        if self.on_release:
            self.on_release(*self.on_release_params)

    def handle_on_entry(self):
        print("entry")
        if self.on_entry:
            self.on_entry(*self.on_entry_params)

    def handle_on_leave(self):
        print("leave")
        if self.on_leave:
            self.on_leave(*self.on_leave_params)

    def contains(self, x, y):
        """# to compensate for a wrong mouse position when scaling the scene up"""
        x_scaled = x // self._scale
        y_scaled = y // self._scale
        return self.rect.collidepoint(x_scaled, y_scaled)


class Button(Wydget):
    def __init__(self, scene, x: float, y: float, w: float = 10, h: float = 10, img = None):
        super().__init__(scene, x, y, w, h)
        self._img = img
        self.rect = pygame.Rect((x, y), (w, h))
        if self._img is not None:
            self.rect = pygame.Rect((x, y), self._img.get_rect().size)

    def draw(self):
        if self._hidden:
            return
        super().draw()
        if self._img is not None:
            self._scene.blit(self._img, self.rect)
            # if self.COLOR_STROKE:
            #     pygame.draw.rect(
            #         self._scene,
            #         self.COLOR_STROKE,
            #         self.rect,
            #         border_radius=self.RADIUS,
            #         width=self.STROKE_WIDTH,
            #     )

class Toggle(Wydget):
    def __init__(self, scene, x: float, y: float, images):
        super().__init__(scene, x, y, 10, 10)
        self._images = images
        self.rect = pygame.Rect((x, y), self._images[0].get_rect().size)
        self._range: int = len(self._images)
        self.index: int = 0

    def draw(self):
        if self._hidden:
            return
        super().draw()
        self._scene.blit(self._images[self.index], self.rect)

    def handle_on_click(self):
        super().handle_on_click()
        self.index += 1
        if self.index >= self._range:
            self.index = 0


class DropDown(Wydget):
    def __init__(self, scene, x: float, y: float, images: List[pygame.Surface]) -> None:
        super().__init__(scene, x, y, 10, 10)
        self._images: List[pygame.Surface] = images
        self.rect = pygame.Rect((x, y), self._images[0].get_rect().size)
        self._range: int = len(self._images)
        self.index: int = 0
        self._element_height: int = self.rect.height
        self.open: bool = False
        self.buttons: List[Button] = []
        for i in range(len(self._images)):
            btn = Button(scene, x, y + self._element_height + i * self._element_height, img=self._images[i])
            btn.on_click = self.select_index
            btn.on_click_params = [i]
            self.buttons.append(btn)

    def update(self):
        if not self._active:
            return
        super().update()
        if self.open:
            for btn in self.buttons:
                btn.update()

    def draw(self):
        if self._hidden:
            return
        super().draw()
        self._scene.blit(self._images[self.index], self.rect)
        if self.open:
            for btn in self.buttons:
                btn.draw()

    def handle_on_click(self):
        super().handle_on_click()
        self.open = not self.open

    def select_index(self, index: int):
        self.index = index
        self.open = False
