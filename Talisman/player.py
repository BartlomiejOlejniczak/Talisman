from database import *
import cards
import random
from game import *
from poszukiwacze import *


class Player(Game):
    def __init__(self):
        super().__init__()
        # self.tal_game=Game()
        self.character = ''
        self.position = ''
        # self.name = ''
        # self.current_player = ''
        # self.throw = ''



    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        for space in cards.ow_game_field:
            if space.name == char.start_position:
                self.position = space

        classes.remove(char)
        return char



    def move_forward(self, dice_roll_result):
        if request.method == 'POST':
            if request.form.get('forward'):
                if IndexError:
                    self.position = cards.ow_game_field[
                        cards.ow_game_field.index(self.position) + dice_roll_result - len(cards.ow_game_field)]
                    return self.position

    def move_backward(self, dice_roll_result):
        self.position = cards.ow_game_field[cards.ow_game_field.index(self.position) - dice_roll_result]
        return self.position
