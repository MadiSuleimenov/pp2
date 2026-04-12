import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

x, y = 300, 200
R = 25
STEP = 20

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - STEP - R >= 0:
        x -= STEP
    if keys[pygame.K_RIGHT] and x + STEP + R <= 600:
        x += STEP
    if keys[pygame.K_UP] and y - STEP - R >= 0:
        y -= STEP
    if keys[pygame.K_DOWN] and y + STEP + R <= 400:
        y += STEP

    pygame.draw.circle(screen, (255, 0, 0), (x, y), R)

    pygame.display.flip()
    clock.tick(60)