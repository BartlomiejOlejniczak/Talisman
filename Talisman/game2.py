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
        self.cards_on_map = []
        self.current_adv_card = ''

        self.current_player = ''
        self.pvp_player = ''
        self.battle_modificator = 0
        self.enemy_power = 0
        # self.enemy_craft = 0
        self.battle_counter = 0
        self.pvp_winner = ''
        self.pvp_loser = ''
        self.battle_type = 'strength'

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

    def change_subphase(self, input):
        self.game_subphase = input
        self.display_ref()

    def dice_roll_single(self):
        result = random.randint(1, 6)
        # result = 1
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
        self.enemy_power = 0
        self.current_player.battle_strength = 0
        self.current_player.dice_roll_result = 0
        self.display['battle_result'] = ''
        self.display['strength_trophy'] = ''
        self.current_player = self.players_in_game[self.cp_index]
        self.pvp_winner = ''
        self.pvp_loser = ''
        self.battle_type = 'strength'

        self.current_player.battle_modificator = 0
        self.current_player.battle_strength = 0
        self.current_player.battle_craft = 0
        if self.pvp_player != '':
            self.pvp_player.battle_modifiactor = 0
            self.pvp_player.battle_strength = 0
            self.pvp_player.battle_craft = 0
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

######### ECOUNTER WITH ENEMY ###################

    def e_battle_power(self):
        self.battle_modificator = self.dice_roll_single()

        if self.current_adv_card.strength != None:
            self.enemy_power = self.current_adv_card.strength + self.battle_modificator
        else:
            print('craft power')
            self.enemy_power = self.current_adv_card.craft + self.battle_modificator
            print(f'{self.enemy_power}')
        self.battle_counter += 1
        self.display_ref()

    def ecounter_with_enemy(self):
        if self.game_subphase != 'EWE_after_battle':
            if self.current_adv_card.strength != None:
                if self.current_player.battle_strength > self.enemy_power:
                    self.move_card('EWE')
                    self.display['battle_result'] = 'player_won'

                elif self.current_player.battle_strength < self.enemy_power:
                    self.current_player.life -= 1
                    self.leave_card_on_map()
                    self.display['battle_result'] = 'player_lost'

                else:
                    self.leave_card_on_map()
                    self.display['battle_result'] = 'draw'

            else:
                if self.current_player.battle_craft > self.enemy_power:
                    self.move_card('EWE')
                    self.display['battle_result'] = 'player_won'

                elif self.current_player.battle_craft < self.enemy_power:
                    self.leave_card_on_map()
                    self.current_player.life -= 1
                    self.display['battle_result'] = 'player_lost'

                else:
                    self.leave_card_on_map()
                    self.display['battle_result'] = 'draw'

                    

            self.game_phase = 'EWE_after_battle'
            return self.game_subphase



        # if self.game_subphase

    def game_is_on(self):
        return True

    ############# EWE ######################################

    def ewe_evade(self):
        self.leave_card_on_map()
        self.end_turn()

    ########## ETS - ECOUNTER THE SPACE #####################################

    def draw_card(self):
        card = random.choice(self.adventure_cards)
        card.position = self.current_player.position
        self.adventure_cards.remove(card)
        self.current_adv_card = card
        return card

    def draw(self):
        self.draw_card()
        self.game_subphase = 'ETS_draw'
        self.display_ref()
        if self.game_subphase == 'ETS_draw':
            if self.current_adv_card.type == 'enemy':
                self.game_phase = 'EWE'
                self.display_ref()

    def check_item_carry(self):
        item = self.current_adv_card
        if len(self.current_player.items) < self.current_player.max_carry_items:
            self.current_player.items.append(item)
        else:
            self.game_subphase = 'ETS_drop_item'

    def leave_card_on_map(self):
        if self.current_adv_card not in self.cards_on_map:
            self.current_adv_card.position = self.current_player.position
            self.cards_on_map.append(self.current_adv_card)

    def move_card(self, *args):
        print('moving card pos')
        if self.current_adv_card in self.cards_on_map:
            self.cards_on_map.remove(self.current_adv_card)
        if 'EWE':
            if self.current_adv_card.craft != None:
                self.current_player.craft_trophy.append(self.current_adv_card)
            else:
                self.current_player.strength_trophy.append(self.current_adv_card)





    # ################# PVP ##############################
    #
    def pvp_result(self):
        if self.current_player.battle_strength > self.pvp_player.battle_strength or self.current_player.battle_craft > self.pvp_player.battle_craft:
            self.pvp_winner = self.current_player
            self.pvp_loser = self.pvp_player
        elif self.current_player.battle_strength < self.pvp_player.battle_strength or self.current_player.battle_craft < self.pvp_player.battle_craft:
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
                    # print('life lost')
                    self.pvp_loser.life -= 1
                    return False
            elif item == 'shield':
                print('using shield')
                if self.dice_roll_result >= 5:
                    return True
                else:
                    # print('life lost')
                    self.pvp_loser.life -= 1
                    return False
            else:
                print('using helmet')
                if self.dice_roll_result >= 6:
                    return True
                else:
                    # print('life lost')
                    self.pvp_loser.life -= 1
                    return False
        # self.end_turn()

    ########## DISPLAY ##############

    def display_ref(self):
        for player in self.players_in_game:
            player.update_item_stats()
        # print(f'karty na mapie: {self.cards_on_map}')
        # for card in self.cards_on_map:
        #     print(f'karta{card.title} \n pozycja: {card.position}')
        # print(f'current player items: {self.current_player.items}')

        self.display['game'] = self
        self.display['players_in_game'] = self.players_in_game
        self.display['position'] = self.current_player.position
        self.display['fmi'] = self.forward_move_index
        self.display['bmi'] = self.backward_move_index
        if self.game_subphase == 'EWE_Battle':
            if tal_game.current_adv_card.strength != None:
                self.display['enemy_strength'] = tal_game.current_adv_card.strength + self.battle_modificator
            else:
                self.display['enemy_strength'] = self.current_adv_card.craft + self.battle_modificator

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

    # def update_item_stats(self):
    #     for player in self.players_in_game:
    #         for item in player.items:
    #             if item.is_special:
    #                 if item.title == 'ring':
    #                     print(player)
    #                     print('ring')
    #                     player.strength = player.base_strength + 1
    #                     player.craft = player.base_craft + 1
    #                     print(player.strength)
    #                 if item.title == 'holy_grail':
    #                     print(player)
    #                     print('holy_grail')
    #                     player.craft = player.base_craft + 1
    #                     print(player.craft)


tal_game = Game()
