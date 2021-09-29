from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///talisman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



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
    description = db.Column(db.String(250), nullable=True)
    meet_number = db.Column(db.Integer, nullable=False)


class AdventureCard_enemy(db.Model, Base):
    __tablename__ = 'adventure_card_enemy'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    craft = db.Column(db.Integer, nullable=True)
    meet_number = db.Column(db.Integer, nullable=False)


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




# new_ac_enemy = AdventureCard_enemy()
# new_ac_enemy.title = 'bear'
# new_ac_enemy.strength = 3
# new_ac_enemy.meet_number = 2
# db.session.add(new_ac_enemy)
# db.session.commit()


#
# new_field = Outer_world()
# new_field.name = 'city'
# new_field.special = True
#
# db.session.add(new_field)
# db.session.commit()


