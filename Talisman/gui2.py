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


tal_game = Game()
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
                print('ppppppppp')
                player = Player()
                player.choose_character_random()
                player.name = f'player{player}'
                tal_game.players_in_game.append(player)
                print(player)


            tal_game.current_player = tal_game.players_in_game[tal_game.cp_index]

            if len(tal_game.current_player.character.b4mov_spells) > 0:
                tal_game.game_phase = 'b4mov_spells'
                print('b4mov_spells')
            else:
                tal_game.game_phase = 'movement_dice_roll'
                print('movement_dice_roll')
            tal_game.display_ref()
            return render_template('game2.html', display=tal_game.display)
        # CAST SPELLS BEFORE MOVEMENT PHASE

        if tal_game.game_phase == 'b4mov_spells':
            print('b4 momooomomomomomom')
            if len(tal_game.current_player.character.b4mov_spells) > 0:
                tal_game.game_subphase = 'b4mov_spells_casting'
                pass
            else:
                tal_game.game_phase = 'movement_dice_roll'

        # MOVEMENT PHASE
        if tal_game.game_phase == 'movement_dice_roll':
            if request.form.get('dice_roll') and tal_game.game_phase == 'movement_dice_roll':
                tal_game.current_player.dice_roll_single()
                # tal_game.change_subphase('movement')
                tal_game.game_subphase = 'movement'
                tal_game.display_ref()
                return render_template('game2.html', display=tal_game.display)




            if request.form.get('forward') and tal_game.game_subphase == 'movement':
                print('forward')
                tal_game.current_player.move_forward(tal_game.current_player.dice_roll_result)
                tal_game.game_phase = 3
                tal_game.display_ref()

            if request.form.get('backward') and tal_game.game_subphase == 'movement':
                tal_game.current_player.move_backward(tal_game.current_player.dice_roll_result)
                tal_game.game_phase = 3

            if tal_game.game_phase == 3:
# check if is another player on space
                if not tal_game.check_player_position():
# if not go to space ecounter
                    tal_game.game_phase = 'ETS'
                else:
                    print('phase 3 pass')
                    tal_game.game_phase = 'ETS'
# if yes choose if you want to ecounter character
                    tal_game.game_phase = 5_1
                # position = tal_game.current_player.position.name
                # return render_template('game.html', name=tal_game.current_player.character.title,
                #                        game_phase=tal_game.game_phase,
                #                        throw=tal_game.current_player.dice_roll_result,
                #                        position=position, game_subphase=tal_game.game_subphase,
                #                        )

            return render_template('game2.html', display=tal_game.display)

        # ECOUNTER the SPACE  PHASE

        if tal_game.game_phase == 'ETS':
            # check if space has special abilites ex. Town
            if not tal_game.check_if_space_is_special():
                # drawing a card
                if request.form.get('draw'):
                    tal_game.draw_card()
                    card = tal_game.current_adv_card
                    tal_game.game_subphase = 'ETS_draw'

                    if tal_game.game_subphase == 'ETS_draw':
                        if tal_game.current_adv_card.type == 'enemy':
                            tal_game.game_phase = 'EWE'
                    # return render_template('game.html', name=tal_game.current_player.character.title,
                    #                            game_phase=tal_game.game_phase,
                    #                            throw=tal_game.current_player.dice_roll_result,
                    #                            position=position, game_subphase=tal_game.game_subphase,
                    #                            card=card.title)
                    return render_template('game2.html', display=tal_game.display)


                # print(f'draw {tal_game.current_player.position.card} card')
            else:
                print('space is special')
                tal_game.end_turn()
            # return render_template('game.html', name=tal_game.current_player.character.title,
            #                        game_phase=tal_game.game_phase,
            #                        throw=tal_game.current_player.dice_roll_result,
            #                        position=position, game_subphase=tal_game.game_subphase,
            #                        card=card.title)
            return render_template('game2.html', display=tal_game.display)

        enemy_name = tal_game.current_adv_card.title
        enemy = tal_game.current_adv_card

        # ECOUNTER WITH ENEMY
        # if tal_game.game_phase == 'EWE':
        #
        #     # check if player can evade enemy
        #
        #     if tal_game.current_player.character.evade == True:
        #         tal_game.game_subphase = 'EWE_Evade'
        #         if tal_game.game_subphase == 'EWE_Evade':
        #             if request.form.get('yes_EWE_Evade') and tal_game.game_subphase == 'EWE_Evade' :
        #                 tal_game.end_turn()
        #             if request.form.get('no_EWE_Evade'):
        #                 tal_game.game_subphase = 'EWE_Spells'
        #                 print(tal_game.game_subphase)
        #         # return render_template('game.html', name=tal_game.current_player.character.title,
        #         #                        game_phase=tal_game.game_phase,
        #         #                        throw=tal_game.current_player.dice_roll_result,
        #         #                        position=position, game_subphase=tal_game.game_subphase)
        #     else:
        #         tal_game.game_subphase = 'EWE_Spells'
        #
        #
        #     if tal_game.game_subphase == 'EWE_Spells':
        #         print(f' pppppppppppppppp {tal_game.game_subphase}')
        #         if request.form.get('yes_EWE_Spells') and tal_game.game_subphase == 'EWE_Spells' :
        #             print(f' yes {tal_game.game_subphase}')
        #             tal_game.game_subphase = 'EWE_Battle'
        #         if request.form.get('no_EWE_Spells'):
        #             tal_game.game_subphase = 'EWE_Battle'
        #         # return render_template('game.html', name=tal_game.current_player.character.title,
        #         #                            game_phase=tal_game.game_phase,
        #         #                            throw=tal_game.current_player.dice_roll_result,
        #         #                            position=position, enemy_name=enemy_name,
        #         #                            game_subphase=tal_game.game_subphase, enemy_strength=enemy.strength)
        #
        #
        #
        #     if tal_game.game_subphase == 'EWE_Battle':
        #         if request.form.get('dice_roll_enemy'):
        #             tal_game.enemy_strength = tal_game.current_adv_card.strength + tal_game.current_player.dice_roll_single()
        #             print(tal_game.enemy_strength)
        #         if request.form.get('dice_roll_character'):
        #             tal_game.current_player_battle_strength = tal_game.current_player.character.strenght + tal_game.current_player.dice_roll_single()
        #             print(tal_game.enemy_strength)
        #         if tal_game.current_player_battle_strength != '' and tal_game.enemy_strength != '':
        #             tal_game.ecounter_with_enemy()
        #
        #         # return render_template('game.html', name=tal_game.current_player.character.title,
        #         #                    game_phase=tal_game.game_phase,
        #         #                    throw=tal_game.current_player.dice_roll_result,
        #         #                    position=position, game_subphase=tal_game.game_subphase)

    # return render_template('game.html', name='', game_phase=tal_game.game_phase, throw='',
    #                        position='')
    return render_template('game2.html', display=tal_game.display)


if __name__ == '__main__':
    app.run(debug=True)
