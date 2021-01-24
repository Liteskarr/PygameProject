import pygame

from src.game import Game
from src.camera import Camera


class MapDrawer:
    def __init__(self, game: Game, camera: Camera, cell_size: int = 40):
        self._game = game
        self._world_map = game.get_map()
        self._camera = camera
        self._cell_size = cell_size

    def render_at(self, surface: pygame):
        width, height = self._world_map.get_size()
        cx, cy, cw, ch = self._camera.get_rect()
        cell_size = int(self._cell_size * self._camera.get_zoom_factor())
        for y in range(height):
            for x in range(width):
                rect = (x * cell_size, y * cell_size, cell_size, cell_size)
                if self._camera.intersect_with_rect(rect):
                    new_rect = list(rect)
                    new_rect[0] -= cx
                    new_rect[1] -= cy
                    pygame.draw.rect(surface, pygame.Color('white'), new_rect, 1)
