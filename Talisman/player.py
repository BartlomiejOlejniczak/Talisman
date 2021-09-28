import cards
import random
import game
from poszukiwacze import *


class Player():
    def __init__(self):
        self.character = self.choose_character_random()
        self.position = self.character.start_position
        self.current_player = ''

    def choose_character_random(self):
        char = random.choice(classes)
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

    def move(self):
        throw = self.throw_1c()
        self.position_index = cards.ow_game_field.index(self.position)
        print(f'\n indeks pozycji {self.position_index}')
        if input('press + if you want to move forward: ') == '+':
            # if cards.ow_game_field[self.position_index + throw] > len(cards.ow_game_field):
            if IndexError:
                self.position = cards.ow_game_field[self.position_index + throw - len(cards.ow_game_field)]
        else:
            self.position = cards.ow_game_field[self.position_index - throw]
