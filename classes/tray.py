import pygame
from pygame.locals import *
import random
import time
from classes.goose import Goose
from imports.constants import *

BLACK = (0, 0, 0)


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

    trap_grids = ((4, 0), (8, 1), (10, 2), (15, 0), (19, 2), (23, 1), (25, 3), (29, 2), (33, 4), (35, 0), (37, 5))
    win_grid = 39

    window = None

    def __init__(self, background_image_src, width, height, player_count):
        self.run = True
        self.HEIGHT = width
        self.WIDTH = height
        self.background_image_src = background_image_src
        self.player_count = player_count
        self.first_space = True
        self.fast_dice_animation = False
        self.is_keyboard_deactivate = False
        pygame.init()
        self.font = pygame.font.Font(None, 40)
        self.default_font = pygame.font.Font(None, 40)
        self.text_to_render = None
        self.create_window()

    def update(self):
        self.check_pygame_events()
        self.draw_players()
        if self.text_to_render is not None:
            self.window.blit(self.text_to_render, (130, 255))
        pygame.display.flip()

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False
                pass
            if event.type == KEYDOWN and not self.is_keyboard_deactivate:
                if event.key == K_SPACE:
                    if self.first_space:
                        self.first_space = False
                        self.fast_dice_animation = False
                        self.launch_dices()
                    else:
                        self.fast_dice_animation = True

    def create_window(self):
        self.window = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        pygame.display.set_caption("Jeu de l’oie")
        self.background = pygame.image.load(self.background_image_src).convert_alpha()
        self.window.blit(self.background, (0, 0))
        self.init_players()
        self.init_dices()
        self.text_to_render = self.font.render("Appuyez sur espace pour lancer le dé.", 1, BLACK)
        pygame.display.flip()

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
            goose = Goose(players_colors[k], players_start_positions[k], k)
            self.players_sprite.add(goose)
            self.players.append(goose)
            self.players[k].init_sprite_positions()

    def launch_dices(self):
        if self.players[self.player_turn].is_trapped():
            self.text_to_render = self.font.render(
                "Le joueur " + str((self.player_turn + 1)) + " est bloqué et doit attendre.", 1, BLACK)
            self.first_space = True
            self.update()
        else:
            dice1_number = random.randint(1, 6)
            # dice2_number = random.randint(1, 6)
            to_forward = dice1_number
            self.animate_launch_dices(to_forward)
            self.forward_player(to_forward, self.player_turn)
        if self.player_turn >= 3:
            self.player_turn = 0
        else:
            self.player_turn += 1

    def forward_player(self, to_forward, player_turn):
        self.text_to_render = self.font.render(
            "Le joueur " + str((player_turn + 1)) + " avance de " + str(to_forward) + " case(s)", 1, BLACK)
        for k in range(to_forward):
            if self.check_win(self.players[player_turn], to_forward - k):
                return
            self.players[player_turn].move(
                players_possibles_positions[player_turn][k + self.players[player_turn].get_grid()])
            time.sleep(0.3)
            self.update()
        self.players[player_turn].add_grid(to_forward)
        self.detect_trap(self.players[player_turn].get_grid(), player_turn, to_forward)
        self.is_keyboard_deactivate = False

    def detect_trap(self, player_grid, player_turn, to_forward):
        for k in self.trap_grids:
            if k[0] == player_grid:
                if k[1] == 3 or k[1] == 5:
                    for player in self.players:
                        if player.is_trapped() and player.get_grid() == player_grid and not player == self.players[player_turn]:
                            player.set_trap(False)
                        self.trap_player(k[1], player_turn, to_forward)
                else:
                    self.trap_player(k[1], player_turn, to_forward)

    def backward_player(self, to_backward, player_turn):
        self.text_to_render = self.font.render(
            "Malus: Le joueur " + str((player_turn + 1)) + " recule de " + str(to_backward) + " case(s)", 1, BLACK)
        time.sleep(0.4)
        for k in range(to_backward):
            self.players[player_turn].move(
                players_possibles_positions[player_turn][-k + (self.players[player_turn].get_grid() - 2)])
            time.sleep(0.3)
            self.update()
        self.players[player_turn].remove_grid(to_backward)
        self.is_keyboard_deactivate = False

    def check_win(self, player, to_go):
        if player.get_grid() == self.win_grid:
            if to_go == 0:
                self.text_to_render = self.font.render("Félicitation, le joueur " + player.get_id() + " gagne !")
                self.update()
                self.run = False
            else:
                self.backward_player(to_go, player.get_id())
            return True

    def trap_player(self, trap, player_turn, previous_forward):
        if trap == 0:
            self.backward_player(3, player_turn)
            pass
        elif trap == 1:
            time.sleep(0.4)
            self.forward_player(3, player_turn)
            pass
        elif trap == 2:
            time.sleep(0.4)
            self.forward_player(previous_forward, player_turn)
            pass
        elif trap == 3:
            self.players[player_turn].set_trap(True)
            self.font = pygame.font.Font(None, 33)
            self.text_to_render = self.font.render(
                "Le joueur " + str((player_turn + 1)) + " est tombé dans le puit. Il est bloqué.", 1, BLACK)
            self.update()
            time.sleep(0.4)
            self.is_keyboard_deactivate = False
            pass
        elif trap == 4:
            time.sleep(0.4)
            self.players[player_turn].move(players_possibles_positions[player_turn][12])
            self.players[player_turn].set_grid(13)
            self.font = pygame.font.Font(None, 30)
            self.text_to_render = self.font.render(
                "Le joueur " + str((player_turn + 1)) + " est dans le labyrinthe. Il retourne à la case 11.", 1, BLACK)
            self.update()
            self.is_keyboard_deactivate = False
            pass
        elif trap == 5:
            self.players[player_turn].set_trap(True)
            time.sleep(0.4)
            self.text_to_render = self.font.render(
                "Le joueur " + str((player_turn + 1)) + " est en prison. Il est bloqué.", 1, BLACK)
            self.update()
            self.is_keyboard_deactivate = False
            pass

    def animate_launch_dices(self, dice1_number, dice2_number=None):
        wait_time = 0.1
        self.text_to_render = None
        self.font = self.default_font
        self.update()
        for k in range(0, 4):
            for i in range(0, 6):
                if self.fast_dice_animation:
                    self.window.blit(self.dice_faces[dice1_number - 1], self.dices_pos[0])
                    # self.window.blit(self.dice_faces[dice2_number - 1], self.dices_pos[1])
                    pygame.display.flip()
                    break
                dice1 = self.dice_faces[i]
                # dice2 = self.dice_faces[i]
                if k == 3:
                    if i <= dice1_number - 1:
                        self.window.blit(dice1, self.dices_pos[0])
                    # if i <= dice2_number:
                    # self.window.blit(dice2, self.dices_pos[1])
                else:
                    self.window.blit(dice1, self.dices_pos[0])
                    # self.window.blit(dice2, self.dices_pos[1])
                pygame.display.flip()
                self.check_pygame_events()
                time.sleep(wait_time)
                pass
            if self.fast_dice_animation:
                self.fast_dice_animation = False
                break
            pass
        time.sleep(1.5)
        self.is_keyboard_deactivate = True
        self.first_space = True

    def draw_players(self):
        self.players_sprite.update()
        self.window.blit(self.background, (0, 0))
        self.players_sprite.draw(self.window)
