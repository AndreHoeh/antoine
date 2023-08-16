import pygame


class Textures:
    """
    Class to load and manage Textures. Most of the images get flipped and copied
    to keep the number of textures minimal.
    Images also get dynamically colored via color blending.
    """

    shared = None

    def __init__(self, path: str):
        self.path = path + "/app/assets"

    def load(self):
        self.logo = pygame.image.load(f"{self.path}/logo.png").convert_alpha()
        self.confirm = pygame.image.load(f"{self.path}/confirm_32x32.png").convert_alpha()
        self.confirm.fill((50, 200, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.cancel = pygame.image.load(f"{self.path}/cancel_32x32.png").convert_alpha()
        self.cancel.fill((200, 50, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.vertical = pygame.image.load(f"{self.path}/vertical_32x32.png").convert_alpha()
        self.vertical.fill((180, 180, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.horizontal = pygame.image.load(f"{self.path}/horizontal_32x32.png").convert_alpha()
        self.horizontal.fill((180, 180, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.zoom_minus = pygame.image.load(f"{self.path}/zoom_minus.png").convert_alpha()
        self.zoom_minus.fill((200, 100, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.zoom_plus = pygame.image.load(f"{self.path}/zoom_plus.png").convert_alpha()
        self.zoom_plus.fill((200, 100, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.filetype_jpg = pygame.image.load(f"{self.path}/filetype_jpg.png").convert_alpha()
        self.filetype_jpg.fill((180, 180, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.filetype_png = pygame.image.load(f"{self.path}/filetype_png.png").convert_alpha()
        self.filetype_png.fill((180, 180, 180, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # self.player_idle_frames = [
        #     pygame.image.load(f"{self.path}/player/idle/1.png").convert_alpha(),
        #     pygame.image.load(f"{self.path}/player/idle/2.png").convert_alpha(),
        #     pygame.image.load(f"{self.path}/player/idle/3.png").convert_alpha(),
        #     pygame.image.load(f"{self.path}/player/idle/4.png").convert_alpha(),
        # ]

        # self.player_idle_flipped = pygame.transform.flip(self.player_idle, True, False)
        # self.player_idle_copy = self.player_idle.copy()
        # self.player_idle_copy.fill((255, 30, 30, 0), special_flags=pygame.BLEND_RGBA_ADD)

    @classmethod
    def setup(cls, path) -> None:
        """
        Setup textures and start loading images
        """
        cls.shared = Textures(path)
        cls.shared.load()

    @classmethod
    def get_shared(cls) -> "Textures":
        """
        Returns the shared textures instance
        """
        return cls.shared