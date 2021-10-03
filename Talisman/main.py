# from flask import Flask, render_template, redirect, url_for, flash , request
import cards
import poszukiwacze
from cards import *
# from player import *

# import random

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
#
# for space in cards.ow_game_field:
#     print(f'{space.name}, {cards.ow_game_field.index(space)}')

# player1 = Player()
# player2 = Player()
# print(player1.character.title)
# print(player2.character.title)

# player.move()
# print(player.position.name)
# player.move()
# print(player.position.name)
from database import *
from player import *
from poszukiwacze import *
from main import *
from game import *

player1 = ''
game_phase = 'how_many_players'
position = ''
char_name = ''
throw = ''
current_player = ''
players_in_game = []


@app.route('/', methods=['POST', 'GET'])
def home():
    global player1, game_phase, position, char_name, throw, players_in_game
    if request.method == 'POST':
        if game_phase == 'how_many_players':
            a = int(request.form['p'])
            for player in range(1,a+1):
                players_in_game.append(f'player{player}')
            print(players_in_game)
            for p in players_in_game:
                p = Player()
                p.choose_character_random()
                print(p.character)


        if request.form.get('move'):
            # if game_phase == 1:
            throw = player1.throw_1c()
            # player1.throw = throw
            game_phase = 2

        if request.form.get('forward'):
            player1.move_forward(throw)
            position = player1.position.name

        if request.form.get('backward'):
            player1.move_backward(throw)
            position = player1.position.name

        return render_template('index.html', name=char_name, game_phase=game_phase, position=position)
        # return redirect(url_for('home', name=char_name))
        # return render_template('index.html', name=char_name, game_phase=game_phase, position=position)

    return render_template('index.html', name=char_name, game_phase=game_phase, position=position)


if __name__ == '__main__':
    app.run(debug=True)




# if __name__ == "__main__":
#     app.run(debug=True)
