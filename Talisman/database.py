from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import jyserver.Flask as jsf


from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///talisman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return App.render(render_template('index2.html'))



class Outer_world(db.Model, Base):
    __tablename__ = 'outer_world'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=True)
    special = db.Column(db.Boolean, nullable=True)
    card = db.Column(db.Integer, nullable=True)


class AdventureCard(db.Model, Base):
    __tablename__ = 'adventure_card'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    meet_number = db.Column(db.Integer, nullable=False)
    enemy_type = db.Column(db.String(250), nullable=True)
    is_special = db.Column(db.Boolean, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    craft = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(250), nullable=True)

    def __init__(self):
        self.position = ''
        self.tokens = ''


class Character(db.Model, Base):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    strenght = db.Column(db.Integer, nullable=False)
    craft = db.Column(db.Integer, nullable=False)
    life = db.Column(db.Integer, nullable=False)
    fate = db.Column(db.Integer, nullable=False)
    gold = db.Column(db.Integer, nullable=True)
    spells = db.Column(db.Integer, nullable=True)
    aligment = db.Column(db.String(250), nullable=False)
    start_position = db.Column(db.String(250), nullable=False)
    craft_fighting = db.Column(db.Boolean, nullable=True)

    def __init__(self):
        self.title = ''
        Character.title = self.title
        self.strenght = 0
        Character.strenght = self.strenght
        self.craft = 0
        Character.craft = self.craft
        self.gold = 0
        Character.gold = self.gold
        self.fate = 0
        Character.fate = self.fate
        self.life = 4
        Character.life = self.life
        self.spells = 0
        Character.spells = self.spells
        self.max_items = 4
        self.start_position = ''
        Character.start_position = self.start_position
        self.aligment = 'neutral'
        Character.aligment = self.aligment
        self.craft_fighting = False
        Character.craft_fighting = self.craft_fighting
        self.evade = False
        self.b4mov_spells = []

    def small_wizz(self):
        self.spells = 1

    def big_wizz(self):
        self.spells = 2

    def craft_attack(self):
        pass

    def can_fight_craft(self):
        self.craft_fighting = True


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# db.create_all()
#
# new_ac = AdventureCard()
# new_ac.title = 'bear'
# new_ac.strength = 3
# new_ac.meet_number = 2
# new_ac.type = 'enemy'
# new_ac.enemy_type = 'animal'
# db.session.add(new_ac)
# db.session.commit()

# new_ac = AdventureCard()

#
# new_field = Outer_world()
# new_field.name = 'city'
# new_field.special = True
#
# db.session.add(new_field)
# db.session.commit()
