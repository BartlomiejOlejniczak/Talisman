from database import *
from player import *
from poszukiwacze import *
from main import *
from game import *
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

game_phase = 'how_many_players'
position = ''
char_name = ''
throw = ''
cp_index = 0
players_in_game = []
current_player = ''


@app.route('/', methods=['POST', 'GET'])
def home():
    global player1, game_phase, position, char_name, throw, players_in_game, cp_index, current_player

    if request.method == 'POST':
        if game_phase == 'how_many_players':
            a = int(request.form['p'])
            for player in range(1, a + 1):
                player = Player()
                player.choose_character_random()
                player.name = f'player{player}'
                # players_in_game.append(f'player{player}')
                players_in_game.append(player)

            print(players_in_game)
            game_phase = 1
            # current_player = 0
            current_player = players_in_game[cp_index]
            char_name = current_player.character.title

        if request.form.get('move'):
            print(f'babababa: {players_in_game[0].character.title}')
            if game_phase == 1:
                throw = current_player.throw_1c()
                current_player.throw = throw
                game_phase = 2

        if request.form.get('forward'):
            current_player.move_forward(throw)
            position = current_player.position.name
            print(position)

        if request.form.get('backward'):
            current_player.move_backward(throw)
            position = current_player.position.name
            print(position)


        return render_template('index.html', name=char_name, game_phase=game_phase, position=position)
        # return redirect(url_for('home', name=char_name))
        # return render_template('index.html', name=char_name, game_phase=game_phase, position=position)

    return render_template('index.html', name=char_name, game_phase=game_phase, position=position)


if __name__ == '__main__':
    app.run(debug=True)
