import random
from player import *

game_phase = 'how_many_players'
position = ''
char_name = ''
dice_roll_result = ''
cp_index = 0
players_in_game = []
current_player = ''


# def turn():
#     if 'there are anothers players?':
#         if 'yes':
#             if 'do you want to meet him ?':
#                 if 'yes':
#                     if 'attack of special ability?':
#                         if 'choose gifht style might or magic':
#                             if 'normal':
#                                 'normal fight()'
#                                 'end turn()'
#                             else:
#                                 'magic fight()'
#                                 'end turn()'
#                     else:
#                         'use special ability on player()'
#                     'end turn()'
#     'ecounter the space()'
#     if 'card to draw?':
#         if 'yes':
#             'draw a card()'
#             'card ecounter()'
#         else:
#             'card ecounter()'
#     else:
#         'follow instruction on space()'

def move_dice_roll(current_player):
    global game_phase, dice_roll_result
    print(f'babababa: {players_in_game[0].character.title}')
    print(current_player)
    dice_roll_result = current_player.dice_roll_single()
    print(f'move_dice_roll: {dice_roll_result}')
    return current_player, game_phase, dice_roll_result
    # if game_phase == 1:
    #     throw = current_player.throw_1c()
    #     print(f'move_dice_roll: {throw}')
    #     # current_player.throw = throw
    #     # game_phase = 2
    #     return current_player, game_phase, throw


def m_forward(current_player):
    current_player.move_forward(dice_roll_result)
    position = current_player.position.name
    print(position)
    return position


class Game():
    def __init__(self):
        self.game_phase = 'how_many_players'
        self.position = ''
        self.char_name = ''
        self.dice_roll_result = ''
        self.cp_index = 0
        self.players_in_game = []
        self.current_player = ''

    def move_dice_roll(self, current_player):
        # global game_phase, dice_roll_result
        print(f'babababa: {players_in_game[0].character.title}')
        print(current_player)
        self.dice_roll_result = current_player.dice_roll_single()
        print(f'move_dice_roll: {self.dice_roll_result}')
        return current_player, game_phase, dice_roll_result


    # def m_forward(self, current_player):
    #     self.current_player.move_forward(dice_roll_result)
    #     self.position = current_player.position.name
    #     print(position)
    #     return position
