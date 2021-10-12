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

        self.display = {'name': '', 'game_phase': self.game_phase, 'dice_roll': '', 'position': '',
                        'game_subphase': '', 'move_option_1': {'name': '',
                                                               'cards_to_draw': ''}, 'move_option_2': {'name': '',
                                                                                                       'cards_to_draw': ''}}

    def display_ref(self):
        self.display['name'] = self.current_player.character.title
        self.display['game_phase'] = self.game_phase
        # print(f'zmieniam game_phase na {self.game_phase}')
        self.display['dice_roll'] = self.current_player.dice_roll_result
        print(f'zmieniam wynik rzutu na {self.current_player.dice_roll_result}')
        self.display['position'] = self.current_player.character.start_position
        self.display['game_subphase'] = self.game_subphase
        try:
            self.display['move_option_1']['name'] = cards.ow_game_field[
                cards.ow_game_field.index(
                    self.current_player.position) + self.current_player.dice_roll_result - len(
                    cards.ow_game_field)].name
        except TypeError:
            pass
        try:
            self.display['move_option_1']['cards_to_draw'] = cards.ow_game_field[
                cards.ow_game_field.index(
                    self.current_player.position) + self.current_player.dice_roll_result - len(
                    cards.ow_game_field)].card
        except TypeError:
            pass
        try:
            self.display['move_option_2']['name'] = cards.ow_game_field[
                cards.ow_game_field.index(
                    self.current_player.position) + self.current_player.dice_roll_result].name
        except TypeError:
            pass
        try:
            self.display['move_option_2']['cards_to_draw'] = cards.ow_game_field[
                cards.ow_game_field.index(
                    self.current_player.position) + self.current_player.dice_roll_result].card
        except TypeError:
            pass

        try:
            print(
                f"{cards.ow_game_field[cards.ow_game_field.index(self.current_player.position) + self.current_player.dice_roll_result - len(cards.ow_game_field)]}\n position {cards.ow_game_field.index(self.current_player.position) + self.current_player.dice_roll_result  - len(cards.ow_game_field)}")
        except:
            pass
        try:
            print(
                f"{cards.ow_game_field[cards.ow_game_field.index(self.current_player.position) + self.current_player.dice_roll_result]} \n  position {cards.ow_game_field.index(self.current_player.position) + self.current_player.dice_roll_result}")
        except:
            pass


        print(f' bbbbbb {len(cards.ow_game_field)}')


    def change_subphase(self, input):
        self.game_subphase = input
        self.display_ref()


    def dice_roll_single(self):
        result = random.randint(1, 6)
        self.dice_roll_result = result
        print(f'papapapa {self.dice_roll_result}')
        # self.display_ref()
        return result


    def dice_roll_double(self):
        result = random.randint(2, 12)
        # print(f' wynik rzutu: {result}')
        self.dice_roll_result = result
        self.display_ref()
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
        # a=a
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
        self.display_ref()
