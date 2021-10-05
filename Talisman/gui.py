from flask import url_for
from database import *
from player import *
from poszukiwacze import *
from main import *
from game import *
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import EmailField
from game import *


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', logged_in=current_user.is_authenticated)


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    send = SubmitField('register')


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    send = SubmitField('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        new_user = User()
        new_user.email = form.email.data
        new_user.password = form.password.data
        new_user.name = form.name.data
        db.session.add(new_user)
        db.session.commit()

    return render_template("/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f'{email}{password}')
        if User.query.filter_by(email=email).first():
            user = User.query.filter_by(email=email).first()
            if user.password == password:
                login_user(user)
                return redirect(url_for('game'))
            else:
                flash('password incorrect, please try again')
        else:
            flash('email incorrect, please try again')
            # redirect(url_for('login')).
    return render_template("/login.html", form=form, logged_in=current_user.is_authenticated)


tal_game = Game()


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'POST':

        if tal_game.game_phase == 'how_many_players':
            # print(tal_game.adventure_cards)
            a = int(request.form['p'])
            for player in range(1, a + 1):
                player = Player()
                player.choose_character_random()
                player.name = f'player{player}'
                tal_game.players_in_game.append(player)

            tal_game.game_phase = 1
            tal_game.current_player = tal_game.players_in_game[tal_game.cp_index]
            return render_template('game.html', name=tal_game.current_player.character.title,
                                   game_phase=tal_game.game_phase, throw='',
                                   position=tal_game.current_player.character.start_position)

        if request.form.get('dice_roll') and tal_game.game_phase == 1:
            tal_game.current_player.dice_roll_single()
            fw_space = cards.ow_game_field[
                cards.ow_game_field.index(
                    tal_game.current_player.position) + tal_game.current_player.dice_roll_result - len(
                    cards.ow_game_field)]
            bw_space = cards.ow_game_field[
                cards.ow_game_field.index(tal_game.current_player.position) - tal_game.current_player.dice_roll_result]

            tal_game.game_phase = 2
            move_option_1 = {'name' : fw_space.name,
                             'cards to draw' : fw_space.card}

            move_option_2 = bw_space.name

            return render_template('game.html', name=tal_game.current_player.character.title,
                                   game_phase=tal_game.game_phase, throw='',
                                   position=tal_game.current_player.character.start_position,
                                   move_option_1=move_option_1, move_option_2 = move_option_2)

        if request.form.get('forward') and tal_game.game_phase == 2:
            tal_game.current_player.move_forward(tal_game.current_player.dice_roll_result)
            tal_game.game_phase = 3

        if request.form.get('backward') and tal_game.game_phase == 2:
            tal_game.current_player.move_backward(tal_game.current_player.dice_roll_result)
            tal_game.game_phase = 3

        if tal_game.game_phase == 3:
            # check if is another player on space
            if not tal_game.check_player_position():
                # if not go to space ecounter
                tal_game.game_phase = 4
            else:
                # if yes choose if you want to ecounter character
                tal_game.game_phase = 5_1

        # ECOUNTER the SPACE  PHASE

        if tal_game.game_phase == 4:
            # check if space has special abilites ex. Town
            if not tal_game.check_if_space_is_special():
                # drawing a card
                tal_game.draw_card()
                if tal_game.current_adv_card.type == 'enemy':
                    tal_game.game_phase = 'EWE_Evade'
                # print(f'draw {tal_game.current_player.position.card} card')

            else:
                tal_game.end_turn()
        position = tal_game.current_player.position.name
        enemy_name = tal_game.current_adv_card.title
        # ECOUNTER WITH ENEMY
        if tal_game.game_phase == 'EWE_Evade':
            if request.form.get('yes'):
                tal_game.end_turn()
            # else:
            if request.form.get('no'):
                tal_game.game_phase = 'EWE_Spells'
                return render_template('game.html', name=tal_game.current_player.character.title,
                                       game_phase=tal_game.game_phase,
                                       throw=tal_game.current_player.dice_roll_result,
                                       position=position)
        if tal_game.game_phase == 'EWE_Spells':
            if request.form.get('yes'):
                pass
            else:
                tal_game.game_phase = 'EWE_Battle'
                return render_template('game.html', name=tal_game.current_player.character.title,
                                       game_phase=tal_game.game_phase,
                                       throw=tal_game.current_player.dice_roll_result,
                                       position=position, enemy_name=enemy_name)
        if tal_game.game_phase == 'EWE_Battle':
            if request.form.get('dice_roll_enemy'):
                tal_game.enemy_strength = tal_game.current_adv_card.strength + tal_game.current_player.dice_roll_single()
            if request.form.get('dice_roll_character'):
                tal_game.current_player_battle_strength = tal_game.current_player.character.strenght + tal_game.current_player.dice_roll_single()
            if tal_game.current_player_battle_strength != '' and tal_game.enemy_strength != '':
                tal_game.ecounter_with_enemy()

        return render_template('game.html', name=tal_game.current_player.character.title,
                               game_phase=tal_game.game_phase,
                               throw=tal_game.current_player.dice_roll_result,
                               position=position)

    return render_template('game.html', name='', game_phase=tal_game.game_phase, throw='',
                           position='')


if __name__ == '__main__':
    app.run(debug=True)
