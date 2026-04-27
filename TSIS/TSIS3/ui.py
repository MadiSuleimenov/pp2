import pygame

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (220, 40,  40)
GREEN  = (40,  180, 40)
BLUE   = (50,  100, 220)
YELLOW = (230, 200, 0)
ORANGE = (230, 130, 0)
GRAY   = (180, 180, 180)
DGRAY  = (60,  60,  60)
DARK   = (20,  20,  30)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  100, 220),
    "green":  (50,  200, 80),
    "yellow": (230, 200, 0),
}

WIDTH, HEIGHT = 400, 600


def _init_fonts():
    global font, fsmall, fbig
    font   = pygame.font.SysFont("Verdana", 20)
    fsmall = pygame.font.SysFont("Verdana", 15)
    fbig   = pygame.font.SysFont("Verdana", 32, bold=True)


def setup(screen_surf):
    global screen
    screen = screen_surf
    _init_fonts()


def draw_btn(rect, text, color=BLUE, txt_color=WHITE):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    lbl = font.render(text, True, txt_color)
    screen.blit(lbl, (rect.centerx - lbl.get_width()  // 2,
                      rect.centery - lbl.get_height() // 2))


def draw_text(text, x, y, color=WHITE, f=None):
    f = f or font
    screen.blit(f.render(text, True, color), (x, y))


# Button rects
BTN_PLAY  = pygame.Rect(120, 220, 160, 44)
BTN_BOARD = pygame.Rect(120, 280, 160, 44)
BTN_SETT  = pygame.Rect(120, 340, 160, 44)
BTN_QUIT  = pygame.Rect(120, 400, 160, 44)

BTN_BACK_BOARD = pygame.Rect(140, 540, 120, 40)
BTN_BACK_SETT  = pygame.Rect(140, 540, 120, 40)

BTN_SOUND  = pygame.Rect(200, 140, 120, 36)
COLOR_BTNS = {
    name: pygame.Rect(15 + i * 93, 240, 85, 36)
    for i, name in enumerate(CAR_COLORS)
}
DIFF_BTNS = {
    d: pygame.Rect(15 + i * 127, 340, 118, 36)
    for i, d in enumerate(["easy", "normal", "hard"])
}

BTN_RETRY = pygame.Rect(50,  430, 130, 44)
BTN_MENU  = pygame.Rect(220, 430, 130, 44)


def screen_menu():
    screen.fill(DARK)
    for y in range(0, HEIGHT, 60):
        pygame.draw.rect(screen, (30, 30, 45), (0, y, WIDTH, 30))
    draw_text("RACER",  95,  110, YELLOW, fbig)
    draw_text("TSIS 3", 155, 160, GRAY,   fsmall)
    draw_btn(BTN_PLAY,  "Play",        GREEN)
    draw_btn(BTN_BOARD, "Leaderboard", BLUE)
    draw_btn(BTN_SETT,  "Settings",    DGRAY)
    draw_btn(BTN_QUIT,  "Quit",        RED)


def menu_click(pos):
    if BTN_PLAY.collidepoint(pos):  return "play"
    if BTN_BOARD.collidepoint(pos): return "leaderboard"
    if BTN_SETT.collidepoint(pos):  return "settings"
    if BTN_QUIT.collidepoint(pos):  return "quit"
    return None


def screen_name(buf):
    screen.fill(DARK)
    draw_text("Enter your name:", 95, 180, WHITE, font)
    box = pygame.Rect(80, 220, 240, 44)
    pygame.draw.rect(screen, DGRAY, box, border_radius=6)
    pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
    draw_text(buf + "|", 92, 232, WHITE, font)
    draw_text("Press ENTER to start", 80, 290, GRAY, fsmall)


def screen_leaderboard(board):
    screen.fill(DARK)
    draw_text("Top 10", 120, 30, YELLOW, fbig)
    cols    = [15, 50, 165, 255, 325]
    headers = ["#", "Name", "Score", "Dist", "Coins"]
    for h, cx in zip(headers, cols):
        draw_text(h, cx, 68, GRAY, fsmall)
    pygame.draw.line(screen, GRAY, (10, 88), (390, 88))

    for i, entry in enumerate(board):
        y   = 95 + i * 42
        col = YELLOW if i == 0 else (220, 180, 80) if i < 3 else WHITE
        vals = [f"{i+1}.", entry["name"][:9], str(entry["score"]),
                f"{entry['distance']}m", str(entry["coins"])]
        for v, cx in zip(vals, cols):
            draw_text(v, cx, y, col, fsmall)
        pygame.draw.line(screen, DGRAY, (10, y + 34), (390, y + 34))

    draw_btn(BTN_BACK_BOARD, "Back", DGRAY)


def screen_settings(s):
    screen.fill(DARK)
    draw_text("Settings", 120, 50, WHITE, fbig)

    draw_text("Sound:", 20, 148, GRAY, font)
    draw_btn(BTN_SOUND, "ON" if s["sound"] else "OFF", GREEN if s["sound"] else RED)

    draw_text("Car colour:", 20, 200, GRAY, font)
    for name, rect in COLOR_BTNS.items():
        pygame.draw.rect(screen, CAR_COLORS[name], rect, border_radius=6)
        if s["car_color"] == name:
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=6)
        draw_text(name, rect.x + 6, rect.y + 9, WHITE, fsmall)

    draw_text("Difficulty:", 20, 300, GRAY, font)
    dcols = {"easy": GREEN, "normal": BLUE, "hard": RED}
    for name, rect in DIFF_BTNS.items():
        sel = s["difficulty"] == name
        pygame.draw.rect(screen, dcols[name] if sel else DGRAY, rect, border_radius=6)
        pygame.draw.rect(screen, dcols[name], rect, 2, border_radius=6)
        draw_text(name, rect.x + 10, rect.y + 9, WHITE, fsmall)

    draw_btn(BTN_BACK_SETT, "Back", DGRAY)


def settings_click(pos, settings):
    if BTN_BACK_SETT.collidepoint(pos): return "back"
    if BTN_SOUND.collidepoint(pos):
        settings["sound"] = not settings["sound"]
        return "sound_changed"
    for name, rect in COLOR_BTNS.items():
        if rect.collidepoint(pos):
            settings["car_color"] = name
            return "changed"
    for name, rect in DIFF_BTNS.items():
        if rect.collidepoint(pos):
            settings["difficulty"] = name
            return "changed"
    return None


def screen_game_over(score, dist, coins, reason=""):
    screen.fill((60, 0, 0))
    draw_text("GAME OVER", 105, 100, RED, fbig)
    if reason:
        draw_text(reason, 200 - font.size(reason)[0]//2, 150, ORANGE, font)
    draw_text(f"Score    : {score}", 80, 220, WHITE, font)
    draw_text(f"Distance : {dist}m", 80, 255, WHITE, font)
    draw_text(f"Coins    : {coins}", 80, 290, WHITE, font)
    draw_btn(BTN_RETRY, "Retry", GREEN)
    draw_btn(BTN_MENU,  "Menu",  BLUE)


def game_over_click(pos):
    if BTN_RETRY.collidepoint(pos): return "retry"
    if BTN_MENU.collidepoint(pos):  return "menu"
    return None


def _draw_heart(surf, cx, cy, size, color):
    r = size // 2
    pygame.draw.circle(surf, color, (cx - r // 2, cy), r // 2)
    pygame.draw.circle(surf, color, (cx + r // 2, cy), r // 2)
    pygame.draw.polygon(surf, color, [(cx - r, cy), (cx + r, cy), (cx, cy + r + 2)])


def draw_hud(score, coins, distance, active_pu, pu_secs, shield, lives):
    bar = pygame.Surface((WIDTH, 66), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 175))
    screen.blit(bar, (0, 0))

    draw_text(f"Score:  {score}",     8,  3,  WHITE,  fsmall)
    draw_text(f"Coins:  {coins}",     8,  21, YELLOW, fsmall)
    draw_text(f"Dist:   {distance}m", 8,  42, WHITE,  fsmall)

    draw_text(f"Left: {max(0, 2000 - distance)}m", 155, 3, GRAY, fsmall)

    draw_text("Lives:", 155, 22, GRAY, fsmall)
    for i in range(3):
        _draw_heart(screen, 215 + i * 22, 30, 14, RED if i < lives else DGRAY)

    pu_col = {"nitro": ORANGE, "shield": BLUE, "repair": GREEN}
    if shield:
        draw_text("SHIELD", 298, 3, BLUE, fsmall)
    if active_pu == "nitro" and pu_secs > 0:
        draw_text(f"NITRO {pu_secs}s", 288, 22, ORANGE, fsmall)

    bar_w = min(int((distance / 2000) * WIDTH), WIDTH)
    pygame.draw.rect(screen, DGRAY, (0, 63, WIDTH, 4))
    pygame.draw.rect(screen, ORANGE if active_pu == "nitro" else GREEN, (0, 63, bar_w, 4))
