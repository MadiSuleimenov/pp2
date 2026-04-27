import pygame, sys
from datetime import datetime
from tools import pencil_draw, draw_shape, flood_fill

pygame.init()

# Constants
W, H      = 900, 640
TOOLBAR   = 85
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
GRAY      = (210, 210, 210)
BLUE      = (60, 120, 220)

PALETTE = [
    BLACK, (255,0,0), (255,140,0), (255,220,0),
    (0,200,0), (0,160,220), (0,0,255), (160,0,210),
    (255,105,180), (139,69,19), (255,255,255),
]
TOOLS = ["pencil","line","rectangle","circle",
         "square","right_triangle","equilateral_triangle","rhombus",
         "fill","text","eraser"]
SIZES = {1: 2, 2: 5, 3: 10}

# Setup
win    = pygame.display.set_mode((W, H))
canvas = pygame.Surface((W, H - TOOLBAR))
canvas.fill(WHITE)
pygame.display.set_caption("Paint – TSIS 2")

font    = pygame.font.SysFont("Arial", 14, bold=True)
tfont   = pygame.font.SysFont("Arial", 22)

# State
color      = BLACK
tool       = "pencil"
size_lvl   = 2

drawing    = False
start      = None
prev       = None
snap       = None       # canvas snapshot for line preview

text_on    = False
text_pos   = None
text_buf   = ""
text_snap  = None

# UI rects
pal_rects = [(pygame.Rect(10 + i*30, 6, 26, 26), c) for i, c in enumerate(PALETTE)]

# Tool buttons: 2 rows of up to 6
tool_rects = {}
for i, t in enumerate(TOOLS):
    x = 10 + (i % 6) * 80
    y = 38 + (i // 6) * 24
    tool_rects[t] = pygame.Rect(x, y, 76, 20)

# Size buttons
size_rects = {lvl: pygame.Rect(W - 105 + (lvl-1)*34, 8, 30, 18) for lvl in (1,2,3)}


# Helpers
def in_canvas(pos):
    return pos[1] >= TOOLBAR

def to_canvas(pos):
    return (pos[0], pos[1] - TOOLBAR)

def save():
    name = f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(canvas, name)
    print("Saved:", name)

def draw_ui():
    pygame.draw.rect(win, (225, 225, 230), (0, 0, W, TOOLBAR))
    pygame.draw.line(win, (170,170,175), (0, TOOLBAR-1), (W, TOOLBAR-1))

    # Palette
    for r, c in pal_rects:
        pygame.draw.rect(win, c, r)
        pygame.draw.rect(win, BLUE if c == color else (100,100,100), r, 2 if c == color else 1)

    # Tool buttons
    for t, r in tool_rects.items():
        active = t == tool
        pygame.draw.rect(win, BLUE if active else GRAY, r, border_radius=3)
        lbl = font.render(t.replace("_"," "), True, WHITE if active else BLACK)
        win.blit(lbl, (r.x + 3, r.y + (r.h - lbl.get_height())//2))

    # Size buttons
    win.blit(font.render("Size:", True, BLACK), (W-112, 10))
    for lvl, r in size_rects.items():
        active = lvl == size_lvl
        pygame.draw.rect(win, BLUE if active else GRAY, r, border_radius=3)
        lbl = font.render(str(lvl), True, WHITE if active else BLACK)
        win.blit(lbl, (r.centerx - lbl.get_width()//2, r.centery - lbl.get_height()//2))

    # Hint
    hint = font.render("1/2/3: size   Ctrl+S: save   Enter: confirm text   Esc: cancel", True, (120,120,130))
    win.blit(hint, (W - hint.get_width() - 6, TOOLBAR - 16))


# Main loop
clock = pygame.time.Clock()
while True:
    # Draw
    win.blit(canvas, (0, TOOLBAR))
    draw_ui()

    # Text preview on win only
    if text_on and text_pos:
        preview = tfont.render(text_buf + "|", True, color)
        win.blit(preview, (text_pos[0], text_pos[1] + TOOLBAR))

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # Keys
        elif event.type == pygame.KEYDOWN:
            if text_on:
                if event.key == pygame.K_RETURN:
                    if text_buf:
                        canvas.blit(tfont.render(text_buf, True, color), text_pos)
                    text_on = False; text_buf = ""; text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    if text_snap: canvas.blit(text_snap, (0,0))
                    text_on = False; text_buf = ""; text_pos = None; text_snap = None
                elif event.key == pygame.K_BACKSPACE:
                    text_buf = text_buf[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_buf += event.unicode
            else:
                if event.key == pygame.K_1:   size_lvl = 1
                elif event.key == pygame.K_2: size_lvl = 2
                elif event.key == pygame.K_3: size_lvl = 3
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save()
                elif event.key == pygame.K_ESCAPE:
                    if snap: canvas.blit(snap, (0,0))
                    drawing = False; snap = None

        # Mouse Down
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            clicked = False

            for r, c in pal_rects:
                if r.collidepoint(pos): color = c; clicked = True; break

            if not clicked:
                for t, r in tool_rects.items():
                    if r.collidepoint(pos): tool = t; clicked = True; break

            if not clicked:
                for lvl, r in size_rects.items():
                    if r.collidepoint(pos): size_lvl = lvl; clicked = True; break

            if not clicked and in_canvas(pos):
                cp = to_canvas(pos)
                sz = SIZES[size_lvl]

                if tool == "fill":
                    flood_fill(canvas, cp, color)

                elif tool == "text":
                    if text_snap: canvas.blit(text_snap, (0,0))
                    text_snap = canvas.copy()
                    text_pos  = cp
                    text_buf  = ""
                    text_on   = True

                else:
                    drawing = True
                    start   = cp
                    prev    = cp
                    if tool == "line":
                        snap = canvas.copy()

        # Mouse Up
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and in_canvas(event.pos):
                cp = to_canvas(event.pos)
                sz = SIZES[size_lvl]

                if tool == "line":
                    if snap: canvas.blit(snap, (0,0))
                    pygame.draw.line(canvas, color, start, cp, sz)
                    snap = None

                elif tool not in ("pencil", "eraser"):
                    draw_shape(canvas, tool, start, cp, color, sz)

            drawing = False; prev = None

        # Mouse Motion
        elif event.type == pygame.MOUSEMOTION and drawing:
            if in_canvas(event.pos):
                cp = to_canvas(event.pos)
                sz = SIZES[size_lvl]

                if tool == "pencil":
                    pencil_draw(canvas, prev, cp, color, sz)
                    prev = cp

                elif tool == "eraser":
                    pencil_draw(canvas, prev, cp, WHITE, sz * 4)
                    prev = cp

                elif tool == "line":
                    if snap: canvas.blit(snap, (0,0))
                    pygame.draw.line(canvas, color, start, cp, sz)
