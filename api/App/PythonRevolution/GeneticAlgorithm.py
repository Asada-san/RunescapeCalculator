from App.PythonRevolution import Revolution_main as RevoMain
import AbilityBook
import time
# import copy
from random import shuffle, randint, choice
from joblib import Parallel, delayed
import multiprocessing
import numpy as np

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

N = 500
nParents = 30

Population = []
Parents = []
ParentDamage = []
Citizens = AbilityWeaponBook[KeyChoice]

nBar = 14

for i in range(0, N):
    if i == 0:
        Population.append(['Snap Shot', "Death's Swiftness", 'Corruption Shot', 'Fragmentation Shot', 'Greater Dazing Shot', 'Shadow Tendrils', 'Binding Shot', 'Rapid Fire', 'Piercing Shot', "Tuska's Wrath"])
    shuffle(Citizens)
    Population.append(Citizens[0:nBar])

NNN = 200
Stop = 0
MaxIter = 20
BestRotation = []
for k in range(0, NNN):

    start_bsub = time.time()

    num_cores = multiprocessing.cpu_count()

    Results = Parallel(n_jobs=num_cores)(delayed(RevoMain.fight_dummy)(user_input, subgroup,
                                                                       AbilityBook) for subgroup in Population)

    end_bsub = time.time()

    DamageDict = {}
    for i in range(0, N):
        if Results[i][2] is None:
            DamageDict.update({i: Results[i][0]['AADPT']})

    ParentIndices = sorted(DamageDict, key=DamageDict.get)[-1 - nParents: -1]

    for IDX in ParentIndices:
        ParentDamage.append(DamageDict[IDX])
        Parent = Results[IDX][0]['CycleBar']

        for ability in Results[IDX][0]['CycleRedundant']:
            Parent.remove(ability)

        Parents.append(Parent)

    if len(BestRotation) == 0:
        BestRotation = [max(ParentDamage), Parents[-1]]

    if max(ParentDamage) > BestRotation[0]:
        BestRotation = [max(ParentDamage), Parents[-1]]
        Stop = 0
    elif max(ParentDamage) == BestRotation[0] and k != 0:
        Stop += 1

    if Stop == MaxIter:
        break

    print(Stop, BestRotation)

    ScoreDict = {}
    AbilityScore = {}
    weighting = 0.5

    for i in range(0, nParents):

        for j, ability in enumerate(Parents[i]):

            if ability not in ScoreDict:
                ScoreDict.update({ability: 1})
            else:
                ScoreDict[ability] += 1

    WeightingBook = []
    for i in range(0, len(ScoreDict)):

        SlotAbilities = list(ScoreDict.keys())
        SlotWeightings = np.array(list(ScoreDict.values()))
        SlotWeightings = SlotWeightings / np.sum(SlotWeightings)

    SingleBar = []
    Population = []
    for m in range(0, N):
        SingleBar = []
        SlotAbilitiesLoop = SlotAbilities.copy()
        SlotWeightingsLoop = SlotWeightings.copy()

        while len(SingleBar) < 14 and len(SlotWeightingsLoop) > 0:
            Ability = np.random.choice(SlotAbilitiesLoop, 1, p=SlotWeightingsLoop)

            IDX = SlotAbilitiesLoop.index(Ability)

            SlotAbilitiesLoop.pop(IDX)
            SlotWeightingsLoop = np.delete(SlotWeightingsLoop, IDX)

            SlotWeightingsLoop = SlotWeightingsLoop / np.sum(SlotWeightingsLoop)

            SingleBar.append(Ability[0])

        randomA = randint(0, 100)

        if randomA < 100:
            slot1 = choice(range(0, 5))
            slot2 = choice(range(0, 8))

            SingleBar[slot1], SingleBar[slot2] = SingleBar[slot2], SingleBar[slot1]

        if randomA < 75:
            slot1 = choice(range(0, 5))
            slot2 = choice(range(0, 8))

            SingleBar[slot1], SingleBar[slot2] = SingleBar[slot2], SingleBar[slot1]

        if randomA < 50:
            slot1 = choice(range(0, 5))
            slot2 = choice(range(0, 8))

            SingleBar[slot1], SingleBar[slot2] = SingleBar[slot2], SingleBar[slot1]

        if randomA < 25:
            slot1 = choice(range(0, 5))
            slot2 = choice(range(0, 8))

            SingleBar[slot1], SingleBar[slot2] = SingleBar[slot2], SingleBar[slot1]

        if randomA % 20 == 0:
            shuffle(SingleBar)

        # if randomA % 2 == 0 and len(SingleBar) != 14:
        #     InsertIndex = choice(range(0, len(SingleBar)))
        #
        #     Ability = choice(Citizens)
        #
        #     if Ability in SingleBar:
        #         IDX = Citizens.index(Ability)
        #
        #         for j in range(IDX + 1, IDX + 1 + len(Citizens)):
        #             j = j % len(Citizens)
        #             if Citizens[j] not in SingleBar:
        #                 SingleBar.insert(InsertIndex, Citizens[j])
        #                 break
        #     else:
        #         SingleBar.insert(InsertIndex, Ability)

        Population.append(SingleBar)

    # pprint.pprint(Population)


# pprint.pprint(Population)
# print(SingleBar)
# pprint.pprint(ScoreDict)
# pprint.pprint(Parents)

# np.array(ParentDamage)
# NormalizedVector = ProbabilityArray / np.linalg.norm(ProbabilityArray)

print(f'Average Ability Damage Per Tick: {max(ParentDamage)}\n'
      f'The rotation: {Parents[-1]}\n'
      f'The rotation cycle: {Results[ParentIndices[-1]][0]["CycleRotation"]}\n'
      f'The loop time: {round(end_bsub - start_bsub, 2)}\n'
      f'The amount of loop iterations: {len(Results)}\n'
      f'Time per iteration: {round((end_bsub - start_bsub) / len(Results), 7)}\n'
      f'Number of abilities in list: {nBar}')







