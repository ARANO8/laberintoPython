# main.py
import pygame
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.level import Level
from game.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    # Lista de niveles
    levels = ["assets/levels/level1.txt", "assets/levels/level2.txt"]
    current_level = 0

    # Crear al jugador
    player = Player(50, 50)  # Posición inicial del jugador

    running = True
    while running:
        # Cargar el nivel actual
        level = Level(levels[current_level], screen)

        # Bucle del nivel
        level_running = True
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level_running = False
                    running = False

            # Manejar la entrada del jugador y detectar colisiones
            player.handle_input(level.tiles)

            # Detectar si el jugador alcanzó la meta
            if level.goal and player.rect.colliderect(level.goal):
                print(f"¡Nivel {current_level + 1} completado!")
                current_level += 1
                if current_level >= len(levels):  # Si no hay más niveles, termina el juego
                    print("¡Has completado todos los niveles!")
                    running = False
                level_running = False

            # Renderizar el nivel y el jugador
            level.render()
            player.render(screen)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
