import random
# from player import Player
from cards import *
import cards


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


class Game:
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

        # self.current_player_battle_strength = ''

        self.display = {'name': '', 'game_phase': self.game_phase, 'dice_roll': '', 'position': '',
                        'game_subphase': '',
                        'move_backward': {'name': '',
                                          'cards_to_draw': ''},
                        'move_forward': {'name': '',
                                          'cards_to_draw': ''},
                        'card' : ''}

    def display_ref(self):
        self.display['name'] = self.current_player.character.title
        self.display['game_phase'] = self.game_phase
        self.display['dice_roll'] = self.current_player.dice_roll_result
        self.display['position'] = self.current_player.position.name
        self.display['game_subphase'] = self.game_subphase

        self.backward_move_index = ''
        self.forward_move_index = ''
        try:
            self.display['card'] = self.current_adv_card
        except AttributeError:
            pass
        if self.current_player.dice_roll_result != '':
            try:
                self.backward_move_index = cards.ow_game_field.index(self.current_player.position) - self.current_player.dice_roll_result
            except (TypeError, ValueError):
                pass

            try:
                self.forward_move_index = cards.ow_game_field.index(self.current_player.position) + self.current_player.dice_roll_result - len(cards.ow_game_field)
            except (TypeError, ValueError):
                pass


            try:
                self.display['move_backward']['name'] = cards.ow_game_field[self.backward_move_index].name
            except TypeError:
                pass
            try:
                self.display['move_backward']['cards_to_draw'] = cards.ow_game_field[
                    self.backward_move_index].card
            except TypeError:
                pass

            try:
                self.display['move_forward']['name'] = cards.ow_game_field[self.forward_move_index].name
            except TypeError:
                pass

            try:
                self.display['move_forward']['cards_to_draw'] = cards.ow_game_field[self.forward_move_index].card
            except TypeError:
                pass


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
        self.display_ref()

    def check_player_position(self):
        for p in self.players_in_game:
            if p != self.current_player:
                if p.position == self.current_player.position:
                    print('true')
                    print(p.character.title)
                    return True
                else:
                    print('check false')
                    return False
        # return False

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

    # def how_many_players(self, a):
    #     # a=a
    #     for player in range(1, a + 1):
    #         player = Player()
    #         player.choose_character_random()
    #         player.name = f'player{player}'
    #         self.players_in_game.append(player)
    #
    #     self.current_player = self.players_in_game[self.cp_index]
    #
    #     if len(self.current_player.character.b4mov_spells) > 0:
    #         self.game_phase = 'b4mov_spells'
    #     else:
    #         self.game_phase = 'movement_dice_roll'
    #     self.display_ref()

    # def move_forward(self, dice_roll_result):
    #     if request.method == 'POST':
    #         if request.form.get('forward'):
    #             if IndexError:
    #                 self.position = self.display['position']
    #                 # self.game_phase= 3
    #
    #                 return self.position
    #
    # def move_backward(self, dice_roll_result):
    #     self.position = cards.ow_game_field[cards.ow_game_field.index(self.position) - dice_roll_result]
    #     return self.position

tal_game = Game()
