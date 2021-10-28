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
        self.pvp_player = ''
        self.battle_modificator = 0
        self.enemy_strength = 0
        self.battle_counter = 0
        self.pvp_winner = ''
        self.pvp_loser = ''



        self.backward_move_index = ''
        self.forward_move_index = ''

        # self.current_player_battle_strength = ''

        self.display = {'position': '', 'move_backward': {'name': '', 'cards_to_draw': ''},
                        'move_forward': {'name': '',
                                         'cards_to_draw': ''},
                        'card': '', 'enemy_strength': '',
                        'player_strength': '', 'battle_result': '', 'life': '',
                        'players_position': {}, 'bmi': self.backward_move_index, 'fmi': self.forward_move_index,
                        'game_field': cards.ow_game_field, 'players_position_fwd': {}, 'players_position_bkw': {},
                        'players_in_game': self.players_in_game, 'game': self}

    def display_ref(self):
        self.display['game'] = self
        self.display['players_in_game'] = self.players_in_game
        self.display['position'] = self.current_player.position
        self.display['fmi'] = self.forward_move_index
        self.display['bmi'] = self.backward_move_index
        if self.game_subphase == 'EWE_Battle':
            self.display['enemy_strength'] = tal_game.current_adv_card.strength + self.battle_modificator
        else:
            self.display['enemy_strength'] = self.enemy_strength

        try:
            self.display['player_strength'] = self.current_player.strength
        except AttributeError:
            pass
        if self.current_player.battle_strength > 0:
            self.display['player_strength'] = self.current_player.battle_strength
        else:
            pass
        if self.current_player.life != '':
            self.display['life'] = self.current_player.life

        # if len(self.current_player.strength_trophy) > 0:
        #     self.display['strength_trophy'] = self.current_player.strength_trophy

        try:
            for player in self.players_in_game:
                if player != self.current_player:
                    if player.position == cards.ow_game_field[self.backward_move_index]:
                        self.display['players_position_bkw'][player.character.title] = player.position
                    if player.position == cards.ow_game_field[self.forward_move_index]:
                        self.display['players_position_fwd'][player.character.title] = player.position
                    else:
                        self.display['players_position_bkw'] = {}
                        self.display['players_position_fwd'] = {}
        except:
            pass

        try:
            self.display['card'] = self.current_adv_card
        except AttributeError:
            pass
        if self.current_player.dice_roll_result != '':
            try:
                self.backward_move_index = cards.ow_game_field.index(
                    self.current_player.position) - self.current_player.dice_roll_result
            except (TypeError, ValueError):
                pass

            try:
                self.forward_move_index = cards.ow_game_field.index(
                    self.current_player.position) + self.current_player.dice_roll_result - len(cards.ow_game_field)
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

            try:
                for player in self.players_in_game:
                    self.display['players_position'][player] = player.position
            except:
                pass

    def change_subphase(self, input):
        self.game_subphase = input
        self.display_ref()

    def dice_roll_single(self):
        # result = random.randint(1, 6)
        result = 1
        self.dice_roll_result = result
        print(f'wynik rzuty kostka {self.dice_roll_result}')
        # self.display_ref()
        return result

    def dice_roll_double(self):
        result = random.randint(2, 12)
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
        self.battle_modificator = 0
        self.current_player.battle_strength = 0
        self.current_player.dice_roll_result = 0
        self.display['battle_result'] = ''
        self.display['strength_trophy'] = ''
        self.current_player = self.players_in_game[self.cp_index]
        self.pvp_winner = ''
        self.pvp_loser = ''


        self.current_player.battle_modificator = 0
        self.current_player.battle_strength = 0
        if self.pvp_player != '':
            self.pvp_player.battle_modifiactor = 0
            self.pvp_player.battle_strength = 0
        self.battle_counter = 0

        self.display_ref()

    def check_player_position(self):
        for p in self.players_in_game:
            if p != self.current_player:
                if p.position == self.current_player.position:
                    print('true')
                    return True
                else:
                    print('check false')
                    return False

    def check_if_space_is_special(self):
        if self.current_player.position.special:
            return True
        else:
            return False

    # def e_battle_strength(self):
    #     self.battle_modificator = self.current_player.dice_roll_single()
    #     self.enemy_strength = self.current_adv_card.strength + self.battle_modificator
    #     self.display_ref()

    def e_battle_strength(self):
        self.battle_modificator = self.dice_roll_single()
        self.enemy_strength = self.current_adv_card.strength + self.battle_modificator
        self.display_ref()

    def ecounter_with_enemy(self):
        if self.game_subphase != 'EWE_after_battle':
            if self.current_player.battle_strength > self.enemy_strength:
                self.current_player.strength_trophy.append(self.current_adv_card)
                self.display['battle_result'] = 'player_won'

            elif self.current_player.battle_strength < self.enemy_strength:
                self.current_player.life -= 1
                self.display['battle_result'] = 'player_lost'
            else:
                self.display['battle_result'] = 'draw'
            self.game_phase = 'EWE_after_battle'
            print(self.game_subphase)
            return self.game_subphase

        # if self.game_subphase

    def draw_card(self):
        card = random.choice(self.adventure_cards)
        card.position = self.current_player.position
        self.adventure_cards.remove(card)
        self.current_adv_card = card
        return card

    def game_is_on(self):
        return True

    ############# EWE ######################################

    def ewe_evade(self):
        while self.game_subphase == 'EWE_Evade':
            if request.form.get('yes_EWE_Evade'):
                print('bbbb')

    ########## ETS #####################################

    def draw(self):
        self.draw_card()
        self.game_subphase = 'ETS_draw'
        self.display_ref()
        if self.game_subphase == 'ETS_draw':
            if self.current_adv_card.type == 'enemy':
                self.game_phase = 'EWE'
                self.display_ref()

    # ################# PVP ##############################
    #
    def pvp_result(self):
        if self.current_player.battle_strength  > self.pvp_player.battle_strength or self.current_player.battle_craft  > self.pvp_player.battle_craft:
            self.pvp_winner = self.current_player
            self.pvp_loser = self.pvp_player
        elif self.current_player.battle_strength < self.pvp_player.battle_strength or self.current_player.battle_craft < self.pvp_player.battle_craft :
            self.pvp_winner = self.pvp_player
            self.pvp_loser = self.current_player
        else:
            self.pvp_winner = 'draw'

    def pvp_use_defence_item(self):
        print("defence is used")
        self.dice_roll_single()
        for item in self.pvp_loser.defence_items:
            if item == 'armor':
                print('using armor')
                if self.dice_roll_result >= 4:
                    return True
                else:
                    print('life lost')
                    self.pvp_loser.life -= 1
                    return False
            elif item == 'shield':
                print('using shield')
                if self.dice_roll_result >= 5:
                    return True
                else:
                    print('life lost')
                    self.pvp_loser.life -= 1
                    return False
            else:
                print('using helmet')
                if self.dice_roll_result >= 6:
                    return True
                else:
                    print('life lost')
                    self.pvp_loser.life -= 1
                    return False
        # self.end_turn()





tal_game = Game()
