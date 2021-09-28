# outher_world = ['city', 'fields', 'hills', 'plains', 'wood', 'plains', 'tavern', 'city', 'fields', 'hills', 'plains',
#                 'wood', 'plains', 'tavern']


class Character():
    def __init__(self):
        self.strenght = 0
        self.craft = 0
        self.gold = 0
        self.fate = 0
        self.life = 4
        self.spells = 0
        self.max_items = 4
        self.start_place = 0
        self.aligment = 'neutral'

    def small_wizz(self):
        self.spells = 1

    def big_wizz(self):
        self.spells = 2

    def craft_attack(self):
        pass


class Warrior(Character):
    def __init__(self):
        super().__init__()
        self.strenght = 4
        self.craft = 2
        self.fate = 1
        self.life = 5
        self.start_place = 'tavern'

    def twohanded(self):
        pass

    def lucky_figher(self):
        pass


class Thiev(Character):
    def __init__(self):
        super().__init__()
        self.strenght = 3
        self.craft = 3
        self.fate = 2
        self.start_place = 'city'

    def steal_char(self):
        pass

    def steal_eq(self):
        pass


def choose_player():
    pass

def move():
    if 'there are anothers players?':
        if 'yes':
            if 'do you want to meet him ?':
                if 'yes':
                    if 'attack of special ability?':
                        if 'choose gifht style might or magic':
                            if 'normal':
                                'normal fight()'
                                'end turn()'
                            else:
                                'magic fight()'
                                'end turn()'
                    else:
                        'use special ability on player()'
                    'end turn()'
    'ecounter the space()'
    if 'card to draw?':
        if 'yes':
            'draw a card()'
            'card ecounter()'
        else:
            'card ecounter()'
    else:
        'follow instruction on space()'

# def turn():
#     if 'player has spells, to cast before movement':
#         'cast special spell()'
#         move()
#     else:
#         move()
