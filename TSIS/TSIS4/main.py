# main.py — стейт-машина и все экраны
import pygame
import sys
import db
import settings as stt
from game import Game
from config import *

# init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake — TSIS 4")
clock = pygame.time.Clock()

font_big  = pygame.font.SysFont("Arial", 42, bold=True)
font_md   = pygame.font.SysFont("Arial", 24, bold=True)
font_sm   = pygame.font.SysFont("Arial", 18)
font_xs   = pygame.font.SysFont("Arial", 14)

# DB
db_ok = db.init_db()

# Settings
cfg = stt.load()


# Helpers

def draw_text(text, x, y, color=WHITE, f=None):
    f = f or font_sm
    screen.blit(f.render(text, True, color), (x, y))


def draw_btn(rect: pygame.Rect, text: str, color=BLUE, hover=False):
    col = tuple(min(255, c + 30) for c in color) if hover else color
    pygame.draw.rect(screen, col, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    lbl = font_sm.render(text, True, WHITE)
    screen.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                      rect.centery - lbl.get_height() // 2))


def center_x(surf_or_width, text, f):
    lbl = f.render(text, True, WHITE)
    return (surf_or_width - lbl.get_width()) // 2


# State
state        = "menu"
username     = ""
name_buf     = ""
game: Game | None = None
last_result  = {}    # score, level, personal_best

# Button rects
BTN_PLAY   = pygame.Rect(200, 230, 200, 46)
BTN_BOARD  = pygame.Rect(200, 292, 200, 46)
BTN_SETT   = pygame.Rect(200, 354, 200, 46)
BTN_QUIT   = pygame.Rect(200, 416, 200, 46)

BTN_RETRY  = pygame.Rect(80,  460, 160, 46)
BTN_MMENU  = pygame.Rect(360, 460, 160, 46)

BTN_BACK   = pygame.Rect(220, 580, 160, 40)

# Settings btns
BTN_GRID   = pygame.Rect(340, 180, 120, 36)
BTN_SOUND  = pygame.Rect(340, 240, 120, 36)
BTN_SAVE   = pygame.Rect(200, 560, 200, 42)
COLOR_BTNS = {
    "Green":  (pygame.Rect(60,  320, 120, 36), (0,   200, 0)),
    "Blue":   (pygame.Rect(200, 320, 120, 36), (50,  120, 220)),
    "Yellow": (pygame.Rect(340, 320, 120, 36), (230, 200, 0)),
    "Red":    (pygame.Rect(60,  370, 120, 36), (220, 50,  50)),
    "Cyan":   (pygame.Rect(200, 370, 120, 36), (0,   220, 220)),
    "Purple": (pygame.Rect(340, 370, 120, 36), (160, 60,  220)),
}
#  SCREENS

def screen_menu(mouse):
    screen.fill(DARK)
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, (18, 18, 30), (0, y, WIDTH, 20))

    draw_text("SNAKE", center_x(WIDTH, "SNAKE", font_big), 80, YELLOW, font_big)
    draw_text("TSIS 4", center_x(WIDTH, "TSIS 4", font_xs), 138, GRAY, font_xs)

    # Username display
    if username:
        draw_text(f"Player: {username}", center_x(WIDTH, f"Player: {username}", font_sm),
                  185, GREEN, font_sm)
    else:
        draw_text("Enter username below to play", 120, 185, GRAY, font_xs)

    for rect, label, col in [
        (BTN_PLAY,  "Play",        GREEN),
        (BTN_BOARD, "Leaderboard", BLUE),
        (BTN_SETT,  "Settings",    GRAY),
        (BTN_QUIT,  "Quit",        RED),
    ]:
        draw_btn(rect, label, col, hover=rect.collidepoint(mouse))

    # name input box
    box = pygame.Rect(150, 490, 300, 42)
    pygame.draw.rect(screen, DARK_GRAY, box, border_radius=6)
    pygame.draw.rect(screen, WHITE,     box, 2,  border_radius=6)
    draw_text(name_buf + "|", 160, 501, WHITE, font_sm)
    draw_text("Type name + ENTER", 185, 545, GRAY, font_xs)


def screen_game():
    if game:
        game.draw(screen)


def screen_game_over(mouse):
    screen.fill((40, 0, 0))
    draw_text("GAME OVER", center_x(WIDTH, "GAME OVER", font_big), 70, RED, font_big)
    reason = last_result.get("reason", "")
    if reason:
        draw_text(reason, center_x(WIDTH, reason, font_sm), 140, ORANGE, font_sm)

    rows = [
        (f"Score:        {last_result.get('score', 0)}", WHITE),
        (f"Level:        {last_result.get('level', 1)}",  WHITE),
        (f"Personal best:{last_result.get('personal_best', 0)}", YELLOW),
    ]
    for i, (txt, col) in enumerate(rows):
        draw_text(txt, 160, 200 + i * 50, col, font_md)

    if not db_ok:
        draw_text("(DB offline — score not saved)", 140, 380, GRAY, font_xs)

    draw_btn(BTN_RETRY, "Retry",     GREEN, BTN_RETRY.collidepoint(mouse))
    draw_btn(BTN_MMENU, "Main Menu", BLUE,  BTN_MMENU.collidepoint(mouse))


