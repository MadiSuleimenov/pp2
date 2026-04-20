import pygame, sys
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 3  # только для фона
SCORE = 0
COINS = 0
game_over = False

LEVEL_UP_COINS = 5  # каждые 5 монет ускоряем врага

# Sounds
crash_sound = pygame.mixer.Sound("lab10/assets/crash.mp3")
drive_sound = pygame.mixer.Sound("lab10/assets/drive.mp3")
coin_sound = pygame.mixer.Sound("lab10/assets/coin.mp3")

drive_sound.play(-1)

font = pygame.font.SysFont("Verdana", 20)
background = pygame.image.load("lab10/assets/road.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")


# ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab10/assets/enemy.png")
        self.rect = self.image.get_rect()
        self.speed = 4  # скорость врага
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        global SCORE
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset()


# COIN
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.image.load("lab10/assets/coin.png")
        self.speed = 3  # скорость монеты
        self.reset()

    def reset(self):
        # случайный вес
        self.weight = random.randint(1, 3)

        # размер зависит от веса
        size = 20 + self.weight * 10
        self.image = pygame.transform.scale(self.base_image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def collect(self):
        global COINS

        COINS += self.weight
        coin_sound.play()

        # ускоряем только врага
        if COINS % LEVEL_UP_COINS == 0:
            E1.speed += 3

        self.reset()


# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab10/assets/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)
        if pressed[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 5)


# RESET
def reset_game():
    global SPEED, SCORE, COINS, game_over

    SPEED = 3
    SCORE = 0
    COINS = 0
    game_over = False

    P1.rect.center = (160, 520)
    E1.reset()
    C1.reset()

    E1.speed = 4  # сброс скорости врага

    drive_sound.play(-1)


# SETUP
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

background_y = 0


# LOOP
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if game_over and event.key == K_r:
                reset_game()

    if not game_over:

        # столкновение с врагом
        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play()
            drive_sound.stop()
            game_over = True

        # сбор монеты
        if pygame.sprite.spritecollideany(P1, coins):
            C1.collect()

        # движение фона
        background_y = (background_y + SPEED) % SCREEN_HEIGHT
        screen.blit(background, (0, background_y))
        screen.blit(background, (0, background_y - SCREEN_HEIGHT))

        # текст
        score_text = font.render(f"Score: {SCORE}", True, BLACK)
        coins_text = font.render(f"Coins: {COINS}", True, BLACK)
        enemy_speed_text = font.render(f"Enemy speed: {E1.speed}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (250, 10))
        screen.blit(enemy_speed_text, (120, 40))

        # отрисовка
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
            entity.move()

    else:
        screen.fill((255, 0, 0))
        text = font.render("Game Over! Press R", True, BLACK)
        screen.blit(text, (80, 300))

    pygame.display.update()
    FramePerSec.tick(FPS)