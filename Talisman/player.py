from database import *
import cards
import random
from game import *
from poszukiwacze import *


class Player():
    def __init__(self):
        self.character = ''
        self.position = ''
        self.name = ''
        # self.current_player = ''
        # self.throw = ''



    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        for space in cards.ow_game_field:
            if space.name == char.start_position:
                self.position = space
        # print(self.character.title)
        # print(self.position)
        # print(self.position.name)

        classes.remove(char)
        return char

    def dice_roll_single(self):
        result = random.randint(1, 6)
        print(f' wynik rzutu: {result}')
        # dice_roll_result = result
        return result

    def dice_roll_double(self):
        result = random.randint(2, 12)
        print(f' wynik rzutu: {result}')
        return result

    def move_forward(self, dice_roll_result):
        if request.method == 'POST':
            if request.form.get('forward'):
                if IndexError:
                    self.position = cards.ow_game_field[
                        cards.ow_game_field.index(self.position) + dice_roll_result - len(cards.ow_game_field)]
                    return self.position

    def move_backward(self, throw):
        self.position = cards.ow_game_field[cards.ow_game_field.index(self.position) - throw]
        return self.position
