import pygame
import random
import os

from ui import (
    WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, GRAY,
    CAR_COLORS, WIDTH, HEIGHT, draw_hud
)

BASE_DIR = os.path.dirname(__file__)

def _asset(name):
    return os.path.join(BASE_DIR, "assets", name)

def _make_car(color, w=40, h=70):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, color,           (4,  10, w-8, h-20), border_radius=8)
    pygame.draw.rect(s, (160, 210, 255), (8,  14, w-16, 16),  border_radius=3)
    pygame.draw.rect(s, (255, 80, 80),   (6,  h-18, 10, 6),   border_radius=2)
    pygame.draw.rect(s, (255, 80, 80),   (w-16, h-18, 10, 6), border_radius=2)
    for bx, by in [(0, 14), (w-6, 14), (0, h-28), (w-6, h-28)]:
        pygame.draw.rect(s, (20, 20, 20), (bx, by, 6, 16), border_radius=3)
    return s

def _make_enemy_car(w=38, h=65):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (180, 30, 30),   (3,  8,  w-6, h-16), border_radius=8)
    pygame.draw.rect(s, (120, 180, 255), (7,  12, w-14, 14),  border_radius=3)
    pygame.draw.rect(s, (255, 220, 0),   (5,  h-14, 10, 5),   border_radius=2)
    pygame.draw.rect(s, (255, 220, 0),   (w-15, h-14, 10, 5), border_radius=2)
    for bx, by in [(0, 12), (w-6, 12), (0, h-26), (w-6, h-26)]:
        pygame.draw.rect(s, (20, 20, 20), (bx, by, 6, 14), border_radius=3)
    return s

def load_image(name, size=None, fallback=None):
    try:
        img = pygame.image.load(_asset(name)).convert_alpha()
        return pygame.transform.scale(img, size) if size else img
    except Exception:
        return fallback() if fallback else pygame.Surface(size or (40, 70), pygame.SRCALPHA)

def load_sound(name):
    try:    return pygame.mixer.Sound(_asset(name))
    except: return None

background  = None
coin_img    = None
crash_sound = coin_sound = drive_sound = menu_sound = None

def load_assets():
    global background, coin_img, crash_sound, coin_sound, drive_sound, menu_sound
    background  = load_image("road.png", (WIDTH, HEIGHT), fallback=_make_road)
    coin_img    = load_image("coin.png", (28, 28),        fallback=_make_coin)
    crash_sound = load_sound("crash.mp3")
    coin_sound  = load_sound("coin.mp3")
    drive_sound = load_sound("drive.mp3")
    menu_sound  = load_sound("menu.mp3")

def _make_road():
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill((80, 80, 80))
    for y in range(0, HEIGHT, 60):
        pygame.draw.rect(s, (230, 200, 0), (WIDTH//2 - 3, y, 6, 35))
    pygame.draw.rect(s, (220, 220, 220), (60,  0, 4, HEIGHT))
    pygame.draw.rect(s, (220, 220, 220), (336, 0, 4, HEIGHT))
    return s

def _make_coin():
    s = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 200, 0),  (14, 14), 14)
    pygame.draw.circle(s, (255, 230, 80), (11, 11),  6)
    return s

DIFF = {
    "easy":   {"speed": 2, "enemy_ms": 2500, "coin_ms": 1600, "obs_ms": 3500, "max_enemies": 2},
    "normal": {"speed": 4, "enemy_ms": 1400, "coin_ms": 1300, "obs_ms": 2000, "max_enemies": 4},
    "hard":   {"speed": 7, "enemy_ms":  700, "coin_ms": 1000, "obs_ms": 1100, "max_enemies": 8},
}
MAX_LIVES = 3


