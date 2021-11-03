from database import *
import cards
import random
from game2 import *
from poszukiwacze import *
# from gui2 import tal_game

class Player(Game):
    def __init__(self):
        super().__init__()
        # self.game = Game
        # self.tal_game=Game()
        self.character = ''
        self.base_strength = 0
        self.extra_strength = 0
        self.strength = self.base_strength + self.extra_strength
        self.life = 0
        self.base_craft = 0
        self.extra_craft = 0
        self.craft = self.base_craft + self.extra_craft

        self.gold = 1
        self.fate = 0
        # self.position = ''
        # self.name = ''
        # self.current_player = ''
        # self.throw = ''

        self.battle_modificator = 0
        self.battle_strength = self.strength
        self.battle_craft = self.craft
        self.strength_trophy = []
        self.craft_trophy = []
        self.battle_spells = []
        self.spells = []
        self.magic_fight = True
        self.skills_against_character = [2]

        self.defence_items = ['armor']
        self.attack_items = ['axe']
        self.items = []
        self.all_items = [self.defence_items + self.attack_items]


        self.max_carry_items = 10
        self.max_spells = 0




    def update_item_stats(self):
        i_str = 0
        i_crt = 0
        # print(f"i_crt: {i_crt}")
        for item in self.items:
            if item.is_special:
                if not item.is_weapon:
                    try:
                        # print(f"item strength:{item.strength}")
                        i_str += item.strength
                    except TypeError:
                        # print('nie poszło str')
                        pass
                    try:
                        # print(f"item craft:{item.craft}")
                        i_crt += item.craft
                    except TypeError:
                        # print('nie poszło craft')
                        pass
        # print(f"i_crt: {i_crt}")
        # self.extra_strength = i_str
        # self.extra_craft = i_crt
        # print(f"extra crt: {self.extra_craft }")
        self.strength = self.base_strength + i_str
        self.craft = self.base_craft +i_crt



    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        # self.strength = char.strenght
        self.base_strength = char.strenght
        self.strength = self.base_strength
        self.life = char.life
        self.gold = char.gold
        self.fate = char.fate
        # self.craft = char.craft
        self.base_craft = char.craft
        self.craft = self.base_craft
        for space in cards.ow_game_field:
            if space.name == char.start_position:
                self.position = space

        classes.remove(char)
        return char


    def move_forward(self, dice_roll_result):
        if request.method == 'POST':
            if request.form.get('forward'):
                if IndexError:
                    self.position = cards.ow_game_field[tal_game.forward_move_index]

                    return self.position

    def move_backward(self, dice_roll_result):
        self.position = cards.ow_game_field[tal_game.backward_move_index]
        return self.position

    def p_battle_power(self):

        if tal_game.game_subphase == 'EWP_Strength' or (tal_game.game_subphase == 'EWE_Battle' and tal_game.current_adv_card.strength != None):
            for item in self.items:
                if item.is_weapon == True:
                    print('uzywam broni')
                    self.battle_modificator = 1
            self.battle_modificator += self.dice_roll_single()
            self.battle_strength = self.strength + self.battle_modificator

        if tal_game.game_subphase == 'EWP_craft' or (tal_game.game_subphase == 'EWE_Battle' and tal_game.current_adv_card.strength == None):
            self.battle_modificator = self.dice_roll_single()
            self.battle_craft = self.craft + self.battle_modificator
        tal_game.battle_counter += 1


        # if tal_game.game_subphase == 'EWE_Battle' and tal_game.current_adv_card.strength != None:




