import pygame
from pygame.locals import *
import time
import random
from Goose import Goose


class Tray:
    background_image_src = ""
    HEIGHT = 0
    WIDTH = 0
    background = None

    # Dice faces src
    dice_face1_src = "assets/dice_faces/face1.png"
    dice_face2_src = "assets/dice_faces/face2.png"
    dice_face3_src = "assets/dice_faces/face3.png"
    dice_face4_src = "assets/dice_faces/face4.png"
    dice_face5_src = "assets/dice_faces/face5.png"
    dice_face6_src = "assets/dice_faces/face6.png"

    dice_face1 = None
    dice_face2 = None
    dice_face3 = None
    dice_face4 = None
    dice_face5 = None
    dice_face6 = None

    dice_faces = None

    dices_pos = ((322, 243), (398, 243))

    # Grid

    # All player stuff
    players_sprite = pygame.sprite.Group()
    players = []
    player_count = 0
    players_start_positions = ((60, 25), (60, 55), (30, 25), (30, 55))
    players_colors = ((0, 0, 0), (255, 0, 0), (0, 82, 0), (0, 0, 85))
    player_radius = 13
    player_turn = 0
    players_grid = [0, 0, 0, 0]

    player1_possible_position = ((60, 25), (134, 25), (208, 25), (282, 25), (356, 25), (430, 25), (504, 25), (578, 25), (654, 25),
                                 (654, 98), (654, 170),
                                 (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0))

    window = None

    def __init__(self, background_image_src, width, height, player_count):
        self.HEIGHT = width
        self.WIDTH = height
        self.background_image_src = background_image_src
        self.player_count = player_count
        pygame.init()

    def create_window(self):
        self.window = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        pygame.display.set_caption("Jeu de l'oie")
        self.background = pygame.image.load(self.background_image_src).convert_alpha()
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        self.init_dices()

    def init_dices(self):
        self.dice_face1 = pygame.image.load(self.dice_face1_src).convert_alpha()
        self.dice_face2 = pygame.image.load(self.dice_face2_src).convert_alpha()
        self.dice_face3 = pygame.image.load(self.dice_face3_src).convert_alpha()
        self.dice_face4 = pygame.image.load(self.dice_face4_src).convert_alpha()
        self.dice_face5 = pygame.image.load(self.dice_face5_src).convert_alpha()
        self.dice_face6 = pygame.image.load(self.dice_face6_src).convert_alpha()

        self.dice_faces = (
            self.dice_face1, self.dice_face2, self.dice_face3, self.dice_face4, self.dice_face5, self.dice_face6)

    def init_players(self):
        for k in range(0, self.player_count):
            goose = Goose(self.players_colors[k], self.players_start_positions[k])
            self.players_sprite.add(goose)
            self.players.append(goose)
            self.players[k].init_sprite_positions()

    def launch_dices(self):
        dice1_number = random.randint(1, 6)
        dice2_number = random.randint(1, 6)
        to_forward = dice1_number + dice2_number
        # self.animate_launch_dices(dice1_number, dice2_number)
        self.forward_player(to_forward, self.player_turn)
        if self.player_turn >= 4:
            self.player_turn = 0
        else:
            self.player_turn += 1

    def forward_player(self, to_forward, player_turn):
        print(to_forward)
        for i in range(0, self.player_count):
            if i == player_turn and player_turn == 0:
                self.players[i].move(self.player1_possible_position[9 + self.players_grid[i]])
                self.players_grid[i] += to_forward

    def animate_launch_dices(self, dice1_number, dice2_number):
        wait_time = 0.1
        for k in range(0, 3):
            for i in range(0, 6):
                dice1 = self.dice_faces[i]
                dice2 = self.dice_faces[i]
                self.window.blit(dice1, self.dices_pos[0])
                self.window.blit(dice2, self.dices_pos[1])
                pygame.display.flip()
                time.sleep(wait_time)
                pass
            pass

        for i in range(0, 6):
            dice1 = self.dice_faces[i]
            dice2 = self.dice_faces[i]
            if i <= dice1_number:
                self.window.blit(dice1, self.dices_pos[0])
            if i <= dice2_number:
                self.window.blit(dice2, self.dices_pos[1])
            pygame.display.flip()
            time.sleep(wait_time)
        time.sleep(1.5)

    def draw_players(self):
        self.players_sprite.update()
        self.window.blit(self.background, (0, 0))
        self.players_sprite.draw(self.window)
        pygame.display.flip()
