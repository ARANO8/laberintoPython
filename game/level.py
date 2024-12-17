import pygame
from game.config import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from game.utils import resource_path

class Level:
    def __init__(self, level_file, screen):
        self.screen = screen
        self.tiles = []  # Matriz de paredes (rectángulos)
        self.sprites = []  # Matriz de sprites correspondientes a las paredes
        self.goal = None  # Coordenadas de la meta

        # Cargar el fondo (piso)
        self.floor_sprite = pygame.image.load(resource_path("assets/autotiles/Chão (4).png"))
        self.floor_width, self.floor_height = self.floor_sprite.get_size()

        # Cargar el spritesheet de paredes
        self.tree_spritesheet = pygame.image.load(resource_path("assets/images/Object tree 2.png"))  # Cargar spritesheet
        self.tree_sprites = self.load_spritesheet(128, 128, 4, 4)  # Dividir spritesheet en 16 cuadros
        self.load_level(level_file)

    def load_spritesheet(self, width, height, rows, cols):
        """Divide el spritesheet en una lista de cuadros por filas y columnas."""
        frames = []
        frame_width = width // cols
        frame_height = height // rows

        for row in range(rows):
            for col in range(cols):
                frame = self.tree_spritesheet.subsurface(pygame.Rect(
                    col * frame_width, row * frame_height, frame_width, frame_height
                ))
                frame = pygame.transform.scale(frame, (40, 40))  # Escalar cada cuadro a 40x40
                frames.append(frame)
        return frames

    def load_level(self, level_file):
        """Carga el nivel desde un archivo de texto."""
        with open(level_file, "r") as file:
            for y, line in enumerate(file):
                row_tiles = []
                row_sprites = []
                for x, char in enumerate(line.strip()):
                    if char == "1":  # Pared
                        # Crear un rectángulo para la colisión
                        row_tiles.append(pygame.Rect(x * 40, y * 40, 40, 40))
                        # Seleccionar un sprite del spritesheet de manera aleatoria
                        sprite_index = (x + y) % len(self.tree_sprites)  # Alternar sprites en base a la posición
                        row_sprites.append(self.tree_sprites[sprite_index])
                    elif char == "E":  # Meta
                        self.goal = pygame.Rect(x * 40, y * 40, 40, 40)
                self.tiles.append(row_tiles)
                self.sprites.append(row_sprites)

    def update(self):
        """Actualiza la lógica del nivel."""
        pass

    def render(self):
        """Renderiza el nivel en la pantalla."""
        self.render_floor()  # Renderizar el fondo primero
        for row_tiles, row_sprites in zip(self.tiles, self.sprites):
            for tile, sprite in zip(row_tiles, row_sprites):
                self.screen.blit(sprite, tile.topleft)

        # # Dibujar la meta sin resplandor
        # if self.goal:
        #     pygame.draw.rect(self.screen, (0, 255, 0), self.goal)  # Meta en verde (puedes ajustar el color o quitar esto)

    def render_floor(self):
        """Renderiza el piso del laberinto repitiendo el sprite en mosaico."""
        for y in range(0, SCREEN_HEIGHT, self.floor_height):
            for x in range(0, SCREEN_WIDTH, self.floor_width):
                self.screen.blit(self.floor_sprite, (x, y))
