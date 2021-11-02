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
        self.strength = 0
        self.life = 0
        self.craft = 0
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


        self.max_carry_items = 4
        self.max_spells = 0






    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        self.strength = char.strenght
        self.life = char.life
        self.gold = char.gold
        self.fate = char.fate
        self.craft = char.craft
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
            self.battle_modificator = self.dice_roll_single()
            self.battle_strength = self.strength + self.battle_modificator
            for item in self.items:
                if item.is_weapon == True:
                    self.battle_strength += 1
        if tal_game.game_subphase == 'EWP_craft' or (tal_game.game_subphase == 'EWE_Battle' and tal_game.current_adv_card.strength == None):
            self.battle_modificator = self.dice_roll_single()
            self.battle_craft = self.craft + self.battle_modificator


        # if tal_game.game_subphase == 'EWE_Battle' and tal_game.current_adv_card.strength != None:




