import random
from player import *


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


class Game():
    def __init__(self):
        self.game_phase = 'how_many_players'
        self.position = ''
        self.char_name = ''
        self.dice_roll_result = ''
        self.cp_index = 0
        self.players_in_game = []
        self.current_player = ''


    def dice_roll_single(self):
        result = random.randint(1, 6)
        # print(f' wynik rzutu: {result}')
        # dice_roll_result = result
        self.dice_roll_result = result
        return result

    def dice_roll_double(self):
        result = random.randint(2, 12)
        # print(f' wynik rzutu: {result}')
        self.dice_roll_result = result
        return result

    def end_turn(self):
        if self.cp_index + 1 >= len(self.players_in_game):
            self.cp_index = 0
        else:
            self.cp_index += 1
        self.game_phase = 1
        self.current_player=self.players_in_game[self.cp_index]

    def check_player_position(self):
        for p in self.players_in_game:
            if  p != self.current_player:
                if p.position == self.current_player.position:
                    print('true')
                    print(p.character.title)
                else:
                    print('false')



