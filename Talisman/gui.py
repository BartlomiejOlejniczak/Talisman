from database import *
from player import *
from poszukiwacze import *
from main import *
from game import *

player1 = ''
game_phase = 0
position = ''
char_name = ''


@app.route('/', methods=['POST', 'GET'])
def home():
    global player1, game_phase, position, char_name
    print(f'pos:{position} name: {char_name}')

    if request.method == 'POST':
        if player1 == '':
            player1 = Player()
            player1.choose_character_random()
            char_name = player1.character.title
            game_phase = 1
            position = player1.position
            print(f'post pos:{position} name: {char_name}')

            return render_template('index.html', name=char_name, game_phase=game_phase, position=position)
        # if request.form.get(move) == 'move':
        if game_phase == 1:
            player1.move()
            position = player1.position
            print(player1.position)
            # return redirect(url_for('home', name=char_name, position=position))
            print(f'move pos:{position} name: {char_name}')
            return render_template('index.html', name=char_name, game_phase=game_phase, position=position)
        # return redirect(url_for('home', name=char_name))
        return render_template('index.html', name=char_name, game_phase=game_phase, position=position)

    # if player1:
    #     char_name = player1.character.title
    # else:
    #     player1 = Player()
    #     player1.choose_character_random()

    # return render_template('index.html', name=char_name, game_phase=game_phase)
    return render_template('index.html', name=char_name, game_phase=game_phase, position=position)


if __name__ == '__main__':
    app.run(debug=True)
