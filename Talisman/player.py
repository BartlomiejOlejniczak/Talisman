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

    def choose_character_random(self):
        char = random.choice(classes)
        self.character = char
        self.position = char.start_position
        print(f'{Outer_world.query.filter_by(name=self.position).first().id}')
        print(f'player.py { self.position }')
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

    # def move(self):
    #     throw = self.throw_1c()
    #     for space in cards.ow_game_field:
    #         print(f'{space.name}, {cards.ow_game_field.index(space)}')
    #     self.position_index = cards.ow_game_field.index(self.position)
    #     print(f'\n indeks pozycji {self.position_index}')
    #     if input('press + if you want to move forward: ') == '+':
    #         # if cards.ow_game_field[self.position_index + throw] > len(cards.ow_game_field):
    #         if IndexError:
    #             self.position = cards.ow_game_field[self.position_index + throw - len(cards.ow_game_field)]
    #             return self.position
    #     else:
    #         self.position = cards.ow_game_field[self.position_index - throw]
    #         return self.position
    #
    def move(self):
        throw = self.throw_1c()
        print(cards.ow_game_field)
        self.position_index = cards.ow_game_field.index(self.position)
        print(f'\n indeks pozycji {self.position_index}')
        if input('press + if you want to move forward: ') == '+':
            # if cards.ow_game_field[self.position_index + throw] > len(cards.ow_game_field):
            if IndexError:
                self.position = cards.ow_game_field[self.position_index + throw - len(cards.ow_game_field)]
                return self.position
        else:
            self.position = cards.ow_game_field[self.position_index - throw]
            return self.position

