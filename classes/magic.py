import random


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_dmg(self):
        return random.randrange(self.dmg - 10, self.dmg + 10)

    def get_name(self):
        return self.name

    def get_mp_cost(self):
        return self.cost

    def get_type(self):
        return self.type

