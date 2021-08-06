from App.PythonRevolution import Revolution_main as RevoMain
import AbilityBook
import time
# import copy
import random
from random import choice

ability_list = AbilityBook

AbilityWeaponBook = {'melee_2h': [],
                     'melee_dual': [],
                     'melee_any': [],
                     'ranged_2h': [],
                     'ranged_dual': [],
                     'ranged_any': [],
                     'magic_2h': [],
                     'magic_dual': [],
                     'magic_any': []}

for ability in ability_list.values():
    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Strength', 'Attack', 'Constitution',
                                                                        'Defence'] and ability.Name not in ['Surge',
                                                                                                            'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Strength', 'Attack', 'Constitution',
                                                                          'Defence'] and ability.Name not in ['Surge',
                                                                                                              'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Strength', 'Attack',
                                                                                          'Constitution',
                                                                                          'Defence'] and ability.Name not in [
        'Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_any'].append(ability.Name)

    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Ranged', 'Constitution',
                                                                        'Defence'] and ability.Name not in ['Surge',
                                                                                                            'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Ranged', 'Constitution',
                                                                          'Defence'] and ability.Name not in ['Surge',
                                                                                                              'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Ranged', 'Constitution',
                                                                                          'Defence'] and ability.Name not in [
        'Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_any'].append(ability.Name)

    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Magic', 'Constitution',
                                                                        'Defence'] and ability.Name not in ['Surge',
                                                                                                            'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['magic_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Magic', 'Constitution',
                                                                          'Defence'] and ability.Name not in ['Surge',
                                                                                                              'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['magic_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Magic', 'Constitution',
                                                                                          'Defence'] and ability.Name not in [
        'Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['magic_any'].append(ability.Name)

for key in AbilityWeaponBook.keys():
    if key in ['melee_2h', 'melee_dual', 'melee_any']:
        # Trash upgradeable melee abilities
        if 'Fury' in AbilityWeaponBook[key] and 'Greater Fury' in AbilityWeaponBook[key]:
            AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Fury'))

        if 'Barge' in AbilityWeaponBook[key] and 'Greater Barge' in AbilityWeaponBook[key]:
            AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Barge'))

        if 'Flurry' in AbilityWeaponBook[key] and 'Greater Flurry' in AbilityWeaponBook[key]:
            AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Flurry'))

        # Trash 1 of the melee abilities which share a cooldown
        # if 'Kick' in AbilityWeaponBook[key] and 'Backhand' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Backhand'))
        #
        # if 'Forceful Backhand' in AbilityWeaponBook[key] and 'Stomp' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Forceful Backhand'))

        # Trash all melee ultimate abilities except berserk
        # for ability in AbilityWeaponBook[key]:
        #     if ability_list[ability].Type == 'Ultimate' and not ability == 'Berserk':
        #         AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index(ability))

    if key in ['ranged_2h', 'ranged_dual', 'ranged_any']:
        # Trash upgradeable ranged abilities
        if 'Dazing Shot' in AbilityWeaponBook[key] and 'Greater Dazing Shot' in AbilityWeaponBook[key]:
            AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Dazing Shot'))

        # Trash 1 of the ranged abilities which share a cooldown
        # if 'Binding Shot' in AbilityWeaponBook[key] and 'Demoralise' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Binding Shot'))
        #
        # if 'Tight Bindings' in AbilityWeaponBook[key] and 'Rout' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Tight Bindings'))

        # Trash all ranged ultimate abilities except Death's Swiftness
        # for ability in AbilityWeaponBook[key]:
        #     if ability_list[ability].Type == 'Ultimate' and not ability == 'Death\'s Swiftness':
        #         AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index(ability))

    # if key in ['magic_2h', 'magic_dual', 'magic_any']:
    #     # Trash 1 of the magic abilities which share a cooldown
    #     if 'Impact' in AbilityWeaponBook[key] and 'Shock' in AbilityWeaponBook[key]:
    #         AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Impact'))
    #
    #     if 'Deep Impact' in AbilityWeaponBook[key] and 'Horror' in AbilityWeaponBook[key]:
    #         AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Deep Impact'))
    #
    #     # Trash all ranged ultimate abilities except Sunshine
    #     for ability in AbilityWeaponBook[key]:
    #         if ability_list[ability].Type == 'Ultimate' and not ability == 'Sunshine':
    #             AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index(ability))

user_input = {
    # PLAYER OBJECT RELATED

    'afkStatus': False,
    'baseDamage': 1000,
    'ShieldArmourValue': 491,
    'DefenceLevel': 99,
    'StrengthBoost': 0,
    'MagicBoost': 0,
    'RangedBoost': 0,
    'StrengthPrayer': 1,
    'MagicPrayer': 1,
    'RangedPrayer': 1,

    'StrengthCape': False,
    'RoV': False,  # --> Ring of Vigour
    'MSoA': False,  # --> Masterwork Spear of Annihilation
    'Aura': 'None',
    'Level20Gear': False,
    'Grimoire': False,
    'Precise': 0,
    'Equilibrium': 0,
    'Biting': 0,
    'Flanking': 0,
    'Lunging': 0,
    'Aftershock': 0,
    'PlantedFeet': False,

    # DUMMY OBJECT RELATED

    'movementStatus': False,
    'stunbindStatus': False,
    'nTargets': 1,

    # SCRIPT RELATED

    'simulationTime': 0,
    'adrenaline': 0,
    'HTMLwrite': False
}

KeyChoice = 'ranged_2h'

user_input.update({'switchStatus': False})

# AbilityWeaponBook_sorted = {}
# for key in AbilityWeaponBook.keys():
#     abildamage_dict = {}
#     for ability in AbilityWeaponBook[key]:
#         abildamage = sum(ability_list[ability].DamAvg) + sum(ability_list[ability].DoTAvg)
#
#         abildamage_dict.update({ability: abildamage})
#
#     sorted_list = sorted(abildamage_dict.items(), key=lambda x: x[1])
#
#     for i, pair in enumerate(sorted_list):
#         if pair[0] in ['Death\'s Swiftness', 'Berserk', 'Sunshine']:
#             sorted_list.append(pair)
#             sorted_list.pop(i)
#
#     sorted_list = list(reversed(sorted_list))
#
#     for i, pair in enumerate(sorted_list):
#         sorted_list[i] = sorted_list[i][0]
#
#     AbilityWeaponBook[key] = sorted_list
#
#     pprint.pprint(AbilityWeaponBook[key])



runtime = 10000
MAX_AADPT = 0
MAXrot = []
start_bsub = time.time()
loop_counter = 0

current_selection = AbilityWeaponBook[KeyChoice].copy()
random.shuffle(current_selection)
nRevo = 14  # len(current_selection)

opt_bar_compare = current_selection[:nRevo]
opt_bar = current_selection[:nRevo]
or_loop = current_selection[:nRevo]
opt_bar_move = current_selection[:nRevo]
EndLoop = False


nAbil = len(current_selection)

opt_rot_new = []
print(current_selection)

# While the ability bar is not optimal
while not EndLoop:
    counter = 0
    not_better = 0

    loop_counter += 1

    # For every possible ability
    for i in range(0, nAbil):
        print(f'ability numero: {i}')

        # For every slot on the revolution bar, counting backwards
        for j in range(nRevo - 1, -1, -1):

            # The rotation to be checked is the current optimal rotation
            bar_check = opt_bar.copy()
            
            # If ability i is not in the current bar
            if current_selection[i] not in bar_check:
                # Pop the ability in the last slot
                bar_check.pop(-1)

                # Insert the ability on slot j
                bar_check.insert(j, current_selection[i])

            else:
                # Get the current index of the ability
                IDX = bar_check.index(current_selection[i])

                # If the index is not equal to j
                if IDX != j:
                    # Pop the ability in its current slot
                    bar_check.pop(IDX)

                    # Insert the ability on slot j
                    bar_check.insert(j, current_selection[i])
                else:  # Else its the current bar
                    continue

            # Calculate the results of the new bar
            Results, warning, ermes = RevoMain.fight_dummy(user_input, bar_check, ability_list)

            counter += 1

            # If the result shows a higher AADPT than the previous ones
            if Results['AADPT'] > MAX_AADPT:
                MAX_AADPT = Results['AADPT']

                # Delete redundant abilities and fill bar with others
                for ability in Results['CycleRedundant']:
                    bar_check.remove(ability)

                    Ability = choice(current_selection)

                    if Ability in bar_check:
                        IDX = current_selection.index(Ability)

                        for m in range(IDX + 1, IDX + 1 + len(current_selection)):
                            m = m % len(current_selection)
                            if current_selection[m] not in bar_check:
                                bar_check.append(current_selection[m])
                                break
                    else:
                        bar_check.append(Ability)

                # The new optimal bar
                opt_bar_new = bar_check.copy()

                print(f'Loop iterations: {loop_counter}      Index: {counter}\n'
                      f'New maximum damage per tick: {MAX_AADPT}\n'
                      f'The new optimal rotation: {opt_bar_new}')

                # # Optimal index j
                # optimalIDX = j

                # Since a new optimal bar has been found, we need to loop again to make sure its the real bar
                EndLoop = False
            else:
                not_better += 1

            # If looped through all possible changes without getting a new optimal bar
            if not_better == nAbil * nRevo and not optimal_move:
                EndLoop = True
            # Else set new optimal bar
            elif i == nAbil - 1 and j == 0:
                opt_bar = opt_bar_new.copy()

    # If EndLoop is true, skip stuff beneath and go back to while loop check
    if EndLoop:
        continue

    counter = 0

    optimal_move = False
    nCheck = 0
    # For every slot on the bar
    for k in range(0, nRevo):
        print(f'ability in bar numero: {k}')

        # For every other slot on the bar
        for l in range(k + 1, nRevo):
            counter += 1
            # if not k == optimalIDX or not l == optimalIDX:

            # Switcharoo the 2 abilities on index k and l
            opt_bar[l], opt_bar[k] = opt_bar[k], opt_bar[l]

            # Calculate the results of the new bar
            Results, warning, ermes = RevoMain.fight_dummy(user_input, opt_bar, ability_list)

            # If the result shows a higher AADPT than the previous ones
            if Results['AADPT'] > MAX_AADPT:
                # A new optimal bar has been found using the move algorithm
                optimal_move = True

                MAX_AADPT = Results['AADPT']

                # Delete redundant abilities and fill bar with others
                for ability in Results['CycleRedundant']:
                    opt_bar.remove(ability)

                    Ability = choice(current_selection)

                    if Ability in opt_bar:
                        IDX = current_selection.index(Ability)

                        for m in range(IDX + 1, IDX + 1 + len(current_selection)):
                            m = m % len(current_selection)
                            if current_selection[m] not in opt_bar:
                                opt_bar.append(current_selection[m])
                                break
                    else:
                        opt_bar.append(Ability)

                # Set the new optimal bar due to the move algorithm
                opt_bar_move = opt_bar.copy()

                # Switch the 2 abils back
                # opt_bar[k], opt_bar[l] = opt_bar[l], opt_bar[k]

                print(f'Loop iterations: {loop_counter}      Move index: {counter}\n'
                      f'New maximum damage per tick: {MAX_AADPT}\n'
                      f'The new optimal rotation: {opt_bar_move}')

            # elif Results['AADPT'] < MAXdpt:
            #     if l == k + 1:
            #         nCheck += 1
            #     opt_bar[k], opt_bar[l] = opt_bar[l], opt_bar[k]
            #     break

            else:
                # Switch the 2 abils back
                opt_bar[k], opt_bar[l] = opt_bar[l], opt_bar[k]

    # If an optimal bar has been found by the move algorithm, set new opt bar
    if optimal_move:
        opt_bar = opt_bar_move.copy()

# for i in range(0, len(opt_bar)):
#     dummy_damage, ermes = main.fight_dummy(opt_bar[:-1-i], runtime, ability_list)
#
#     if dummy_damage == MAXdpt:
#         opt_bar = opt_bar[:-1-i].copy()
#     else:
#
#         break

end_bsub = time.time()

print(f'Average Ability Damage Per Tick: {round(MAX_AADPT, 3)}\n'
      f'The rotation: {opt_bar}\n'
      f'The loop time: {round(end_bsub - start_bsub, 2)}\n'
      f'Number of abilities in list: {nAbil}')

print(f'\nOriginal optimal loop: {or_loop}')
