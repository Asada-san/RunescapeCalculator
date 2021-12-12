import numpy as np


def StandardChannelDamAvgCalc(Object, player, logger):
    """
    Calculates the average hit of a standard/channeled effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object.
    :param logger: The DoList object.
    :param Type: Type of ability for which the average has to be calculated.
    :return: Average Standard/Channeled hit.
    """

    Max = Object.DamMax.copy()
    Min = Object.DamMin.copy()

    if Object.Name != 'Bash':  # Bash ability has its own base damage
        Max *= player.BaseDamageEffective * (1 + player.Rr * 0.025) * player.BerserkersFury
        Min *= player.BaseDamageEffective * (1 + player.Rr * 0.025) * player.BerserkersFury
    else:
        Max *= player.BashBaseDamage * (1 + player.Rr * 0.025) * player.BerserkersFury
        Min *= player.BashBaseDamage * (1 + player.Rr * 0.025) * player.BerserkersFury

    # Level boost due to potions/aura's
    Max += 8 * player.LevelBoost
    Min += 4 * player.LevelBoost

    CritCap = player.CritCap  # Critical hit damage cap
    DmgCap = 10000  # Normal hit damage cap

    if player.PerkPrecise:  # Increase min by 1.5% per rank
        PrMinIncrease = player.Pr * 0.015 * Max
        Min = Min + PrMinIncrease

    # ---------- Formula used to calculate averages, yoinked from the rs wiki ------------
    if player.Aura == 'Equilibrium':  # If the equilibrium aura is active
        pNatCrit = min(Max / (40 * (Max - Min)) + 0.0125, 1)
    elif player.PerkEquilibrium:  # Increase min by 3% per rank and decrease max by 1% per rank
        pNatCrit = min(((25 - player.Er) * Max) / (
                    500 * (Max - Min)) + player.Er / 2000, 1)

        EqMinIncrease = player.Er * 0.03 * (Max - Min)
        EqMaxDecrease = player.Er * 0.01 * (Max - Min)
        Max = Max - EqMaxDecrease
        Min = Min + EqMinIncrease
    else:
        pNatCrit = min((0.05 * Max) / (Max - Min), 1)

    # If the player has a boost from Berserk or w/e, the aura boost is replaced by the ability boost
    if player.Boost:  # If the player has a damage boost
        Max *= player.getBoost() * player.Boost1X
        Min *= player.getBoost() * player.Boost1X
    else:
        Max *= player.BaseBoost * player.Boost1X
        Min *= player.BaseBoost * player.Boost1X

    CritNatMin = max(Min + (1 - pNatCrit) * (Max - Min), Min)

    CritForcedMin = (Min + 0.95 * (Max - Min))
    CritForcedMax = (Min + (0.95 * (Max - Min)) / 0.95)

    z1 = (CritCap - CritForcedMin) / (CritForcedMax - CritForcedMin)
    z2 = (CritCap - CritNatMin) / (Max - CritNatMin)

    y = (DmgCap - Min) / (CritNatMin - Min)

    pForcedCrit = min(player.ForcedCritBuff + player.AbilCritBuff + player.InitCritBuff, 1)

    # If the ability Greater Fury was used, calculate new CritBuff and return immediately
    if player.GreaterFuryCritCheck:
        player.AbilCritBuff += (pForcedCrit + (1 - pForcedCrit) * pNatCrit) + (1 - pForcedCrit) * (1 - pNatCrit) * 0.1
        player.GreaterFuryCritCheck = False
        return None

    # If an adrenaline buff due to Meteor Strike, Tsunami or Incendiary Shot is active, calculate extra adrenaline and return immediately
    if player.CritAdrenalineBuff:
        player.BasicAdrenalineGain += (pForcedCrit + (1 - pForcedCrit) * pNatCrit) * 10
        player.CritAdrenalineBuff = False
        return None

    AvgCalc1 = max(0, min(1 - z1, 1)) * CritCap + min(max(0, z1), 1) * (min(CritCap, CritForcedMin) + min(CritCap, CritForcedMax)) / 2
    AvgCalc2 = max(0, min(1 - z2, 1)) * CritCap + min(max(0, z2), 1) * (min(CritCap, CritNatMin) + min(CritCap, Max)) / 2
    AvgCalc3 = max(0, min(1 - y, 1)) * DmgCap + min(max(0, y), 1) * (min(DmgCap, Min) + min(DmgCap, CritNatMin)) / 2

    Avg = pForcedCrit * AvgCalc1 + (1 - pForcedCrit) * (pNatCrit * AvgCalc2 + (1 - pNatCrit) * AvgCalc3)
    # ------------------------------------------------------------------------------------

    if logger.DebugMode:
        logger.write(13, [Object.Name, round(Avg, 2), round(pForcedCrit, 4), round(pNatCrit, 4)])

    return Avg


def BleedDamAvgCalc(Object, player, logger):
    """
    Calculates the average hit of a bleed effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object
    :param logger: The Logger object
    :return: Average bleed hits
    """

    Max = Object.DamMax.copy()
    Min = Object.DamMin.copy()

    # If the player has a boost from berserker or w/e, the aura boost is replaced by the ability boost
    if player.Boost:
        Max *= player.BaseDamage
        Min *= player.BaseDamage
    else:
        Max *= player.BaseBoost * player.BaseDamage
        Min *= player.BaseBoost * player.BaseDamage

    ################## Calculate averages ########################
    Avg = (Max + Min) / 2

    if logger.DebugMode:
        logger.write(17, [Object.Name, Avg])

    return Avg


def PunctureDamAvgCalc(Object, player, logger):
    """
    Calculates the average hit of an puncture effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object
    :param logger: The Logger object
    :return: Average puncture hits
    """

    Avg = []
    if Object.Type == 4 and Object.Name == 'Greater Dazing Shot':
        Max = np.array([7 / 15 * 0.072, 5 / 15 * 0.072, 2 / 15 * 0.072, 1 / 15 * 0.072]) * player.BaseBoost * player.BaseDamage
        Min = np.array([7 / 15 * 0.058, 5 / 15 * 0.058, 2 / 15 * 0.058, 1 / 15 * 0.058]) * player.BaseBoost * player.BaseDamage

        for i in range(0, Object.nD):
            Avg.append((Max[i] + Min[i]) / 2)

            if logger.DebugMode:
                logger.write(17, [Object.Name, round(Avg[i], 2)])

    return Avg


def SpecialDamAvgCalc(Object, player, logger):
    """
    Calculates the average hit of a bleed effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object
    :param logger: The Logger object
    :return: Average bleed hits
    """

    Max = Object.DamMax.copy()
    Min = Object.DamMin.copy()

    # If the player has a boost from berserker or w/e, the aura boost is replaced by the ability boost
    if player.PerkAftershock and Object.Name == 'Aftershock':
        Max *= player.Ar * player.BaseDamage
        Min *= player.Ar * player.BaseDamage
    else:
        Max *= player.BaseDamage
        Min *= player.BaseDamage

    ################## Calculate averages ########################
    Avg = (Max + Min) / 2

    if logger.DebugMode:
        logger.write(54, [Object.Name, Avg])

    return Avg
