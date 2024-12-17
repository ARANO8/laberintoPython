# main.py
import random
import pygame

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.enemy import Enemy
from game.level import Level
from game.player import Player
from game.utils import resource_path



def fade_in(screen, background, step=5):
    """
    Efecto de desvanecimiento de negro a visible (fade in).
    
    Args:
        screen (pygame.Surface): Superficie donde se renderiza el juego.
        background (pygame.Surface): Fondo a mostrar durante el desvanecimiento.
        step (int): Incremento de la opacidad en cada iteración. Cuanto menor, más lento.
    """
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))  # Negro sólido

    alpha = 255
    while alpha > 0:
        fade_surface.set_alpha(alpha)
        screen.blit(background, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)  # Control de tiempo por iteración
        alpha -= step  # Reducir opacidad progresivamente
        
def apply_night_effect(screen, opacity=128):
    """
    Aplica un efecto de noche en la pantalla, oscureciendo todo.
    
    Args:
        screen (pygame.Surface): Superficie donde se renderiza el juego.
        opacity (int): Nivel de opacidad del efecto (0-255).
    """
    night_filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    night_filter.fill((0, 0, 64))  # Azul oscuro
    night_filter.set_alpha(opacity)  # Opacidad ajustable
    screen.blit(night_filter, (0, 0))


def fade_out(screen, background, step=5):
    """
    Efecto de desvanecimiento de visible a negro (fade out).
    
    Args:
        screen (pygame.Surface): Superficie donde se renderiza el juego.
        background (pygame.Surface): Fondo visible antes del desvanecimiento.
        step (int): Incremento de la opacidad en cada iteración. Cuanto menor, más lento.
    """
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))  # Negro sólido

    alpha = 0
    while alpha < 255:
        fade_surface.set_alpha(alpha)
        screen.blit(background, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)  # Control de tiempo por iteración
        alpha += step  # Incrementar opacidad progresivamente

# Crear al enemigo
def create_enemy(player_rect, screen_width, screen_height, speed=3):
    """Genera un enemigo asegurándose de que no esté en la misma posición que el jugador."""
    while True:
        enemy_x = random.randint(0, screen_width - 40)  # Tamaño ajustado para el sprite del enemigo
        enemy_y = random.randint(0, screen_height - 40)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 40, 40)  # Tamaño del enemigo
        if not enemy_rect.colliderect(player_rect):  # Verificar que no colisione con el jugador
            break
    return Enemy(enemy_x, enemy_y, speed)


def show_start_screen(screen):
    """Pantalla de inicio del juego con efecto de desvanecimiento."""
    # Cargar imágenes
    
    background = pygame.image.load(resource_path("assets/images/credits5.png"))
    title = pygame.image.load(resource_path("assets/images/pokelogo (low res).png"))

    # Ajustar el fondo al tamaño de la pantalla
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Crear fuente para el texto
    font = pygame.font.Font(None, 36)
    text = font.render("Presione Enter para empezar", True, (255, 255, 255))

    # Cargar y reproducir música de la pantalla de inicio
    pygame.mixer.music.load(resource_path("assets/music/intro.mp3"))
    pygame.mixer.music.play(-1)

    # Aparecer progresivamente desde negro
    fade_in(screen, background, step=2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False  # Salir de la pantalla de inicio cuando se presiona Enter

        # Dibujar el fondo
        screen.blit(background, (0, 0))

        # Dibujar el título centrado
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title, title_rect)

        # Dibujar el texto debajo del título
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    # Desaparecer progresivamente hacia negro
    fade_out(screen, background, step=2)
    pygame.mixer.music.stop()  # Detener la música de la pantalla de inicio

def show_game_over_screen(screen):
    """Muestra la pantalla de Game Over con opciones y permite la interacción."""
    # Fondo negro para la pantalla de Game Over
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    # Crear fuente y texto
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    options = ["Intentar de nuevo", "Salir"]
    selected_option = 0

    # Posiciones del texto
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    # Aparecer progresivamente
    fade_in(screen, background, step=10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Mover selección hacia abajo
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_UP:  # Mover selección hacia arriba
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_RETURN:  # Confirmar selección
                    if selected_option == 0:  # Intentar de nuevo
                        return "retry"
                    elif selected_option == 1:  # Salir
                        return "quit"

        # Dibujar elementos
        screen.blit(background, (0, 0))
        screen.blit(game_over_text, game_over_rect)

        # Dibujar las opciones de menú
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            option_text = small_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            screen.blit(option_text, option_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def show_victory_screen(screen):
    """Muestra la pantalla de victoria."""
    # Fondo negro para la pantalla de victoria
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    # Crear fuente y texto
    font = pygame.font.Font(None, 74)
    victory_text = font.render("Has ganado", True, (255, 255, 0))

    # Posición del texto
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Aparecer progresivamente
    fade_in(screen, background, step=10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Dibujar elementos
        screen.blit(background, (0, 0))
        screen.blit(victory_text, victory_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COD 205 - Alan Israel Arnez Flores")
    clock = pygame.time.Clock()

    # Mostrar la pantalla de inicio
    show_start_screen(screen)

    # Cargar y reproducir música del juego principal
    pygame.mixer.music.load(resource_path("assets/music/Darkrai.mp3"))
    pygame.mixer.music.play(-1)

    # Lista de niveles
    levels = [resource_path("assets/levels/level1.txt"), resource_path("assets/levels/level2.txt")]
    current_level = 0

    # Crear al jugador
    initial_position = (38, 45)  # Posición inicial del jugador
    player = Player(*initial_position)

    # Crear al enemigo
    enemy = create_enemy(player.rect, SCREEN_WIDTH, SCREEN_HEIGHT, speed=3)

    running = True
    while running:
        # Cargar el nivel actual
        level = Level(levels[current_level], screen)

        # Reiniciar posiciones del jugador y enemigo
        player.rect.topleft = initial_position
        enemy = create_enemy(player.rect, SCREEN_WIDTH, SCREEN_HEIGHT, speed=3)

        # Aparecer progresivamente en la pantalla de juego
        fade_in(screen, pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)), step=5)

        # Bucle del nivel
        level_running = True
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level_running = False
                    running = False

            # Manejar la entrada del jugador y detectar colisiones
            player.handle_input(level.tiles)

            # Mover al enemigo
            enemy.move()

            # Detectar colisión entre el enemigo y el jugador
            if player.rect.colliderect(enemy.rect):
                print("¡Game Over!")
                fade_out(screen, pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)), step=10)
                result = show_game_over_screen(screen)
                if result == "retry":
                    break  # Reiniciar el nivel actual
                elif result == "quit":
                    running = False
                    break

            # Detectar si el jugador alcanzó la meta
            if level.goal and player.get_collider_rect().colliderect(level.goal):
                print(f"¡Nivel {current_level + 1} completado!")
                current_level += 1
                if current_level >= len(levels):  # Si no hay más niveles
                    fade_out(screen, pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)), step=10)
                    show_start_screen(screen)  # Volver a la pantalla de inicio
                    current_level = 0  # Reiniciar al primer nivel
                    break
                else:
                    level_running = False

            # Actualizar animaciones del jugador
            player.update()

            # Renderizar el nivel, el jugador y el enemigo
            level.render()
            apply_night_effect(screen, opacity=180)
            player.render(screen)
            enemy.render(screen)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()