from App.PythonRevolution import Revolution_main as RevoMain
import AbilityBook
import time
import itertools
# import copy
from joblib import Parallel, delayed
import multiprocessing

# cp = cProfile.Profile()
# cp.enable()

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
    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Strength', 'Attack', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Strength', 'Attack', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Strength', 'Attack', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['melee_any'].append(ability.Name)

    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Ranged', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Ranged', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Ranged', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['ranged_any'].append(ability.Name)

    if ability.Equipment in ['any', '2h', 'None'] and ability.Style in ['Magic', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['magic_2h'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', 'None'] and ability.Style in ['Magic', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
        AbilityWeaponBook['magic_dual'].append(ability.Name)

    if ability.Equipment in ['any', 'dual', '2h', 'None', 'shield'] and ability.Style in ['Magic', 'Constitution', 'Defence'] and ability.Name not in ['Surge', 'Escape'] and 'Lesser' not in ability.Name:
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

        # # Trash 1 of the melee abilities which share a cooldown
        # if 'Kick' in AbilityWeaponBook[key] and 'Backhand' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Backhand'))
        # 
        # if 'Forceful Backhand' in AbilityWeaponBook[key] and 'Stomp' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Forceful Backhand'))
        # 
        # # Trash all melee ultimate abilities except berserk
        # for ability in AbilityWeaponBook[key]:
        #     if ability_list[ability].Type == 'Ultimate' and not ability == 'Berserk':
        #         AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index(ability))

    if key in ['ranged_2h', 'ranged_dual', 'ranged_any']:
        # Trash upgradeable ranged abilities
        if 'Dazing Shot' in AbilityWeaponBook[key] and 'Greater Dazing Shot' in AbilityWeaponBook[key]:
            AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Dazing Shot'))

        # # Trash 1 of the ranged abilities which share a cooldown
        # if 'Binding Shot' in AbilityWeaponBook[key] and 'Demoralise' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Binding Shot'))
        # 
        # if 'Tight Bindings' in AbilityWeaponBook[key] and 'Rout' in AbilityWeaponBook[key]:
        #     AbilityWeaponBook[key].pop(AbilityWeaponBook[key].index('Tight Bindings'))
        # 
        # # Trash all ranged ultimate abilities except Death's Swiftness
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
    'RoV': False,                # --> Ring of Vigour
    'MSoA': False,               # --> Masterwork Spear of Annihilation
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

current_selection = AbilityWeaponBook[KeyChoice].copy()
nAbil = len(current_selection)

opt_rot = []

nRevo = 4

abilCDtime = []
for ability in AbilityWeaponBook[KeyChoice]:

    abilCDtime.append(ability_list[ability].cdMax)

    abilCDtime = list(reversed(sorted(abilCDtime)))

runtime = sum(abilCDtime[:nRevo])

start_bsub = time.time()

num_cores = multiprocessing.cpu_count()

dummy_damage = Parallel(n_jobs=num_cores)(delayed(RevoMain.fight_dummy)(user_input, subset, ability_list) for subset in itertools.permutations(current_selection, nRevo))

end_bsub = time.time()

IDX = dummy_damage.index(max(dummy_damage))

for i, subset in enumerate(itertools.permutations(current_selection, nRevo)):
    if i == IDX:
        opt_rot = subset

print(f'MAX Damage Per Tick: {max(dummy_damage)}\n'
      f'The rotation: {opt_rot}\n'
      f'The loop time: {round(end_bsub - start_bsub, 2)}\n'
      f'The amount of loop iterations: {len(dummy_damage)}\n'
      f'Time per iteration: {round((end_bsub - start_bsub) / len(dummy_damage), 7)}\n'
      f'Runtime per iteration: {runtime}\n'
      f'Number of abilities in list: {nAbil}')

# cp.disable()
# cp.print_stats(sort='cumtime')