class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="red"):
        super().__init__()
        color_rgb = CAR_COLORS.get(car_color, (220, 50, 50))
        try:
            base = pygame.image.load(_asset("player.png")).convert_alpha()
            w, h = base.get_size()
            # Создаём копию и рисуем цветной слой только там, где есть непрозрачные пиксели
            colored = base.copy()
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((*color_rgb, 140))   # полупрозрачный цвет
            # BLEND_RGBA_ADD добавляет цвет поверх, сохраняя альфа-маску оригинала
            colored.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.image = colored
        except Exception:
            self.image = _make_car(color_rgb)
        self.rect       = self.image.get_rect(center=(WIDTH // 2, 500))
        self.has_shield = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        dy = (keys[pygame.K_DOWN]  - keys[pygame.K_UP])   * 5
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def draw_shield(self, surf):
        if self.has_shield:
            pygame.draw.circle(surf, (80, 160, 255), self.rect.center, 36, 3)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, spd):
        super().__init__()
        try:
            self.image = pygame.image.load(_asset("enemy.png")).convert_alpha()
        except Exception:
            self.image = _make_enemy_car()
        self.rect  = self.image.get_rect(center=(random.randint(70, WIDTH-70), -100))
        self.speed = spd + random.uniform(0, 1.5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, spd):
        super().__init__()
        self.value = random.randint(1, 3)
        size = 18 + self.value * 5
        self.image = pygame.transform.scale(coin_img, (size, size))
        self.rect  = self.image.get_rect(center=(random.randint(70, WIDTH-70), -60))
        self.speed = spd

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()


class Obstacle(pygame.sprite.Sprite):
    KINDS = ["oil", "pothole", "barrier", "bump"]

    def __init__(self, spd):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.speed = spd
        self.image = self._draw()
        self.rect  = self.image.get_rect(center=(random.randint(70, WIDTH-70), -60))

    def _draw(self):
        k = self.kind
        if k == "oil":
            s = pygame.Surface((60, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (100,  40, 200, 230), (0,  0, 60, 30))
            pygame.draw.ellipse(s, (180, 120, 255, 160), (12, 7, 30, 14))
            lbl = pygame.font.SysFont("Arial", 10, bold=True).render("OIL", True, (255,255,255))
            s.blit(lbl, (30 - lbl.get_width()//2, 15 - lbl.get_height()//2))
            return s
        elif k == "pothole":
            s = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.circle(s, (60, 40, 10), (19, 19), 19)
            pygame.draw.circle(s, (30, 20,  5), (19, 19), 12)
            pygame.draw.circle(s, (80, 60, 20), (14, 14),  4)
            return s
        elif k == "barrier":
            s = pygame.Surface((70, 22), pygame.SRCALPHA)
            pygame.draw.rect(s, RED,           (0,  0, 70, 22), border_radius=4)
            pygame.draw.rect(s, YELLOW,        (0,  0, 24, 22))
            pygame.draw.rect(s, YELLOW,        (46, 0, 24, 22))
            pygame.draw.rect(s, (255,255,255), (0,  0, 70, 22), 2, border_radius=4)
            return s
        else:  # bump
            s = pygame.Surface((65, 14), pygame.SRCALPHA)
            pygame.draw.rect(s, (160, 160, 160), (0, 0, 65, 14), border_radius=7)
            pygame.draw.rect(s, (200, 200, 200), (5, 3, 55,  6), border_radius=3)
            return s

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()


class PowerUp(pygame.sprite.Sprite):
    KINDS  = ["nitro", "shield", "repair"]
    COLORS = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}
    LABELS = {"nitro": "N", "shield": "S", "repair": "R"}
    LIFE   = 7000

    def __init__(self, spd):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.speed = spd
        self.born  = pygame.time.get_ticks()
        s = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.rect(s, self.COLORS[self.kind], (0, 0, 44, 44), border_radius=12)
        pygame.draw.rect(s, WHITE, (0, 0, 44, 44), 2, border_radius=12)
        lbl = pygame.font.SysFont("Arial", 24, bold=True).render(self.LABELS[self.kind], True, WHITE)
        s.blit(lbl, (22 - lbl.get_width()//2, 22 - lbl.get_height()//2))
        self.image = s
        self.rect  = s.get_rect(center=(random.randint(70, WIDTH-70), -60))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT or pygame.time.get_ticks() - self.born > self.LIFE:
            self.kill()


def make_game(settings):
    cfg = DIFF[settings.get("difficulty", "normal")]
    return {
        "player":       Player(settings.get("car_color", "red")),
        "enemies":      pygame.sprite.Group(),
        "coins":        pygame.sprite.Group(),
        "obstacles":    pygame.sprite.Group(),
        "powerups":     pygame.sprite.Group(),
        "score":        0,
        "coins_n":      0,
        "distance":     0,
        "_dist_acc":    0.0,
        "_nitro_bonus": 0,
        "bg_y":         0,
        "base_spd":     cfg["speed"],
        "speed":        cfg["speed"],
        "nitro_end":    0,
        "slow_end":     0,
        "active_pu":    None,
        "enemy_ms":     cfg["enemy_ms"],
        "coin_ms":      cfg["coin_ms"],
        "obs_ms":       cfg["obs_ms"],
        "max_enemies":  cfg["max_enemies"],
        "enemy_t":      0, "coin_t": 0, "obs_t": 0, "pu_t": 0,
        "lives":        MAX_LIVES,
        "invincible":   0,
        "done":         False,
        "reason":       "",
    }


def update_game(g, dt, settings):
    p   = g["player"]
    now = pygame.time.get_ticks()
    dt_sec = dt / 1000.0

    road_spd = g["base_spd"] + min(g["distance"] // 200, 4)

    if now < g["slow_end"]:
        road_spd = max(1, road_spd - 2)

    if g["active_pu"] == "nitro":
        if now < g["nitro_end"]:
            road_spd += 5
            g["_nitro_bonus"] += dt_sec * 3
        else:
            g["active_pu"] = None

    g["speed"] = road_spd

    g["_dist_acc"] += dt_sec * road_spd * 1.2
    g["distance"]   = int(g["_dist_acc"])
    g["score"]      = g["distance"] + g["coins_n"] * 10 + int(g["_nitro_bonus"])

    g["enemy_t"] += dt;  g["coin_t"] += dt
    g["obs_t"]   += dt;  g["pu_t"]   += dt

    enemy_int = max(400, g["enemy_ms"] - g["distance"] // 2)
    if g["enemy_t"] >= enemy_int and len(g["enemies"]) < g["max_enemies"]:
        g["enemy_t"] = 0
        _spawn_enemy(g, road_spd)

    if g["coin_t"] >= g["coin_ms"]:
        g["coin_t"] = 0
        g["coins"].add(Coin(road_spd))

    if g["obs_t"] >= g["obs_ms"]:
        g["obs_t"] = 0
        _spawn_obstacle(g, road_spd)

    if g["pu_t"] >= 5000 and not g["powerups"]:
        g["pu_t"] = 0
        g["powerups"].add(PowerUp(road_spd))

    p.update()
    for grp in (g["enemies"], g["coins"], g["obstacles"], g["powerups"]):
        grp.update()

    inv = now < g["invincible"]

    if pygame.sprite.spritecollide(p, g["enemies"], True) and not inv:
        if p.has_shield:
            p.has_shield = False; g["active_pu"] = None
        else:
            _hit(g, settings, "Traffic crash!")
        if g["done"]: return

    for obs in pygame.sprite.spritecollide(p, g["obstacles"], True):
        if obs.kind in ("pothole", "barrier"):
            if not inv:
                if p.has_shield:
                    p.has_shield = False; g["active_pu"] = None
                else:
                    _hit(g, settings, f"Hit {obs.kind}!")
                if g["done"]: return
        else:
            g["slow_end"] = now + 2500

    for c in pygame.sprite.spritecollide(p, g["coins"], True):
        g["coins_n"] += c.value
        if coin_sound and settings["sound"]: coin_sound.play()

    for pu in pygame.sprite.spritecollide(p, g["powerups"], True):
        _powerup(g, pu, settings)


def _hit(g, settings, reason):
    g["lives"] -= 1
    if crash_sound and settings["sound"]: crash_sound.play()
    if g["lives"] <= 0:
        g["done"] = True; g["reason"] = reason
    else:
        g["invincible"] = pygame.time.get_ticks() + 1800

def _spawn_enemy(g, spd):
    e = Enemy(spd)
    if abs(e.rect.centerx - g["player"].rect.centerx) < 70:
        e.rect.x = max(70, min(WIDTH-70, e.rect.x + random.choice([-100, 100])))
    g["enemies"].add(e)

def _spawn_obstacle(g, spd):
    ob = Obstacle(spd)
    if abs(ob.rect.centerx - g["player"].rect.centerx) < 70:
        ob.rect.x = max(70, min(WIDTH-70, ob.rect.x + random.choice([-100, 100])))
    g["obstacles"].add(ob)

def _powerup(g, pu, settings):
    p = g["player"]
    if pu.kind == "nitro":
        g["active_pu"] = "nitro"
        g["nitro_end"] = pygame.time.get_ticks() + 4000
    elif pu.kind == "shield":
        p.has_shield   = True
        g["active_pu"] = "shield"
    elif pu.kind == "repair":
        if g["lives"] < MAX_LIVES: g["lives"] += 1
        g["slow_end"] = 0
    if coin_sound and settings["sound"]: coin_sound.play()


def draw_game(g, screen):
    spd = g["speed"]
    g["bg_y"] = (g["bg_y"] + spd) % HEIGHT
    screen.blit(background, (0, g["bg_y"] - HEIGHT))
    screen.blit(background, (0, g["bg_y"]))

    for grp in (g["enemies"], g["coins"], g["obstacles"], g["powerups"]):
        grp.draw(screen)

    p   = g["player"]
    now = pygame.time.get_ticks()
    if not (now < g["invincible"] and (now // 120) % 2 == 1):
        screen.blit(p.image, p.rect)
    p.draw_shield(screen)

    if g["active_pu"] == "nitro" and now < g["nitro_end"]:
        for fx in (-10, 10):
            cx = p.rect.centerx + fx
            for i, col in enumerate([(255, 60, 0), (255, 160, 0), (255, 220, 60)]):
                length = random.randint(8, 18) - i * 3
                pygame.draw.line(screen, col,
                                 (cx, p.rect.bottom + i * 4),
                                 (cx + random.randint(-2, 2), p.rect.bottom + i * 4 + length),
                                 max(1, 3 - i))

    if now < g["slow_end"]:
        fog = pygame.Surface((WIDTH, 30), pygame.SRCALPHA)
        fog.fill((80, 80, 200, 60))
        screen.blit(fog, (0, HEIGHT - 30))

    pu_secs = max(0, (g["nitro_end"] - now) // 1000) if g["active_pu"] == "nitro" else 0
    draw_hud(g["score"], g["coins_n"], g["distance"],
             g["active_pu"], pu_secs, p.has_shield, g["lives"])
