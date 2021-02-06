from collections import defaultdict

import pygame

from src.camera import Camera
from src.game_component import GameComponent


class GridComponent(GameComponent):
    def init(self):
        self.width = 1
        self.default_color: pygame.Color = pygame.Color('white')
        self.colors = defaultdict(lambda: self.default_color)

    def set_color(self, row: int, column: int, color: pygame.Color):
        self.colors[row, column] = color

    def reset_color(self, row: int, column: int):
        del self.colors[row, column]

    def reset_all(self):
        self.colors.clear()

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        pygame.draw.rect(surface, self.colors[row, column], cell_rect, self.width)
