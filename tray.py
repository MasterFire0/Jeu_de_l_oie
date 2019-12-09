import pygame
from pygame.locals import *
import random
import time
from goose import Goose
from constants import *


class Tray:
    background_image_src = ""
    HEIGHT = 0
    WIDTH = 0
    background = None

    # Dice faces
    dice_face1 = None
    dice_face2 = None
    dice_face3 = None
    dice_face4 = None
    dice_face5 = None
    dice_face6 = None

    dice_faces = None

    dices_pos = ((322, 243), (398, 243))

    # All player stuff
    players_sprite = pygame.sprite.Group()
    players = []
    player_count = 0
    player_turn = 0
    players_grid = [1, 1, 1, 1]

    window = None

    def __init__(self, background_image_src, width, height, player_count):
        self.run = True
        self.HEIGHT = width
        self.WIDTH = height
        self.background_image_src = background_image_src
        self.player_count = player_count
        self.first_space = True
        self.fast_dice_animation = False
        pygame.init()
        self.create_window()

    def update(self):
        self.check_pygame_events()
        self.draw_players()

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False
                pass
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.first_space:
                        self.first_space = False
                        self.fast_dice_animation = False
                        self.launch_dices()
                    else:
                        self.fast_dice_animation = True

    def create_window(self):
        self.window = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        pygame.display.set_caption("Jeu de l'oie")
        self.background = pygame.image.load(self.background_image_src).convert_alpha()
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        self.init_players()
        self.init_dices()

    def init_dices(self):
        self.dice_face1 = pygame.image.load(dice_face1_src).convert_alpha()
        self.dice_face2 = pygame.image.load(dice_face2_src).convert_alpha()
        self.dice_face3 = pygame.image.load(dice_face3_src).convert_alpha()
        self.dice_face4 = pygame.image.load(dice_face4_src).convert_alpha()
        self.dice_face5 = pygame.image.load(dice_face5_src).convert_alpha()
        self.dice_face6 = pygame.image.load(dice_face6_src).convert_alpha()

        self.dice_faces = (
            self.dice_face1, self.dice_face2, self.dice_face3, self.dice_face4, self.dice_face5, self.dice_face6)

    def init_players(self):
        for k in range(0, self.player_count):
            goose = Goose(players_colors[k], players_start_positions[k])
            self.players_sprite.add(goose)
            self.players.append(goose)
            self.players[k].init_sprite_positions()

    def launch_dices(self):
        dice1_number = random.randint(1, 6)
        dice2_number = random.randint(1, 6)
        to_forward = dice1_number + dice2_number
        self.animate_launch_dices(dice1_number, dice2_number)
        self.forward_player(to_forward, self.player_turn)
        if self.player_turn >= 3:
            self.player_turn = 0
        else:
            self.player_turn += 1

    def forward_player(self, to_forward, player_turn):
        for i in range(0, self.player_count):
            if i == player_turn:
                self.players[i].move(players_possibles_positions[i][to_forward + self.players_grid[i]])
                self.players_grid[i] += to_forward

    def animate_launch_dices(self, dice1_number, dice2_number):
        wait_time = 0.1
        for k in range(0, 4):
            for i in range(0, 6):
                if self.fast_dice_animation:
                    self.window.blit(self.dice_faces[dice1_number - 1], self.dices_pos[0])
                    self.window.blit(self.dice_faces[dice2_number - 1], self.dices_pos[1])
                    pygame.display.flip()
                    break
                dice1 = self.dice_faces[i]
                dice2 = self.dice_faces[i]
                if k == 3:
                    if i <= dice1_number:
                        self.window.blit(dice1, self.dices_pos[0])
                    if i <= dice2_number:
                        self.window.blit(dice2, self.dices_pos[1])
                else:
                    self.window.blit(dice1, self.dices_pos[0])
                    self.window.blit(dice2, self.dices_pos[1])
                pygame.display.flip()
                self.check_pygame_events()
                time.sleep(wait_time)
                pass
            if self.fast_dice_animation:
                self.fast_dice_animation = False
                break
            pass
        time.sleep(1.5)
        self.first_space = True

    def draw_players(self):
        self.players_sprite.update()
        self.window.blit(self.background, (0, 0))
        self.players_sprite.draw(self.window)
        pygame.display.flip()
