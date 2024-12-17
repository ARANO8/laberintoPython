import pygame
from game.utils import resource_path

class Player:
    def __init__(self, x, y):
        # Cargar el spritesheet
        self.spritesheet = pygame.image.load(resource_path("assets/images/jogador.png"))
        self.frames = self.load_frames(192, 256, 4, 4)  # Dimensiones del spritesheet (192x256), 4 filas, 4 columnas

        # Diccionario para animaciones por dirección
        self.animations = {
            "down": self.frames[0],
            "left": self.frames[1],
            "right": self.frames[2],
            "up": self.frames[3]
        }
        self.current_animation = "down"
        self.current_frame = 0

        # Rectángulo del jugador
        self.rect = pygame.Rect(x, y, 48, 64)  # Tamaño de cada cuadro (192/4 = 48, 256/4 = 64)
        self.speed = 3

        # Control de tiempo para animaciones
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100  # Tiempo entre frames en milisegundos
        self.is_moving = False  # Estado de movimiento
        
        # Margen personalizado para el colisionador
        self.collider_margin = {"left": 10, "right": 10, "top": 30, "bottom": 0}  # Reducir lados

        # Cargar sonido de pasos
        self.step_sound = pygame.mixer.Sound(resource_path("assets/sounds/steps.wav"))
        self.step_sound.set_volume(0.5)  # Ajustar el volumen (opcional)
        self.last_step_time = 0  # Control del tiempo del sonido
        self.step_interval = 200  # Tiempo entre sonidos de pasos (en milisegundos)

    def load_frames(self, width, height, rows, cols):
        """Divide el spritesheet en una lista de cuadros por filas y columnas."""
        frames = []
        frame_width = width // cols
        frame_height = height // rows

        for row in range(rows):
            row_frames = []
            for col in range(cols):
                frame = self.spritesheet.subsurface(pygame.Rect(
                    col * frame_width, row * frame_height, frame_width, frame_height
                ))
                row_frames.append(frame)
            frames.append(row_frames)
        return frames

    def handle_input(self, walls=None):
        """Mueve al jugador y cambia la animación según la dirección."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.is_moving = False  # Asumimos que no hay movimiento

        if keys[pygame.K_UP]:
            dy = -self.speed
            self.current_animation = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.current_animation = "down"
            self.is_moving = True
        elif keys[pygame.K_LEFT]:
            dx = -self.speed
            self.current_animation = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.current_animation = "right"
            self.is_moving = True

        # Movimiento tentativo
        self.rect.x += dx
        self.rect.y += dy

        # Verificar colisiones con paredes
        if walls:
            collider = self.get_collider_rect()  # Obtener el colisionador ajustado
            for row in walls:
                for wall in row:
                    if collider.colliderect(wall):  # Verificar colisión
                        # Deshacer movimiento
                        self.rect.x -= dx
                        self.rect.y -= dy
                        return

    def update(self):
        """Actualiza el frame actual para la animación y reproduce el sonido de pasos."""
        now = pygame.time.get_ticks()

        if self.is_moving:  # Solo anima y reproduce sonido si el jugador se mueve
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

            # Reproducir sonido de pasos
            if now - self.last_step_time > self.step_interval:
                self.step_sound.play()
                self.last_step_time = now
        else:
            self.current_frame = 0  # Frame estático si no se mueve
    
    def get_collider_rect(self):
        """Devuelve un rectángulo ajustado para colisiones."""
        margin = self.collider_margin
        return pygame.Rect(
            self.rect.x + margin["left"],
            self.rect.y + margin["top"],
            self.rect.width - margin["left"] - margin["right"],
            self.rect.height - margin["top"] - margin["bottom"]
        )

    def render(self, screen):
        """Renderiza el cuadro actual del jugador."""
        frame = self.animations[self.current_animation][self.current_frame]
        screen.blit(frame, self.rect)
        
        # # Debug: Renderizar el colisionador
        # pygame.draw.rect(screen, (255, 0, 0), self.get_collider_rect(), 1)  # Visualizar el colisionador
