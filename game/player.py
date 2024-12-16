# game/player.py
import pygame
from game.config import GREEN

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Tamaño del jugador
        self.color = GREEN
        self.speed = 5

    def handle_input(self, walls=None):
        """Mueve al jugador y verifica las colisiones con las paredes."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # Movimiento tentativo
        self.rect.x += dx
        self.rect.y += dy

        # Verificar colisiones con paredes
        if walls:
            for row in walls:
                for wall in row:
                    if self.rect.colliderect(wall):
                        # Deshacer movimiento
                        self.rect.x -= dx
                        self.rect.y -= dy
                        return

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
