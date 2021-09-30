from database import Outer_world
from database import *
ow_game_field = Outer_world.query.all()
# print(ow_game_field)
# for space in ow_game_field:
#     if space.name == 'city':
#         print(type(ow_game_field.index(space)))
# #

# name='tave'
#
# print (ow_game_field.index(1))
# print(Outer_world.query.filter_by(name='tavern').first().id)
# print(ow_game_field.query.filter_by(name='tavern').first().id)
# print(ow_game_field.index('tavern').name)