from database import *
import cards
import random
import game
from poszukiwacze import *


class Player():
    def __init__(self):
        self.character = ''
        self.position = ''
        self.current_player = ''
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

    def throw_1c(self):
        result = random.randint(1, 6)
        print(f' wynik rzutu: {result}')
        return result

    def throw_2c(self):
        result = random.randint(2, 12)
        print(f' wynik rzutu: {result}')
        return result

    def move_forward(self, throw):
        if request.method == 'POST':
            if request.form.get('forward'):
                if IndexError:
                    self.position = cards.ow_game_field[
                        cards.ow_game_field.index(self.position) + throw - len(cards.ow_game_field)]
                    return self.position

    def move_backward(self, throw):
        self.position = cards.ow_game_field[cards.ow_game_field.index(self.position) - throw]
        return self.position
