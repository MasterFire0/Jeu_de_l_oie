from tray import Tray
import pygame
from pygame.locals import *

run = True
clock = pygame.time.Clock()


def main():

    """
    while True:
        player_count = input("Combien de joueurs participent ? (2-3-4)\n")
        if player_count == "2" or player_count == "3" or player_count == "4":
            break
        else:
            print("Entrée incorrect")
            continue
    """
    player_count = 4

    tray = Tray("assets/tray.png", 720, 540, int(player_count))
    tray.create_window()
    tray.init_players()
    while True:
        if not run:
            break
        tray.draw_players()
        check_pygame_events(tray)
        clock.tick(30)
        continue


def check_pygame_events(tray):
    for event in pygame.event.get():
        if event.type == QUIT:
            global run
            run = False
            pass
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                tray.launch_dices()


if __name__ == '__main__':
    main()
