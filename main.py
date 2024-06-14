import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes pour la taille de l'écran
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

# Couleurs
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialisation de l'écran de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

# Police pour l'affichage du score
font = pygame.font.Font(None, 36)

# Fonction pour dessiner le serpent
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

# Fonction pour dessiner la pomme
def draw_apple(apple_position):
    pygame.draw.rect(screen, RED, pygame.Rect(apple_position[0], apple_position[1], CELL_SIZE, CELL_SIZE))

# Fonction pour déplacer le serpent
def move_snake(snake_body, snake_direction):
    head_x, head_y = snake_body[0]
    if snake_direction == 'UP':
        head_y -= CELL_SIZE
    elif snake_direction == 'DOWN':
        head_y += CELL_SIZE
    elif snake_direction == 'LEFT':
        head_x -= CELL_SIZE
    elif snake_direction == 'RIGHT':
        head_x += CELL_SIZE
    new_head = (head_x, head_y)
    snake_body.insert(0, new_head)
    return snake_body[:-1]  # Retourne le nouveau corps sans la dernière partie

# Fonction pour vérifier si le serpent a mangé la pomme
def check_apple_eaten(snake_head, apple_position):
    return snake_head == apple_position

# Fonction pour vérifier si le serpent s'est mordu ou est sorti de l'écran
def check_game_over(snake_body):
    head_x, head_y = snake_body[0]
    return (head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            (head_x, head_y) in snake_body[1:])

# Fonction pour afficher le score
def show_score(score):
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))

# Fonction pour afficher l'écran de fin de jeu
def show_game_over(score):
    game_over_surface = font.render(f'Game Over! Final Score: {score}', True, WHITE)
    screen.blit(game_over_surface, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Initialisation du serpent et de la pomme
snake_body = [(100, 100), (80, 100), (60, 100)]
snake_direction = 'RIGHT'
apple_position = (300, 300)

# Horloge pour contrôler la vitesse du jeu
clock = pygame.time.Clock()
score = 0

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Déplacer le serpent
    snake_body = move_snake(snake_body, snake_direction)

    # Vérifier si le serpent a mangé la pomme
    if check_apple_eaten(snake_body[0], apple_position):
        score += 10
        while True:
            apple_position = (random.randrange(0, SCREEN_WIDTH, CELL_SIZE),
                              random.randrange(0, SCREEN_HEIGHT, CELL_SIZE))
            if apple_position not in snake_body:
                break
        snake_body.append(snake_body[-1])  # Ajouter un nouveau bloc au serpent

    # Vérifier si le jeu est terminé
    if check_game_over(snake_body):
        show_game_over(score)
        running = False

    # Dessin sur l'écran
    screen.fill(BLACK)
    draw_snake(snake_body)
    draw_apple(apple_position)
    show_score(score)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse du jeu
    clock.tick(10)

# Quitter Pygame
pygame.quit()
