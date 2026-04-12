import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

# ball settings
x, y = WIDTH // 2, HEIGHT // 2
RADIUS = 25
STEP = 20

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # move with boundaries
    if keys[pygame.K_LEFT] and x - STEP - RADIUS >= 0:
        x -= STEP
    if keys[pygame.K_RIGHT] and x + STEP + RADIUS <= WIDTH:
        x += STEP
    if keys[pygame.K_UP] and y - STEP - RADIUS >= 0:
        y -= STEP
    if keys[pygame.K_DOWN] and y + STEP + RADIUS <= HEIGHT:
        y += STEP

    # draw ball
    pygame.draw.circle(screen, (255, 0, 0), (x, y), RADIUS)

    pygame.display.flip()
    clock.tick(60)