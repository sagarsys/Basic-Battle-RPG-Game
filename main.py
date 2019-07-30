from classes.game import Character, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Spells
blizzard = Spell('Blizzard', 5, 30, 'elemental')
firebolt = Spell('Firebolt', 10, 75, 'elemental')
thunderbolt = Spell('Thunderbolt', 15, 100, 'elemental')
lightning = Spell('Chain Lightning', 20, 150, 'elemental')
meteor = Spell('Meteor', 25, 200, 'elemental')
necromancy = Spell('Necromancy', 10, 125, 'black')
summon = Spell('Summoned Wraiths', 20, 300, 'black')
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
geralt = Character('Geralt', 400, 150, 25, 50, player_spells, player_items)
valos = Character('Valos', 450, 75, 100, 75, player_spells, player_items)
kratos = Character('Kratos', 600, 50, 150, 25, player_spells, player_items)
# enemies
grunt = Character('Grunt', 1000, 40, 30, 20, enemy_spells, [])
imp = Character('Imp', 1200, 50, 50, 25, enemy_spells, [])
kraken = Character('Kraken', 2500, 100, 50, 125, enemy_spells, [])


player_party = [
    geralt, valos, kratos
]
enemy_party = [
    grunt, imp, kraken
]

geralt.targets = enemy_party
valos.targets = enemy_party
kratos.targets = enemy_party

grunt.targets = player_party
imp.targets = player_party
kraken.targets = player_party

defeated_enemies = []
defeated_players = []

# game status tracker
running = True


# game loop
def battle():
    # game status
    global running

    # battle status helper
    def print_battle_stats():
        print('------------------STATS------------------')
        # print(bcolors.OKBLUE + 'Player', player.get_stats() + bcolors.ENDC)
        # print(bcolors.WARNING + 'Enemy', enemy.get_stats() + bcolors.ENDC)
        player.pprint_stats()
        enemy.pprint_hp_stats()
        print('-----------------------------------------')

    # Input choice helper
    def input_choice(action):
        __choice = input('Choose ' + action + ': ')
        if __choice == '':
            return False
        try:
            return int(__choice)
        except ValueError:
            return False

    # Attack helper
    def attack(__dmg, __target):
        enemy_party[__target].take_dmg(__dmg)
        print(bcolors.OKGREEN + 'Attack', str(__dmg), enemy_party[__target].name + bcolors.ENDC)

    # Magic attack helper
    def mgk_attack(__spell, __player, __target):
        __dmg = __spell.generate_dmg()
        __player.reduce_mp(__spell.get_mp_cost())
        enemy_party[__target].take_dmg(__dmg)
        print(bcolors.OKGREEN + 'Magic Attack', __spell.get_name(), str(__dmg), enemy_party[__target].name + bcolors.ENDC)

    # Item attack helper
    def item_attack(__item, __target):
        __dmg = __item.pts
        attack(__dmg, __target)

    # Heal helper
    def heal(__name, __hp, __player):
        __player.heal(__hp)
        print(bcolors.OKGREEN + __name, 'heals', __player.name, str(__hp) + bcolors.ENDC)

    # Magic Heal helper
    def mgk_heal(__spell, __player):
        __hp = __spell.generate_dmg()
        __player.reduce_mp(__spell.get_mp_cost())
        heal(__spell.name, __hp, __player)

    # Item Heal helper
    def item_heal(__item, __player):
        __hp = __item.pts
        heal(__item.name, __hp, __player)

    # Item MP Heal
    def item_mp_recover(__item, __player):
        __mp = __item.pts
        __player.recover(__mp)
        print(bcolors.OKGREEN + __item.name, 'recovers player', str(__mp), 'MP' + bcolors.ENDC)

    # spawn enemy
    print(bcolors.HEADER + bcolors.BOLD + 'ENEMY SPAWNS!' + bcolors.ENDC)
    print('=============================')
    # game loop
    while running:
        for player in player_party:
            player.pprint_stats()
        for enemy in enemy_party:
            enemy.pprint_hp_stats()

        for player in player_party:
            player.choose_action()
            choice = input_choice('action')
            if not choice:
                continue
            choice -= 1  # avoid zero values to be evaluated to False
            player.choose_target()
            target_choice = input_choice('target')
            if not target_choice:
                target_choice = 0
            else:
                target_choice -= 1
            print(bcolors.OKBLUE + 'You chose', player.get_target(target_choice).name + bcolors.ENDC)
            # Attack
            if choice == 0:
                print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
                dmg = player.generate_dmg()
                attack(dmg, target_choice)
            # Magic
            elif choice == 1:
                print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
                player.choose_magic()
                mgk_choice = input_choice('spell')
                if not mgk_choice:
                    continue
                mgk_choice -= 1

                try:
                    spell = player.get_spell(mgk_choice)
                except IndexError:
                    continue

                print(bcolors.OKBLUE + 'You chose', spell.get_name() + bcolors.ENDC)

                if spell.get_mp_cost() > player.get_mp():
                    print(bcolors.FAIL + 'Insufficient MP' + bcolors.ENDC)
                    continue

                if spell.type == 'white':
                    mgk_heal(spell, player)
                else:
                    mgk_attack(spell, player, target_choice)
            # Items
            elif choice == 2:
                print(bcolors.OKBLUE + 'You chose', player.get_action(choice) + bcolors.ENDC)
                player.choose_items()
                item_choice = input_choice('item')
                if not item_choice:
                    continue
                item_choice -= 1
                try:
                    item = player.get_item(item_choice)
                except IndexError:
                    continue

                if player.get_item_qnt(item_choice) <= 0:
                    print(bcolors.FAIL + item.name, 'out of stock' + bcolors.ENDC)
                    continue

                if item.type == 'potion':
                    item_heal(item, player)
                elif item.type == 'mana':
                    item_mp_recover(item, player)
                elif item.type == 'attack':
                    item_attack(item, target_choice)
                player.decrement_item_qnt(item_choice)

            # Wrong choice
            else:
                continue

            if enemy_party[target_choice].get_hp() == 0:
                defeated_enemies.append(enemy_party[target_choice])

            # PLAYER WIN
            if len(defeated_enemies) == 3:
                print_battle_stats()
                print('===================================')
                print(bcolors.HEADER + bcolors.BOLD + 'VICTORY!' + bcolors.ENDC)
                print('===================================')
                running = False
                break

        for enemy in enemy_party:
            # ENEMY ATTACK
            enemy_choice = random.randrange(0, len(player_party) - 1)
            player = player_party[enemy_choice]
            enemy_dmg = enemy.generate_dmg()
            player.take_dmg(enemy_dmg)
            print(bcolors.FAIL + 'Enemy strikes', player.name, str(enemy_dmg) + bcolors.ENDC)

            # PLAYER DEFEAT
            if player.get_hp() == 0:
                print_battle_stats()
                print('===================================')
                print(bcolors.FAIL + bcolors.BOLD + 'DEFEAT!' + bcolors.ENDC)
                print('===================================')
                running = False
                break

        print_battle_stats()


# init game
battle()
