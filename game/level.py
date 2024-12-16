# game/level.py
import pygame
from game.config import WHITE, BLACK, RED

class Level:
    def __init__(self, level_file, screen):
        self.screen = screen
        self.tiles = []
        self.goal = None  # Coordenadas de la meta
        self.load_level(level_file)

    def load_level(self, level_file):
        """Carga el nivel desde un archivo de texto."""
        with open(level_file, "r") as file:
            for y, line in enumerate(file):
                row = []
                for x, char in enumerate(line.strip()):
                    if char == "1":  # Pared
                        row.append(pygame.Rect(x * 40, y * 40, 40, 40))
                    elif char == "E":  # Meta
                        self.goal = pygame.Rect(x * 40, y * 40, 40, 40)
                self.tiles.append(row)

    def update(self):
        """Actualiza la lógica del nivel."""
        pass

    def render(self):
        """Renderiza el nivel en la pantalla."""
        self.screen.fill(BLACK)
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(self.screen, WHITE, tile)
        if self.goal:
            pygame.draw.rect(self.screen, RED, self.goal)  # Renderiza la meta
