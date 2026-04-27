import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer – TSIS 3")
clock = pygame.time.Clock()

import ui
import racer
from persistence import load_settings, save_settings, load_leaderboard, add_score

ui.setup(screen)
racer.load_assets()

settings = load_settings()


def play_menu_music():
    if racer.drive_sound: racer.drive_sound.stop()
    if racer.menu_sound and settings["sound"]: racer.menu_sound.play(-1)

def play_drive_music():
    if racer.menu_sound: racer.menu_sound.stop()
    if racer.drive_sound and settings["sound"]: racer.drive_sound.play(-1)


state       = "menu"
player_name = ""
name_buf    = ""
game        = None
last        = {"score": 0, "distance": 0, "coins": 0, "reason": ""}

play_menu_music()

while True:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_settings(settings)
            pygame.quit()
            sys.exit()

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = ui.menu_click(event.pos)
                if action == "play":
                    state = "name"; name_buf = ""
                elif action == "leaderboard":
                    state = "leaderboard"
                elif action == "settings":
                    state = "settings"
                elif action == "quit":
                    save_settings(settings); pygame.quit(); sys.exit()

        elif state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_buf.strip():
                    player_name = name_buf.strip()[:12]
                    game  = racer.make_game(settings)
                    play_drive_music()
                    state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    name_buf = name_buf[:-1]
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif event.unicode and event.unicode.isprintable() and len(name_buf) < 12:
                    name_buf += event.unicode

        elif state == "game":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"; play_menu_music()

        elif state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = ui.game_over_click(event.pos)
                if action == "retry":
                    state = "name"; name_buf = player_name
                elif action == "menu":
                    state = "menu"

        elif state == "leaderboard":
            if (event.type == pygame.MOUSEBUTTONDOWN and ui.BTN_BACK_BOARD.collidepoint(event.pos)
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                state = "menu"

        elif state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = ui.settings_click(event.pos, settings)
                if result == "back":
                    save_settings(settings); state = "menu"
                elif result == "sound_changed":
                    save_settings(settings)
                    if not settings["sound"]:
                        if racer.drive_sound: racer.drive_sound.stop()
                        if racer.menu_sound:  racer.menu_sound.stop()
                    else:
                        play_menu_music()
                elif result == "changed":
                    save_settings(settings)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings); state = "menu"

    if state == "menu":
        ui.screen_menu()
    elif state == "name":
        ui.screen_name(name_buf)
    elif state == "game":
        racer.update_game(game, dt, settings)
        racer.draw_game(game, screen)
        if game["done"] or game["distance"] >= 2000:
            last = {"score": game["score"], "distance": game["distance"],
                    "coins": game["coins_n"], "reason": game.get("reason", "")}
            add_score(player_name, last["score"], last["distance"], last["coins"])
            if racer.drive_sound: racer.drive_sound.stop()
            play_menu_music()
            state = "game_over"
    elif state == "game_over":
        ui.screen_game_over(last["score"], last["distance"], last["coins"], last.get("reason", ""))
    elif state == "leaderboard":
        ui.screen_leaderboard(load_leaderboard())
    elif state == "settings":
        ui.screen_settings(settings)

    pygame.display.flip()
