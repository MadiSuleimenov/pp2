import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Setup
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Snake and food
snake = [(5, 5)]
direction = (1, 0)
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0
speed = 10
game_over = False

# чтобы скорость не росла бесконечно
last_speed_increase = 0

def draw_grid():
    win.fill(BLACK)

    pygame.draw.rect(win, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for segment in snake:
        pygame.draw.rect(win, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()


def reset_game():
    global snake, direction, food, score, speed, game_over, last_speed_increase

    snake = [(5, 5)]
    direction = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    score = 0
    speed = 10
    last_speed_increase = 0
    game_over = False


def update_snake():
    global food, score, speed, game_over, last_speed_increase

    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Collision with wall
    if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
        game_over = True
        return

    # Collision with self
    if new_head in snake:
        game_over = True
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

        # нормальное увеличение скорости
        if score // 5 > last_speed_increase:
            speed += 2
            last_speed_increase += 1
    else:
        snake.pop()


# Game loop
while True:
    clock.tick(speed)

    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        update_snake()
        draw_grid()

    else:
        win.fill(BLACK)
        over_text = font.render("Game Over! Press R to Restart", True, YELLOW)
        score_text = font.render(f"Final Score: {score}", True, WHITE)

        win.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 20))
        win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()