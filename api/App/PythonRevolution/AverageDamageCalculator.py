import numpy as np


def StandardChannelDamAvgCalc(Object, player, logger, Type=None):
    """
    Calculates the average hit of a standard/channeled effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object.
    :param logger: The DoList object.
    :param Type: Type of ability for which the average has to be calculated.
    :return: Average Standard/Channeled hit.
    """

    if Type is None:
        Max = Object.DamMax.copy()
        Min = Object.DamMin.copy()
    elif Type == 'StunBind':
        Max = Object.StunBindDamMax.copy()
        Min = Object.StunBindDamMin.copy()
    elif Type == 'SideTarget':
        Max = Object.SideTargetMax.copy()
        Min = Object.SideTargetMin.copy()
    else:
        Max = [0]
        Min = [0]

    if Object.Name != 'Bash':  # Bash ability has its own base damage
        Max *= player.BaseDamageEffective * (1 + player.Rr * 0.025) * player.BerserkersFury
        Min *= player.BaseDamageEffective * (1 + player.Rr * 0.025) * player.BerserkersFury
    else:
        Max *= player.BashBaseDamage * (1 + player.Rr * 0.025) * player.BerserkersFury
        Min *= player.BashBaseDamage * (1 + player.Rr * 0.025) * player.BerserkersFury

    # Level boost due to potions/aura's
    Max += 8 * player.LevelBoost
    Min += 4 * player.LevelBoost

    Avg = []
    CritCap = player.CritCap  # Critical hit damage cap
    DmgCap = 10000  # Normal hit damage cap
    for i in range(0, len(Max)):
        if player.PerkPrecise:  # Increase min by 1.5% per rank
            PrMinIncrease = player.Pr * 0.015 * Max[i]
            Min[i] = Min[i] + PrMinIncrease

        # ---------- Formula used to calculate averages, yoinked from the rs wiki ------------
        if player.Aura == 'Equilibrium':  # If the equilibrium aura is active
            pNatCrit = min(Max[i] / (40 * (Max[i] - Min[i])) + 0.0125, 1)
        elif player.PerkEquilibrium:  # Increase min by 3% per rank and decrease max by 1% per rank
            pNatCrit = min(((25 - player.Er) * Max[i]) / (
                        500 * (Max[i] - Min[i])) + player.Er / 2000, 1)

            EqMinIncrease = player.Er * 0.03 * (Max[i] - Min[i])
            EqMaxDecrease = player.Er * 0.01 * (Max[i] - Min[i])
            Max[i] = Max[i] - EqMaxDecrease
            Min[i] = Min[i] + EqMinIncrease
        else:
            pNatCrit = min((0.05 * Max[i]) / (Max[i] - Min[i]), 1)

        # If the player has a boost from Berserk or w/e, the aura boost is replaced by the ability boost
        if player.Boost:  # If the player has a damage boost
            Max[i] *= player.BoostX * player.Boost1X
            Min[i] *= player.BoostX * player.Boost1X
        else:
            Max[i] *= player.BaseBoost * player.Boost1X
            Min[i] *= player.BaseBoost * player.Boost1X

        CritNatMin = max(Min[i] + (1 - pNatCrit) * (Max[i] - Min[i]), Min[i])

        CritForcedMin = (Min[i] + 0.95 * (Max[i] - Min[i]))
        CritForcedMax = (Min[i] + (0.95 * (Max[i] - Min[i])) / 0.95)

        z1 = (CritCap - CritForcedMin) / (CritForcedMax - CritForcedMin)
        z2 = (CritCap - CritNatMin) / (Max[i] - CritNatMin)

        y = (DmgCap - Min[i]) / (CritNatMin - Min[i])

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
        AvgCalc2 = max(0, min(1 - z2, 1)) * CritCap + min(max(0, z2), 1) * (min(CritCap, CritNatMin) + min(CritCap, Max[i])) / 2
        AvgCalc3 = max(0, min(1 - y, 1)) * DmgCap + min(max(0, y), 1) * (min(DmgCap, Min[i]) + min(DmgCap, CritNatMin)) / 2

        Avg.append(pForcedCrit * AvgCalc1 + (1 - pForcedCrit) * (
                    pNatCrit * AvgCalc2 + (1 - pNatCrit) * AvgCalc3))
        # ------------------------------------------------------------------------------------

        if logger.DebugMode:
            logger.write(13, [Object.Name, round(Avg[i], 2), round(pForcedCrit, 4), round(pNatCrit, 4)])

    return Avg


def BleedDamAvgCalc(Object, player, logger):
    """
    Calculates the average hit of a bleed effect of an ability.

    :param Object: Hit OR Ability class object.
    :param player: The Player object
    :param logger: The Logger object
    :return: Average bleed hits
    """

    Max = Object.DoTMax.copy()
    Min = Object.DoTMin.copy()

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
    if Object.Puncture and Object.Name == 'Greater Dazing Shot':
        Max = np.array([7 / 15 * 0.072, 5 / 15 * 0.072, 2 / 15 * 0.072, 1 / 15 * 0.72]) * player.BaseBoost * player.BaseDamage
        Min = np.array([7 / 15 * 0.058, 5 / 15 * 0.058, 2 / 15 * 0.058, 1 / 15 * 0.58]) * player.BaseBoost * player.BaseDamage

        for i in range(0, Object.nD):
            Avg.append((Max[i] + Min[i]) / 2)

            if logger.DebugMode:
                logger.write(17, [Object.Name, round(Avg[i], 2)])

    return Avg
