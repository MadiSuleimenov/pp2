import pygame
import sys
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()
font_big = pygame.font.SysFont("arial", 36)
font_small = pygame.font.SysFont("arial", 24)

player = MusicPlayer()

#color
BG = (20, 20, 30)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
GREEN = (0, 200, 120)

while True:
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    #UI
    title = font_big.render("Music Player", True, WHITE)
    track = font_small.render("Track: " + player.current(), True, WHITE)
    status = font_small.render("Status: " + player.status, True, GRAY)

    screen.blit(title, (250, 50))
    screen.blit(track, (50, 150))
    screen.blit(status, (50, 180))

    #Progress bar
    progress = player.get_progress()

    pygame.draw.rect(screen, GRAY, (50, 250, 600, 10))
    pygame.draw.rect(screen, GREEN, (50, 250, int(600 * progress), 10))

    #Controls hint
    controls = font_small.render("P-Play | S-Stop | N-Next | B-Back | Q-Quit", True, GRAY)
    screen.blit(controls, (50, 320))

    pygame.display.flip()
    clock.tick(60)