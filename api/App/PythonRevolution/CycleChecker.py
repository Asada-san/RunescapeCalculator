from App.PythonRevolution import CombatChecks, AttackCycle as Attack
from copy import deepcopy
import numpy as np
import time


def CycleCheck(player, dummy, logger, settings):
    """
    Checks for repeating cycles.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The Logger object.
    """

    cdTimes = [ability.cdTime for ability in player.Bar.Abilities]
    cdTimes.extend([player.Special[special].cdTime for special in player.Special])

    # Tuple consisting of list of cd times, loop time, adrenaline and puncture stack
    condition = (cdTimes,
                 player.Adrenaline,
                 dummy.nPuncture,
                 player.Bar.CritIncreaseNextAbility,
                 player.AsDamage,
                 player.PocketHitCounter,
                 player.Boost,
                 player.Boost1)

    logger.Counter.append(logger.n)

    try:
        idx = logger.ConditionList.index(condition)
    except ValueError:
        idx = -1

    if idx == -1:
        logger.ConditionList.append(condition)
    else:  # A cycle has been found!
        settings.run = False

        logger.CycleFound = True
        logger.CycleTime = logger.n - logger.Counter[idx]  # The cycle time
        logger.CycleStart = logger.n  # Starting time of the next cycle
        logger.CycleConvergenceTime = logger.CycleStart - logger.CycleTime  # Convergence time

        if True:
            dummy.getResults(logger.CycleConvergenceTime, logger.CycleTime)
            logger.getResults(logger.CycleConvergenceTime, logger.CycleTime)

        if logger.DebugMode:
            logger.Text += f'<li style="color: {logger.TextColor["cycle"]};">CYCLE FOUND!!! Terminating intense fight with dummy.</li>'


# def CycleRotation(bar, player, dummy, logger, settings):
#     """
#     Checks if the verification cycle has to end or not and checks for unused abilities
#     on the bar.
#
#     :param bar: The Bar object.
#     :param dummy:  The Dummy object.
#     :param player: The Player object.
#     :param logger: The Logger object.
#     :param settings: The Settings object.
#     """
#     # The below is not performed in the last tick when cooldowns are checked again, causing small inaccuracies
#
#     # Subtract tick time
#     logger.Cycle1More -= 1
#
#     if logger.Cycle1More == 0:
#         # !!! important for accurate results, check 1 more time for possible bleeds/punctures
#         # Status checks
#         bar.TimerCheck(logger)  # CHECK GLOBAL COOLDOWN TIMER
#         dummy.TimerCheck(logger)  # CHECK STUN AND BIND STATUS TIMERS
#         player.TimerCheck(dummy, logger)  # CHECK PLAYER COOLDOWNS/BUFFS/BOOSTS/CHANNEL TIMERS
#
#         # Check for any hits that need to inflict damage in the current tick
#         Attack.PHitCheck(bar, dummy, player, logger, settings)
#
#         # Check for redundant abilities (abilities which do not occur in the rotation)
#         for j in range(0, bar.N):
#             # If an ability has not been fired during the cycle verification
#             if not logger.nFA[j]:
#                 logger.Redundant.extend([bar.Rotation[j].Name])
#
#         settings.run = False
#
#         if logger.DebugMode:
#             logger.Text += f'<li style="color: {logger.TextColor["cycle"]};">VERIFICATION LOOP COMPLETED: RETURN RESULTS</li>'
#
#     elif logger.n == settings.nMax:  # If the max runtime has been reached
#         for attr, value in logger.AbilInfo.items():
#             if value['activations'] == 0:
#                 logger.Redundant.extend([attr])
