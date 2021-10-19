from flask import url_for
from database import *
from player import *
from poszukiwacze import *
from main import *
# from game import *
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import EmailField
from game2 import *


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


game_is_on = True


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    try:
        tal_game.current_player.position.name
    except AttributeError:
        pass
    else:
        position = tal_game.current_player.position.name
    try:
        tal_game.current_adv_card
    except AttributeError:
        pass
    else:
        card = tal_game.current_adv_card

    if request.method == 'POST':
        if tal_game.game_phase == 'how_many_players':
            a = int(request.form['quantity'])
            for player in range(1, a + 1):
                player = Player()
                player.choose_character_random()
                player.name = f'player{player}'
                tal_game.players_in_game.append(player)
            print(tal_game.players_in_game)

            tal_game.current_player = tal_game.players_in_game[tal_game.cp_index]

            if len(tal_game.current_player.character.b4mov_spells) > 0:
                tal_game.game_phase = 'b4mov_spells'
            else:
                tal_game.game_phase = 'movement_dice_roll'
            # tal_game.display_ref()
        # CAST SPELLS BEFORE MOVEMENT PHASE

        if tal_game.game_phase == 'b4mov_spells':
            if len(tal_game.current_player.character.b4mov_spells) > 0:
                tal_game.game_subphase = 'b4mov_spells_casting'
                pass
            else:
                tal_game.game_phase = 'movement_dice_roll'

        # MOVEMENT PHASE
        if tal_game.game_phase == 'movement_dice_roll':
            if request.form.get('dice_roll') and tal_game.game_phase == 'movement_dice_roll':
                tal_game.current_player.dice_roll_single()

                tal_game.game_subphase = 'movement'
                tal_game.display_ref()

            if request.form.get('forward') and tal_game.game_subphase == 'movement':
                tal_game.current_player.move_forward(tal_game.current_player.dice_roll_result)
                tal_game.game_phase = 3

            if request.form.get('backward') and tal_game.game_subphase == 'movement':
                tal_game.current_player.move_backward(tal_game.current_player.dice_roll_result)
                tal_game.game_phase = 3

            tal_game.display_ref()

            if tal_game.game_phase == 3:
                # check if is another player on space
                if not tal_game.check_player_position():
                    # if not go to space ecounter
                    tal_game.game_phase = 'ETS'
                else:
                    # if yes choose if you want to ecounter character
                    if request.form.get('yes'):
                        tal_game.game_phase = 'ETP'
                    if request.form.get('no'):
                        tal_game.game_phase = 'ETS'
                tal_game.display_ref()

        # ECOUNTER the SPACE  PHASE

        if tal_game.game_phase == 'ETS':
            # check if space has special abilites ex. Town
            if not tal_game.check_if_space_is_special():
                # drawing a card
                if request.form.get('draw'):
                    tal_game.draw_card()
                    tal_game.game_subphase = 'ETS_draw'
                    # tal_game.display_ref()
                if request.form.get('OK_card'):
                    if tal_game.game_subphase == 'ETS_draw':
                        if tal_game.current_adv_card.type == 'enemy':
                            tal_game.game_phase = 'EWE'
                            if tal_game.current_player.character.evade == True:
                                tal_game.game_subphase = 'EWE_Evade'
                            elif len(tal_game.current_player.battle_spells) > 0:
                                tal_game.game_subphase = 'EWE_Spells'
                            else:
                                tal_game.game_subphase = 'EWE_Battle'

                tal_game.display_ref()


            else:
                print('space is special')
                tal_game.end_turn()
                tal_game.display_ref()
            # return render_template('game2.html', display=tal_game.display)

        # ECOUNTER WITH ENEMY
        if tal_game.game_phase == 'EWE':

            if tal_game.game_subphase == 'EWE_Evade':
                if request.form.get('yes_EWE_Evade'):
                    tal_game.end_turn()
                if request.form.get('no_EWE_Evade'):

                    if len(tal_game.current_player.battle_spells) > 0:
                        tal_game.game_subphase = 'EWE_Spells'
                    else:
                        tal_game.game_subphase = 'EWE_Battle'

            if tal_game.game_subphase == 'EWE_Spells':
                if request.form.get('yes_EWE_Spells'):
                    tal_game.game_subphase = 'EWE_Battle'
                if request.form.get('no_EWE_Spells'):
                    tal_game.game_subphase = 'EWE_Battle'

            if tal_game.game_subphase == 'EWE_Battle':

                if request.form.get('dice_roll_enemy'):
                    tal_game.e_battle_strength()

                if request.form.get('dice_roll_character'):
                    tal_game.current_player.p_battle_strength()

                if tal_game.current_player.battle_strength > tal_game.current_player.strength and tal_game.battle_modificator > 0:
                    tal_game.ecounter_with_enemy()
            tal_game.display_ref()

        # ECOUNTER WITH ANOTHER PLAYER

        if tal_game.game_phase == 'EWP':
            tal_game.game_phase = 'EWP_Choose_PLayer_to_attack'
            tal_game.game_subphase = 'EWP_Choose'
            if request.form.get('skill_EWP'):
                tal_game.game_subphase = 'EWP_Skills'
            if request.form.get('strength_EWP'):
                tal_game.game_subphase = 'EWP_strength'
            if request.form.get('craft_EWP'):
                tal_game.game_subphase = 'EWP_craft'




    if request.form.get('end_turn'):
        tal_game.end_turn()

    #
    return render_template('game2.html', display=tal_game.display)


if __name__ == '__main__':
    app.run(debug=True)
