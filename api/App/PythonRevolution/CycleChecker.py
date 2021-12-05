from App.PythonRevolution import CombatChecks, AttackCycle as Attack
from copy import deepcopy
import numpy as np
import time


def CycleCheck(bar, player, dummy, logger):
    """
    Checks for repeating cycles.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The Logger object.
    """

    cdTimes = [ability.cdTime for ability in bar.Rotation]

    # Tuple consisting of list of cd times, loop time, adrenaline and puncture stack
    condition = (cdTimes,
                 bar.Adrenaline,
                 dummy.nPuncture,
                 player.AbilCritBuff,
                 player.ArDamage)

    logger.Counter.append(logger.n)

    try:
        idx = logger.ConditionList.index(condition)
    except ValueError:
        idx = -1

    if idx == -1:
        logger.ConditionList.append(condition)
    else:  # A cycle has been found!
        logger.CycleFound = True
        logger.CycleTime = logger.n - logger.Counter[idx]  # The cycle time
        logger.Cycle1More = logger.CycleTime  # Set the time for the next cycle
        logger.CycleStart = logger.n  # Starting time of the next cycle
        logger.CycleConvergenceTime = logger.CycleStart - logger.CycleTime  # Convergence time

        if logger.DebugMode:
            logger.write(35, round(logger.CycleTime * .6, 1))


def CycleRotation(bar, player, dummy, logger, settings):
    """
    Checks if the verification cycle has to end or not and checks for unused abilities
    on the bar.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    """
    # The below is not performed in the last tick when cooldowns are checked again, causing small inaccuracies

    # Get damage done in current tick
    tickDamage = logger.CycleDamage - logger.CycleDamagePreviousTick
    logger.CycleDamagePerTick.append(tickDamage)

    # Subtract tick time
    logger.Cycle1More -= 1

    # Calculate new total damage up until current tick
    logger.CycleDamagePreviousTick = logger.CycleDamage
    logger.CycleDamageIncrement.append(logger.CycleDamagePreviousTick)

    for key, value in logger.AbilInfo.items():
        if key != 'Boosted':
            # tickAbilityDamage = logger.AbilInfo[key]['damage'] - \
            #                                         logger.PreviousAbilInfo[key]['damage']

            logger.CycleAbilityDamagePerTick[key]['damage'].append(logger.AbilInfo[key]['damage'])
            # if tickAbilityDamage != 0:
            #     logger.CycleAbilityDamagePerTick[key]['activations'] += 1

    logger.PreviousAbilInfo = deepcopy(logger.AbilInfo)

    if logger.Cycle1More == 0:
        # !!! important for accurate results, check 1 more time for possible bleeds/punctures
        # Status checks
        bar.TimerCheck(logger)  # CHECK GLOBAL COOLDOWN TIMER
        dummy.TimerCheck(logger)  # CHECK STUN AND BIND STATUS TIMERS
        player.TimerCheck(logger)  # CHECK PLAYER COOLDOWNS/BUFFS/BOOSTS/CHANNEL TIMERS

        # Check for any hits that need to inflict damage in the current tick
        Attack.PHitCheck(bar, dummy, player, logger, settings)

        # Check for redundant abilities (abilities which do not occur in the rotation)
        for j in range(0, bar.N):
            # If an ability has not been fired during the cycle verification
            if not logger.nFA[j]:
                logger.Redundant.extend([bar.Rotation[j].Name])

        settings.run = False

        if logger.DebugMode:
            logger.write(48)

    elif logger.n == settings.nMax:  # If the max runtime has been reached
        for attr, value in logger.AbilInfo.items():
            if value['activations'] == 0:
                logger.Redundant.extend([attr])









# loop.ConditionList.append([loop.cdTimes[0: bar.N].copy(), bar.Adrenaline, dummy.nPuncture, player.AbilCritBuff, loop.n])
# # start_time = time.time()
# # For every Array in ConditionList created at an previous attack cycle
# for i in range(0, loop.nAC - 1):
#     # CONDITION 1: If the adrenaline is equal
#     if loop.ConditionList[i][1] == loop.ConditionList[-1][1]:
#         # CONDITION 2: If the cooldown array is equal
#         if (loop.ConditionList[i][0] == loop.ConditionList[-1][0]).all():
#             # CONDITION 3: If the puncture stack is equal
#             if loop.ConditionList[i][2] == loop.ConditionList[-1][2]:
#                 # CONDITION 3: If the critical hit boost is equal
#                 if loop.ConditionList[i][3] == loop.ConditionList[-1][3]:
#                     loop.CycleFound = True  # A cycle has been found!
#                     loop.CycleTime = loop.ConditionList[-1][4] - loop.ConditionList[i][4]   # The cycle time
#                     loop.Cycle1More = loop.CycleTime                                # Set the time for the next cycle
#                     loop.CycleStart = loop.n                                        # Starting time of the next cycle
#                     loop.CycleConvergenceTime = loop.CycleStart - loop.CycleTime    # Convergence time
#
#                     # HTML.write(35, round(loop.CycleTime * .6, 1))
