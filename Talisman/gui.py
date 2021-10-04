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
        print(f'tal_game game phase to {tal_game.game_phase}')
        if tal_game.game_phase == 'how_many_players':
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

        if request.form.get('dice_roll'):
            tal_game.current_player.dice_roll_single()
            tal_game.game_phase = 2

        if request.form.get('forward'):
            tal_game.current_player.move_forward(tal_game.current_player.dice_roll_result)
            tal_game.check_player_position()
            tal_game.end_turn()

        if request.form.get('backward'):
            tal_game.current_player.move_backward(tal_game.current_player.dice_roll_result)
            tal_game.check_player_position()
            tal_game.end_turn()

        position = tal_game.current_player.position.name

        return render_template('game.html', name=tal_game.current_player.character.title,
                               game_phase=tal_game.game_phase,
                               throw=tal_game.current_player.dice_roll_result,
                               position=position)

    return render_template('game.html', name='', game_phase=tal_game.game_phase, throw='',
                           position='')


if __name__ == '__main__':
    app.run(debug=True)
