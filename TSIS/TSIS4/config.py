# config.py — все константы проекта

WIDTH, HEIGHT = 600, 660   # +60px снизу под HUD
CELL_SIZE     = 20
GRID_WIDTH    = WIDTH  // CELL_SIZE   # 30
GRID_HEIGHT   = (HEIGHT - 60) // CELL_SIZE  # 30  (игровое поле без HUD)

FPS = 60   # pygame.time.Clock — только для отрисовки; скорость змейки через USEREVENT

# Базовая скорость (мс между шагами)
BASE_STEP_MS  = 150
MIN_STEP_MS   = 40

# Сколько еды до следующего уровня
FOOD_PER_LEVEL = 5

# Время жизни обычной еды (мс)
FOOD_LIFETIME_MS = 5000

# Время жизни power-up на поле (мс)
PU_FIELD_LIFE_MS = 8000

# Длительность эффекта power-up (мс)
PU_EFFECT_MS = 5000

# Скорость при speed-boost / slow-motion
BOOST_STEP_MS = 70
SLOW_STEP_MS  = 280

# Уровень, с которого появляются препятствия
OBSTACLE_LEVEL = 3
# Количество блоков препятствий за уровень
OBSTACLES_PER_LEVEL = 4

# Цвета (дефолтные; реальный цвет змейки берётся из settings.json)
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   140, 0)
RED        = (200, 0,   0)
POISON_CLR = (120, 0,   0)    # тёмно-красный — яд
YELLOW     = (255, 215, 0)
ORANGE     = (255, 140, 0)
BLUE       = (50,  120, 220)
CYAN       = (0,   220, 220)
GRAY       = (120, 120, 120)
DARK_GRAY  = (40,  40,  40)
DARK       = (15,  15,  25)
OBSTACLE_CLR = (160, 80, 0)   # коричневый блок

PU_COLORS = {
    "boost":  ORANGE,
    "slow":   CYAN,
    "shield": BLUE,
}
PU_LABELS = {
    "boost":  "▶▶",
    "slow":   "◀◀",
    "shield": "🛡",
}