def screen_leaderboard(mouse):
    screen.fill(DARK)
    draw_text("Leaderboard", center_x(WIDTH, "Leaderboard", font_big), 30, YELLOW, font_big)

    headers = ["#", "Username", "Score", "Level", "Date"]
    col_x   = [20, 60, 220, 320, 400]
    y0      = 110
    for h, cx in zip(headers, col_x):
        draw_text(h, cx, y0, GRAY, font_xs)
    pygame.draw.line(screen, GRAY, (10, y0 + 20), (WIDTH - 10, y0 + 20))

    board = db.get_leaderboard(10) if db_ok else []
    for i, row in enumerate(board):
        y   = y0 + 30 + i * 38
        col = YELLOW if i == 0 else (220, 180, 80) if i < 3 else WHITE
        vals = [str(i + 1), row["username"][:12], str(row["score"]),
                str(row["level_reached"]), str(row.get("date", ""))]
        for v, cx in zip(vals, col_x):
            draw_text(v, cx, y, col, font_xs)
        pygame.draw.line(screen, DARK_GRAY, (10, y + 28), (WIDTH - 10, y + 28))

    if not board:
        draw_text("No records yet" if db_ok else "Database offline",
                  center_x(WIDTH, "No records yet", font_sm), 280, GRAY, font_sm)

    draw_btn(BTN_BACK, "Back", GRAY, BTN_BACK.collidepoint(mouse))


def screen_settings(mouse):
    screen.fill(DARK)
    draw_text("Settings", center_x(WIDTH, "Settings", font_big), 40, WHITE, font_big)

    # Grid toggle
    draw_text("Grid overlay:", 60, 188, GRAY, font_sm)
    draw_btn(BTN_GRID,  "ON" if cfg["grid"]  else "OFF",
             GREEN if cfg["grid"]  else GRAY, BTN_GRID.collidepoint(mouse))

    # Sound toggle
    draw_text("Sound:", 60, 248, GRAY, font_sm)
    draw_btn(BTN_SOUND, "ON" if cfg["sound"] else "OFF",
             GREEN if cfg["sound"] else GRAY, BTN_SOUND.collidepoint(mouse))

    # Snake color
    draw_text("Snake colour:", 60, 288, GRAY, font_sm)
    current = tuple(cfg["snake_color"])
    for name, (rect, rgb) in COLOR_BTNS.items():
        pygame.draw.rect(screen, rgb, rect, border_radius=6)
        if current == rgb:
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=6)
        draw_text(name, rect.x + 8, rect.y + 9, WHITE, font_xs)

    draw_btn(BTN_SAVE, "Save & Back", BLUE, BTN_SAVE.collidepoint(mouse))

#  MAIN LOOP

while True:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            stt.save(cfg)
            pygame.quit()
            sys.exit()

        # MENU
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_buf.strip():
                    username = name_buf.strip()[:16]
                elif event.key == pygame.K_BACKSPACE:
                    name_buf = name_buf[:-1]
                elif event.unicode and event.unicode.isprintable() and len(name_buf) < 16:
                    name_buf += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_QUIT.collidepoint(event.pos):
                    stt.save(cfg); pygame.quit(); sys.exit()
                elif BTN_PLAY.collidepoint(event.pos) and username:
                    pb = db.get_personal_best(username) if db_ok else 0
                    game  = Game(username, pb, cfg["snake_color"], cfg["grid"])
                    state = "game"
                elif BTN_BOARD.collidepoint(event.pos):
                    state = "leaderboard"
                elif BTN_SETT.collidepoint(event.pos):
                    state = "settings"

        # GAME
        elif state == "game":
            if event.type == Game.STEP_EVENT:
                game.step()
                if game.done:
                    last_result = {
                        "score":         game.score,
                        "level":         game.level,
                        "reason":        game.reason,
                        "personal_best": game.personal_best,
                    }
                    if db_ok:
                        db.save_session(username, game.score, game.level)
                        # обновляем personal best если побили
                        new_pb = db.get_personal_best(username)
                        last_result["personal_best"] = new_pb
                    state = "game_over"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    pygame.time.set_timer(Game.STEP_EVENT, 0)
                else:
                    game.handle_key(event.key)

        # GAME OVER
        elif state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_RETRY.collidepoint(event.pos):
                    pb    = db.get_personal_best(username) if db_ok else 0
                    game  = Game(username, pb, cfg["snake_color"], cfg["grid"])
                    state = "game"
                elif BTN_MMENU.collidepoint(event.pos):
                    state = "menu"

        # LEADERBOARD
        elif state == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and BTN_BACK.collidepoint(event.pos):
                state = "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"

        # SETTINGS
        elif state == "settings":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                stt.save(cfg); state = "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_SAVE.collidepoint(event.pos):
                    stt.save(cfg); state = "menu"
                elif BTN_GRID.collidepoint(event.pos):
                    cfg["grid"] = not cfg["grid"]
                elif BTN_SOUND.collidepoint(event.pos):
                    cfg["sound"] = not cfg["sound"]
                else:
                    for name, (rect, rgb) in COLOR_BTNS.items():
                        if rect.collidepoint(event.pos):
                            cfg["snake_color"] = list(rgb)

    # DRAW
    if state == "menu":
        screen_menu(mouse)
    elif state == "game":
        screen_game()
    elif state == "game_over":
        screen_game_over(mouse)
    elif state == "leaderboard":
        screen_leaderboard(mouse)
    elif state == "settings":
        screen_settings(mouse)

    pygame.display.flip()
