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
        self.game_subphase = ''
        self.position = ''
        self.char_name = ''
        self.dice_roll_result = ''
        self.cp_index = 0
        self.players_in_game = []

        self.adventure_cards = AdventureCard.query.all()
        self.used_adventures_cards = []
        self.current_adventures_cards = []
        self.current_adv_card = ''
        self.current_player = ''

        self.printed()


    def printed(self):
        print(f'printed phase {self.game_phase} subphase {self.game_subphase}')


    def dice_roll_single(self):
        result = random.randint(1, 6)
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
        self.game_phase = 'movement_dice_roll'
        self.game_subphase = ''
        self.current_player = self.players_in_game[self.cp_index]

    def check_player_position(self):
        for p in self.players_in_game:
            if p != self.current_player:
                if p.position == self.current_player.position:
                    # print('true')
                    print(p.character.title)
                    return True
                else:
                    return False

    def check_if_space_is_special(self):
        if self.current_player.position.special:
            return True
        else:
            return False
        # print(self.current_player.position.name)
        # print(self.current_player.position.special)



    # def ecounter_with_enemy(self):
    #     if self.current_player_battle_strength > self.enemy_strength:
    #         print('player won')
    #     elif self.current_player_battle_strength > self.enemy_strength:
    #         print('player lost')
    #     else:
    #         print('draw')
    #     self.end_turn()


        # print(self.current_player.position.name)
        # print(self.current_player.position.special)

    def draw_card(self):
        card = random.choice(self.adventure_cards)
        card.position = self.current_player.position
        self.adventure_cards.remove(card)
        self.current_adv_card = card
        return card

    def ecounter_with_enemy(self, es, ps):

        self.current_player_battle_strength = es
        self.enemy_strength = ps
        print(f'zycie gracza {self.current_player.character.life}')
        if self.current_player_battle_strength > self.enemy_strength:
            print('player won')
        elif self.current_player_battle_strength > self.enemy_strength:
            self.current_player.character.life -= 1
            print('player lost')
        else:
            print('draw')
        self.end_turn()

    def game_is_on(self):
        return True

    def how_many_players(self, a):
        a=a
        # a = int(request.form['p'])
        for player in range(1, a + 1):
            player = Player()
            player.choose_character_random()
            player.name = f'player{player}'
            self.players_in_game.append(player)

        self.current_player = self.players_in_game[self.cp_index]

        if len(self.current_player.character.b4mov_spells) > 0:
            self.game_phase = 'b4mov_spells'
        else:
            self.game_phase = 'movement_dice_roll'
