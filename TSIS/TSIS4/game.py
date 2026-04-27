# game.py — вся игровая логика (змейка, еда, power-ups, препятствия)
import pygame
import random
from config import *


# вспомогательная функция

def _free_cell(blocked: set) -> tuple:
    """Случайная свободная клетка."""
    while True:
        c = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if c not in blocked:
            return c


# объекты поля

class Food:
    def __init__(self, blocked: set):
        self.pos      = _free_cell(blocked)
        self.value    = random.choice([1, 2, 3])
        self.poison   = False
        self.born     = pygame.time.get_ticks()

    @classmethod
    def poison_food(cls, blocked: set):
        f = cls.__new__(cls)
        f.pos    = _free_cell(blocked)
        f.value  = 0
        f.poison = True
        f.born   = pygame.time.get_ticks()
        return f

    def expired(self) -> bool:
        return pygame.time.get_ticks() - self.born > FOOD_LIFETIME_MS

    def draw(self, surf, cell):
        x, y = self.pos[0] * cell, self.pos[1] * cell
        color = POISON_CLR if self.poison else RED
        pygame.draw.rect(surf, color, (x, y, cell, cell))
        pygame.draw.rect(surf, WHITE, (x, y, cell, cell), 1)
        if not self.poison:
            lbl = pygame.font.SysFont("Arial", 14, bold=True).render(
                str(self.value), True, WHITE)
            surf.blit(lbl, (x + cell // 2 - lbl.get_width() // 2,
                            y + cell // 2 - lbl.get_height() // 2))
        else:
            lbl = pygame.font.SysFont("Arial", 12, bold=True).render("☠", True, (255, 80, 80))
            surf.blit(lbl, (x + 3, y + 2))


class PowerUp:
    def __init__(self, kind: str, blocked: set):
        self.kind  = kind
        self.pos   = _free_cell(blocked)
        self.born  = pygame.time.get_ticks()

    def expired(self) -> bool:
        return pygame.time.get_ticks() - self.born > PU_FIELD_LIFE_MS

    def draw(self, surf, cell):
        x, y  = self.pos[0] * cell, self.pos[1] * cell
        color = PU_COLORS.get(self.kind, YELLOW)
        pygame.draw.rect(surf, color, (x + 1, y + 1, cell - 2, cell - 2), border_radius=4)
        pygame.draw.rect(surf, WHITE, (x + 1, y + 1, cell - 2, cell - 2), 1, border_radius=4)
        lbl = pygame.font.SysFont("Arial", 11, bold=True).render(
            PU_LABELS.get(self.kind, "?"), True, WHITE)
        surf.blit(lbl, (x + cell // 2 - lbl.get_width() // 2,
                        y + cell // 2 - lbl.get_height() // 2))


# основное состояние

class Game:
    STEP_EVENT = pygame.USEREVENT + 1

    def __init__(self, username: str, personal_best: int, snake_color, grid: bool):
        self.username      = username
        self.personal_best = personal_best
        self.snake_color   = tuple(snake_color)
        self.grid          = grid

        self.font_sm = pygame.font.SysFont("Arial", 16)
        self.font_md = pygame.font.SysFont("Arial", 20, bold=True)

        self._reset()

    # инициализация

    def _reset(self):
        self.snake     = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.next_dir  = (1, 0)

        self.score      = 0
        self.level      = 1
        self.food_count = 0   # сколько еды съедено на этом уровне
        self.step_ms    = BASE_STEP_MS
        self.done       = False
        self.reason     = ""

        self.obstacles: set = set()

        self.foods:   list[Food]    = []
        self.powerup: PowerUp | None = None

        # активный эффект: {"kind": str, "end": int}
        self.effect: dict | None = None
        self.shield_ready = False   # щит активирован (ждёт столкновения)

        pygame.time.set_timer(self.STEP_EVENT, self.step_ms)
        self._spawn_food()

    # блокированные клетки

    def _blocked(self) -> set:
        b = set(self.snake) | self.obstacles
        for f in self.foods:
            b.add(f.pos)
        if self.powerup:
            b.add(self.powerup.pos)
        return b

    #  спаун

    def _spawn_food(self):
        # обычная еда
        if not any(not f.poison for f in self.foods):
            self.foods.append(Food(self._blocked()))
        # яд (50% шанс, не чаще одного)
        if not any(f.poison for f in self.foods) and random.random() < 0.5:
            self.foods.append(Food.poison_food(self._blocked()))

    def _spawn_powerup(self):
        if self.powerup is None:
            kind = random.choice(["boost", "slow", "shield"])
            self.powerup = PowerUp(kind, self._blocked())

    def _place_obstacles(self):
        """Добавляет блоки препятствий на новом уровне."""
        count   = (self.level - OBSTACLE_LEVEL) * OBSTACLES_PER_LEVEL + OBSTACLES_PER_LEVEL
        head    = self.snake[0]
        safe    = {(head[0] + dx, head[1] + dy)
                   for dx in range(-3, 4) for dy in range(-3, 4)}
        attempts = 0
        while len(self.obstacles) < count and attempts < 500:
            attempts += 1
            c = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if c not in safe and c not in set(self.snake) and c not in self.obstacles:
                self.obstacles.add(c)

    # скорость

    def _apply_speed(self):
        if self.effect:
            if self.effect["kind"] == "boost":
                ms = BOOST_STEP_MS
            elif self.effect["kind"] == "slow":
                ms = SLOW_STEP_MS
            else:
                ms = self.step_ms
        else:
            ms = self.step_ms
        pygame.time.set_timer(self.STEP_EVENT, ms)

    # события 

    def handle_key(self, key):
        dirs = {
            pygame.K_UP:    (0, -1),
            pygame.K_DOWN:  (0,  1),
            pygame.K_LEFT:  (-1, 0),
            pygame.K_RIGHT: (1,  0),
        }
        if key in dirs:
            nd = dirs[key]
            # нельзя развернуться на 180°
            if (nd[0] + self.direction[0], nd[1] + self.direction[1]) != (0, 0):
                self.next_dir = nd

    def step(self):
        """Один шаг змейки — вызывается по STEP_EVENT."""
        if self.done:
            return

        self.direction = self.next_dir
        head    = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # столкновения
        wall_hit = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT)
        self_hit = new_head in self.snake
        obs_hit  = new_head in self.obstacles

        if wall_hit or self_hit or obs_hit:
            if self.shield_ready:
                self.shield_ready = False
                self.effect       = None
                self._apply_speed()
                # телепортируем на голову (остаёмся на месте — пропускаем шаг)
                return
            reason_map = {wall_hit: "Wall collision!", self_hit: "Self collision!", obs_hit: "Obstacle hit!"}
            self.done   = True
            self.reason = next(r for cond, r in reason_map.items() if cond)
            pygame.time.set_timer(self.STEP_EVENT, 0)
            return

        self.snake.insert(0, new_head)

        # еда
        ate = False
        for f in self.foods[:]:
            if new_head == f.pos:
                self.foods.remove(f)
                ate = True
                if f.poison:
                    self.snake = self.snake[:-2] if len(self.snake) > 3 else self.snake[:1]
                    if len(self.snake) <= 1:
                        self.done   = True
                        self.reason = "Poisoned!"
                        pygame.time.set_timer(self.STEP_EVENT, 0)
                        return
                else:
                    self.score      += f.value
                    self.food_count += 1
                    if self.food_count >= FOOD_PER_LEVEL:
                        self._level_up()
                break

        if not ate:
            self.snake.pop()

        # power-up
        if self.powerup and new_head == self.powerup.pos:
            self._activate_powerup(self.powerup.kind)
            self.powerup = None

        # таймеры спауна
        self._tick_spawns()

    def _level_up(self):
        self.level      += 1
        self.food_count  = 0
        self.step_ms     = max(MIN_STEP_MS, self.step_ms - 15)
        self._apply_speed()
        if self.level >= OBSTACLE_LEVEL:
            self._place_obstacles()

    def _activate_powerup(self, kind: str):
        end = pygame.time.get_ticks() + PU_EFFECT_MS
        self.effect = {"kind": kind, "end": end}
        if kind == "shield":
            self.shield_ready = True
        self._apply_speed()

    def _tick_spawns(self):
        now = pygame.time.get_ticks()

        # истёкшая еда
        self.foods = [f for f in self.foods if not f.expired()]
        self._spawn_food()

        # истёкший power-up на поле
        if self.powerup and self.powerup.expired():
            self.powerup = None

        # спаун power-up каждые ~10 секунд случайно
        if self.powerup is None and random.random() < 0.01:
            self._spawn_powerup()

        # истёкший эффект
        if self.effect and now > self.effect["end"]:
            self.effect       = None
            self.shield_ready = False
            self._apply_speed()

    # отрисовка

    def draw(self, surf: pygame.Surface):
        cell = CELL_SIZE
        gw   = GRID_WIDTH  * cell
        gh   = GRID_HEIGHT * cell

        # фон поля
        pygame.draw.rect(surf, DARK, (0, 0, gw, gh))

        # сетка
        if self.grid:
            for x in range(0, gw, cell):
                pygame.draw.line(surf, DARK_GRAY, (x, 0), (x, gh))
            for y in range(0, gh, cell):
                pygame.draw.line(surf, DARK_GRAY, (0, y), (gw, y))

        # препятствия
        for ox, oy in self.obstacles:
            pygame.draw.rect(surf, OBSTACLE_CLR, (ox*cell, oy*cell, cell, cell))
            pygame.draw.rect(surf, (200, 120, 40), (ox*cell, oy*cell, cell, cell), 1)

        # еда
        for f in self.foods:
            f.draw(surf, cell)

        # power-up на поле
        if self.powerup:
            self.powerup.draw(surf, cell)

        # змейка
        for i, (sx, sy) in enumerate(self.snake):
            color = self.snake_color if i > 0 else tuple(
                min(255, c + 60) for c in self.snake_color)
            pygame.draw.rect(surf, color, (sx*cell, sy*cell, cell, cell))
            pygame.draw.rect(surf, BLACK,  (sx*cell, sy*cell, cell, cell), 1)

        # HUD (нижняя полоска)
        hud_y = gh
        pygame.draw.rect(surf, (20, 20, 35), (0, hud_y, gw, 60))
        pygame.draw.line(surf, GRAY, (0, hud_y), (gw, hud_y), 1)

        now = pygame.time.get_ticks()

        # левая часть HUD
        surf.blit(self.font_md.render(f"Score: {self.score}", True, YELLOW), (8, hud_y + 4))
        surf.blit(self.font_sm.render(f"Best: {self.personal_best}", True, GRAY), (8, hud_y + 28))

        # центр HUD
        surf.blit(self.font_md.render(f"Level {self.level}", True, WHITE),
                  (gw // 2 - 30, hud_y + 4))
        # прогресс до следующего уровня
        bar_w = int((self.food_count / FOOD_PER_LEVEL) * 120)
        pygame.draw.rect(surf, DARK_GRAY, (gw // 2 - 60, hud_y + 34, 120, 10), border_radius=4)
        pygame.draw.rect(surf, GREEN,     (gw // 2 - 60, hud_y + 34, bar_w, 10), border_radius=4)

        # правая часть HUD — активный эффект
        if self.effect:
            secs_left = max(0, (self.effect["end"] - now) // 1000)
            col = PU_COLORS.get(self.effect["kind"], WHITE)
            lbl = f"{PU_LABELS[self.effect['kind']]} {secs_left}s"
            surf.blit(self.font_md.render(lbl, True, col), (gw - 90, hud_y + 4))
        if self.shield_ready:
            surf.blit(self.font_sm.render("SHIELD", True, BLUE), (gw - 70, hud_y + 30))
