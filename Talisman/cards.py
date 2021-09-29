from database import Outer_world
from database import *
ow_game_field = Outer_world.query.all()
# ow_game_field = Outer_world.c.name


# name='tave'
#
print (ow_game_field.index(1))
# print(Outer_world.query.filter_by(name='tavern').first().id)
# print(ow_game_field.query.filter_by(name='tavern').first().id)
# print(ow_game_field.index('tavern').name)