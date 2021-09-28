# from flask import Flask, render_template, redirect, url_for, flash , request
import cards
import poszukiwacze
from cards import *
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


def throw_1c():
    result = random.randint(1, 6)
    return result


def throw_2c():
    result = random.randint(2, 12)
    return result


print(cards.ow_game_field)


# print(poszukiwacze.outher_world)

class Player():
    def __init__(self):
        self.position = cards.ow_game_field[0]
        # self.position = poszukiwacze.outher_world[0]

    def move(self):
        throw = throw_1c()
        self.position_index = cards.ow_game_field.index(self.position)
        # self.position_index = poszukiwacze.outher_world.index(self.position)
        print(f'indeks pozycji {self.position_index}')
        # self.position = poszukiwacze.outher_world[self.position_index + throw]
        print(f'wynik rzutu: {throw}')
        if input('press + if you want to move forward: ') == '+':
            self.position = cards.ow_game_field[self.position_index + throw]
        else:
            self.position = cards.ow_game_field[self.position_index - throw]


player = Player()
print(player.position.name)
player.move()
print(player.position.name)
player.move()
print(player.position.name)

# if __name__ == "__main__":
#     app.run(debug=True)
