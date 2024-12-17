import pygame
import os
import random
from game.utils import resource_path

class Enemy:
    def __init__(self, x, y, speed=2):
        """
        Inicializa al enemigo.
        
        Args:
            x (int): Posición inicial en X.
            y (int): Posición inicial en Y.
            speed (int): Velocidad del enemigo.
        """
        # Cargar los cuadros del GIF
        self.frames = self.load_frames(resource_path("assets/images/enemy_frames"), (120, 120))
        self.current_frame = 0
        self.animation_speed = 100  # Milisegundos entre cuadros
        self.last_update = pygame.time.get_ticks()

        # Rectángulo del enemigo
        self.rect = pygame.Rect(x, y, 120, 120)  # Tamaño inicial igual a los frames (120x120)
        self.speed = speed  # Velocidad del enemigo
        self.direction = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]  # Dirección inicial aleatoria

        # Margen personalizado para el colisionador
        self.collider_margin = {"left": 20, "right": 20, "top": 20, "bottom": 20}  # Márgenes ajustables

        # Cargar el sonido de cambio de dirección
        self.change_direction_sound = pygame.mixer.Sound(resource_path("assets/sounds/flying.wav"))
        self.change_direction_sound.set_volume(0.5)  # Ajustar el volumen (opcional)

    def load_frames(self, folder, size):
        """Carga los cuadros del GIF desde una carpeta."""
        frames = []
        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                frame = pygame.image.load(os.path.join(folder, file))
                frame = pygame.transform.scale(frame, size)  # Ajustar el tamaño de los cuadros
                frames.append(frame)
        return frames

    def animate(self):
        """Actualiza el cuadro actual para la animación."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def move(self):
        """Mueve al enemigo en una dirección aleatoria."""
        previous_direction = self.direction.copy()

        # Cambiar dirección aleatoriamente
        if random.randint(0, 50) == 0:
            self.direction = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
            if self.direction != previous_direction:
                self.change_direction_sound.play()

        # Actualizar posición
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Mantener al enemigo dentro de los límites de la pantalla
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction[0] *= -1
            self.change_direction_sound.play()
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.direction[0] *= -1
            self.change_direction_sound.play()
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction[1] *= -1
            self.change_direction_sound.play()
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.direction[1] *= -1
            self.change_direction_sound.play()

    def get_collider_rect(self):
        """
        Devuelve un rectángulo ajustado para colisiones.
        Igual a la lógica usada en player.py.
        """
        margin = self.collider_margin
        return pygame.Rect(
            self.rect.x + margin["left"],
            self.rect.y + margin["top"],
            self.rect.width - margin["left"] - margin["right"],
            self.rect.height - margin["top"] - margin["bottom"]
        )

    def render(self, screen):
        """Renderiza al enemigo en la pantalla."""
        self.animate()
        screen.blit(self.frames[self.current_frame], self.rect)

        # pygame.draw.rect(screen, (255, 0, 0), self.get_collider_rect(), 1)
