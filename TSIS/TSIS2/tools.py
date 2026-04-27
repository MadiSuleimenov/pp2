import pygame
from collections import deque

WHITE = (255, 255, 255)


def pencil_draw(surface, prev_pos, curr_pos, color, size):
    if prev_pos:
        pygame.draw.line(surface, color, prev_pos, curr_pos, size)
    else:
        pygame.draw.circle(surface, color, curr_pos, size // 2 + 1)


def draw_shape(surface, shape, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    if shape == "rectangle":
        r = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, r, size)

    elif shape == "circle":
        cx, cy = (x1+x2)//2, (y1+y2)//2
        r = max(abs(x2-x1), abs(y2-y1)) // 2
        pygame.draw.circle(surface, color, (cx, cy), r, size)

    elif shape == "square":
        side = min(abs(x2-x1), abs(y2-y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, color, pygame.Rect(sx, sy, side, side), size)

    elif shape == "right_triangle":
        pygame.draw.polygon(surface, color, [(x1,y1),(x1,y2),(x2,y2)], size)

    elif shape == "equilateral_triangle":
        h = int((3**0.5 / 2) * abs(x2-x1))
        tip_y = y1 - h if y2 < y1 else y1 + h
        pygame.draw.polygon(surface, color, [(x1,y1),(x2,y1),((x1+x2)//2, tip_y)], size)

    elif shape == "rhombus":
        cx, cy = (x1+x2)//2, (y1+y2)//2
        pygame.draw.polygon(surface, color, [(cx,y1),(x2,cy),(cx,y2),(x1,cy)], size)


def flood_fill(surface, pos, fill_color):
    x, y = pos
    w, h = surface.get_size()
    target = surface.get_at((x, y))[:3]
    if target == fill_color[:3]:
        return
    queue = deque([(x, y)])
    visited = {(x, y)}
    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != target:
            continue
        surface.set_at((cx, cy), fill_color)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
