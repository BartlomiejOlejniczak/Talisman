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
        # self.position = ''
        # self.name = ''
        # self.current_player = ''
        # self.throw = ''
        self.battle_modificator = 0
        self.battle_strength = 0
        self.strength_trophy = []
        self.craft_trophy = []



    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        self.strength = char.strenght
        self.life = char.life
        # print(f'char strength is {char.strenght}')
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
                    # print(self.position.name)

                    return self.position

    def move_backward(self, dice_roll_result):
        self.position = cards.ow_game_field[tal_game.backward_move_index]
        # print(self.position.name)
        return self.position

    def p_battle_strength(self):
        self.battle_modificator = self.dice_roll_single()
        self.battle_strength = self.strength + self.battle_modificator
        # print(f'player battle strength: {self.battle_modificator}')



