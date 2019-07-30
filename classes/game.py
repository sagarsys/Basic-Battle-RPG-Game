import random
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Character:
    def __init__(self, name, hp, mp, atk, df, mgk, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_lo = atk - 10
        self.atk_hi = atk + 10
        self.df = df
        self.mgk = mgk
        self.inventory = items
        self.actions = ['Attack', 'Magic', 'Items']

    def generate_dmg(self):
        return random.randrange(self.atk_lo, self.atk_hi)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, pts):
        self.hp += pts
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def recover(self, pts):
        self.mp += pts
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_spell(self, i):
        return self.mgk[i]

    def get_item(self, i):
        return self.inventory[i]['item']

    def get_item_qnt(self, i):
        return self.inventory[i]['quantity']

    def increment_item_qnt(self, i, __qnt=1):
        self.inventory[i]['quantity'] += __qnt

    def decrement_item_qnt(self, i):
        self.inventory[i]['quantity'] -= 1

    def get_action(self, i):
        return self.actions[i]

    def choose_action(self):
        i = 1
        print(bcolors.HEADER + bcolors.UNDERLINE + 'Actions' + bcolors.ENDC)
        for item in self.actions:
            print('    ', str(i), item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.HEADER + bcolors.UNDERLINE + 'Magic' + bcolors.ENDC)
        for item in self.mgk:
            print('    ', str(i), item.get_name(), '-', str(item.get_mp_cost()))
            i += 1

    def choose_items(self):
        i = 1
        print(bcolors.HEADER + bcolors.UNDERLINE + 'Items' + bcolors.ENDC)
        for items in self.inventory:
            print('    ', str(i), items['item'].name, '-', items['item'].desc,
                  'x ' + bcolors.OKBLUE + bcolors.BOLD + str(items['quantity']) + bcolors.ENDC)
            i += 1

    def get_stats(self):
        return 'HP ' + str(self.hp) + '/' + str(self.max_hp) + ' MP ' + str(self.mp) + '/' + str(self.max_mp)

    def pprint_stats(self):
        hp_disp = str(self.hp) + '/' + str(self.max_hp)
        mp_disp = str(self.mp) + '/' + str(self.max_mp)

        max_name_len = 20
        max_mp_len = 11

        name_offset = max_name_len - len(self.name) - len(hp_disp)
        mp_offset = max_mp_len - len(mp_disp)

        name = self.name
        name += name_offset * ' '

        mp = ''
        mp += mp_offset * ' '
        mp += mp_disp

        max_hp_spaces = 25
        max_mp_spaces = 10

        curr_hp_percentile = self.hp / self.max_hp
        curr_mp_percentile = self.mp / self.max_mp

        num_of_hp_tiles = math.floor(max_hp_spaces * curr_hp_percentile)
        num_of_mp_tiles = math.floor(max_mp_spaces * curr_mp_percentile)
        num_of_hp_spaces = max_hp_spaces - num_of_hp_tiles
        num_of_mp_spaces = max_mp_spaces - num_of_mp_tiles

        __actual_hp = ''
        __actual_mp = ''

        if num_of_hp_tiles > 0:
            __actual_hp += '█' * num_of_hp_tiles
        if num_of_mp_tiles > 0:
            __actual_mp += '█' * num_of_mp_tiles

        __actual_hp += ' ' * num_of_hp_spaces
        __actual_mp += ' ' * num_of_mp_spaces

        print('Name                  ____________HP_____________             _____MP_____')
        print(
            name + hp_disp + '  ║'
            + bcolors.OKGREEN + __actual_hp + bcolors.ENDC + '║'
            + mp + '  ║'
            + bcolors.OKBLUE + __actual_mp + bcolors.ENDC + '║'
        )

    def pprint_hp_stats(self):
        hp_disp = '{}/{}'.format(str(self.hp), str(self.max_hp))

        max_name_len = 20

        name_offset = max_name_len - len(self.name) - len(hp_disp)
        name = self.name
        name += name_offset * ' '

        max_hp_spaces = 50
        curr_hp_percentile = self.hp / self.max_hp
        num_of_hp_tiles = math.floor(max_hp_spaces * curr_hp_percentile)
        num_of_spaces = max_hp_spaces - num_of_hp_tiles
        hp = ''
        if num_of_hp_tiles > 0:
            hp += '█' * num_of_hp_tiles
        hp += ' ' * num_of_spaces

        print('Name                  _________________________HP_________________________')
        print(
            name + hp_disp + '  ║'
            + bcolors.FAIL + hp + bcolors.ENDC + '║'
        )
