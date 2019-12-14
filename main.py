from tray import Tray
import pygame


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
    clock = pygame.time.Clock()
    while True:
        if not tray.run:
            break
        clock.tick(10)
        tray.update()
        continue


if __name__ == '__main__':
    main()
