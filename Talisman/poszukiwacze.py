from database import Character


class Char(Character):
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

    def small_wizz(self):
        self.spells = 1

    def big_wizz(self):
        self.spells = 2

    def craft_attack(self):
        pass

    def can_fight_craft(self):
        self.craft_fighting = True


class Warrior(Char):
    def __init__(self):
        super().__init__()
        self.title = 'warrior'
        self.strenght = 4
        self.craft = 2
        self.fate = 1
        self.life = 5
        self.start_position = 'tavern'

    def twohanded(self):
        print('use two weapons')

    def lucky_figher(self):
        pass


class Thiev(Char):
    def __init__(self):
        super().__init__()
        self.title = 'thiev'
        self.strenght = 3
        self.craft = 3
        self.fate = 2
        self.start_position = 'city'

    def steal_char(self):
        pass

    def steal_eq(self):
        pass


classes = [Warrior(), Thiev()]

# db.create_all()
# db.session.add(Thiev())
# db.session.add(Warrior())
# db.session.commit()


# def turn():
#     if 'player has spells, to cast before movement':
#         'cast special spell()'
#         move()
#     else:
#         move()
