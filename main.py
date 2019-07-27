from classes.game import Character, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Spells
blizzard = Spell('Blizzard', 5, 30, 'elemental')
firebolt = Spell('Firebolt', 10, 75, 'elemental')
thunderbolt = Spell('Thunderbolt', 15, 100, 'elemental')
lightning = Spell('Chain Lightning', 20, 150, 'elemental')
meteor = Spell('Meteor', 25, 200, 'elemental')
necromancy = Spell('Necromancy', 10, 50, 'black')
summon = Spell('Summoned Swords', 20, 150, 'black')
cure = Spell('Cure', 10, 100, 'white')
g_cure = Spell('Greater Cure', 20, 250, 'white')

player_spells = [blizzard, firebolt, thunderbolt, lightning, meteor, cure, g_cure]
enemy_spells = [necromancy, summon]


# Items
potion = Item('Potion', 'Heals player HP 50 points', 'potion', 50)
hi_potion = Item('High Potion', 'Heals player HP 150 points', 'potion', 150)
mana = Item('Mana', 'Heals player MP 25 points', 'mana', 25)
hi_mana = Item('Greater Mana', 'Heals player MP 75 points', 'mana', 75)
grenade = Item('Grenade', 'Deals 100 points of damage', 'attack', 100)

player_items = [
    {'item': potion, 'quantity': 3},
    {'item': hi_potion, 'quantity': 1},
    {'item': mana, 'quantity': 2},
    {'item': hi_mana, 'quantity': 1},
    {'item': grenade, 'quantity': 2}
]

# Characters
player = Character(400, 100, 75, 35, player_spells, player_items)
enemy = Character(1000, 40, 30, 20, enemy_spells, [])


# game status tracker
running = True


# game loop
def battle():
    # game status
    global running

    # battle status helper
    def print_battle_stats():
        print('------------------STATS------------------')
        print(bcolors.OKBLUE + 'Player', player.get_stats() + bcolors.ENDC)
        print(bcolors.WARNING + 'Enemy', enemy.get_stats() + bcolors.ENDC)
        print('-----------------------------------------')

    # Input choice helper
    def input_choice(action):
        __choice = input('Choose ' + action + ': ')
        if __choice == '':
            return False
        try:
            return int(__choice) - 1
        except ValueError:
            return False

    # Attack helper
    def attack(__dmg):
        enemy.take_dmg(__dmg)
        print(bcolors.OKGREEN + 'Attack', str(__dmg) + bcolors.ENDC)

    # Magic attack helper
    def mgk_attack(__spell):
        __dmg = __spell.generate_dmg()
        player.reduce_mp(__spell.get_mp_cost())
        enemy.take_dmg(__dmg)
        print(bcolors.OKGREEN + 'Magic Attack', __spell.get_name(), str(__dmg) + bcolors.ENDC)

    # Item attack helper
    def item_attack(__item):
        __dmg = __item.pts
        attack(__dmg)

    # Heal helper
    def heal(__name, __hp):
        player.heal(__hp)
        print(bcolors.OKGREEN + __name, 'heals player', str(__hp) + bcolors.ENDC)

    # Magic Heal helper
    def mgk_heal(__spell):
        __hp = __spell.generate_dmg()
        player.reduce_mp(__spell.get_mp_cost())
        heal(__spell.name, __hp)

    # Item Heal helper
    def item_heal(__item):
        __hp = __item.pts
        heal(__item.name, __hp)

    # Item MP Heal
    def item_mp_recover(__item):
        __mp = __item.pts
        player.recover(__mp)
        print(bcolors.OKGREEN + __item.name, 'recovers player', str(__mp), 'MP' + bcolors.ENDC)

    # spawn enemy
    print(bcolors.HEADER + bcolors.BOLD + 'ENEMY SPAWNS!' + bcolors.ENDC)
    print('=============================')
    # game loop
    while running:
        player.choose_action()
        choice = input_choice('action')
        if not choice:
            continue

        # Attack
        if choice == 0:
            print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
            dmg = player.generate_dmg()
            attack(dmg)
        # Magic
        elif choice == 1:
            print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
            player.choose_magic()
            mgk_choice = input_choice('spell')
            if not mgk_choice:
                continue

            try:
                spell = player.get_spell(mgk_choice)
            except IndexError:
                continue

            print(bcolors.OKBLUE + 'You chose', spell.get_name() + bcolors.ENDC)

            if spell.get_mp_cost() > player.get_mp():
                print(bcolors.FAIL + 'Insufficient MP' + bcolors.ENDC)
                continue

            if spell.type == 'white':
                mgk_heal(spell)
            else:
                mgk_attack(spell)
        # Items
        elif choice == 2:
            print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
            player.choose_items()
            item_choice = input_choice('item')
            if not item_choice:
                continue

            try:
                item = player.get_item(item_choice)
            except IndexError:
                continue

            if player.get_item_qnt(item_choice) <= 0:
                print(bcolors.FAIL + item.name, 'out of stock' + bcolors.ENDC)
                continue

            if item.type == 'potion':
                item_heal(item)
            elif item.type == 'mana':
                item_mp_recover(item)
            elif item.type == 'attack':
                item_attack(item)
            player.decrement_item_qnt(item_choice)

        # Wrong choice
        else:
            continue

        # PLAYER WIN
        if enemy.get_hp() == 0:
            print_battle_stats()
            print('===================================')
            print(bcolors.HEADER + bcolors.BOLD + 'VICTORY!' + bcolors.ENDC)
            print('===================================')
            running = False
            break

        # ENEMY ATTACK
        # enemy_choice = 1
        enemy_dmg = enemy.generate_dmg()
        player.take_dmg(enemy_dmg)
        print(bcolors.FAIL + 'Enemy strikes', str(enemy_dmg) + bcolors.ENDC)

        # PLAYER DEFEAT
        if player.get_hp() == 0:
            print_battle_stats()
            print('===================================')
            print(bcolors.FAIL + bcolors.BOLD + 'DEFEAT!' + bcolors.ENDC)
            print('===================================')
            running = False
            break

        print_battle_stats()


battle()
