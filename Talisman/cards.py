from database import Outer_world
from database import *
ow_game_field = Outer_world.query.all()
from database import AdventureCard
# game_adv_cards = []
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

# class AdvCard():
#     def __init__(self):
#         self.position = ''
#         self.title = ''
#         self.type = ''
#         self.enemy_type = ''
#         self.strength = ''
#         self.craft = ''
#         self.is_special = False
#         self.description = ''
#
# for card in AdventureCard.query.all():
#     card = AdvCard()
#     game_adv_cards.append(card)

# from database import AdventureCard
# mummy =AdventureCard(title='mummy',
#                       craft=2,
#                       meet_number=3,
#                       type='enemy',
#                       enemy_type='ghost',
#                       is_special = True)
#
# db.session.add(mummy)
# db.session.commit()