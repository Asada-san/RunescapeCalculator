import numpy as np


def StandardChannelDamAvgCalc(Ability, player, Do, Type=None, IDX=None, Multiplier=0):
    """
    Calculates the average hit of a standard/channeled effect of an ability.

    :param player: The Player object.
    :param Do: The DoList object.
    :param Type: Type of ability for which the average has to be calculated.
    :param IDX: Index of the average hit to be calculated.
    :param Multiplier: Damage multiplier for several abilities.
    :return: Average Standard/Channeled hit.
    """

    if IDX is None:
        Max = Ability.DamMax.copy()
        Min = Ability.DamMin.copy()
    else:
        if Type == 'Normal':
            Max = np.array([Ability.DamMax[IDX].copy()])
            Min = np.array([Ability.DamMin[IDX].copy()])
        elif Type == 'StunBind':
            Max = Ability.StunBindDamMax.copy()
            Min = Ability.StunBindDamMin.copy()
        elif Type == 'Salt the Wound':  # Min = .036   Max = .18  Avg = .108
            Max = Ability.DamMax.copy() + .18 * Multiplier  # Puncturestack
            Min = Ability.DamMin.copy() + .036 * Multiplier  # PunctureStack
        elif Type == 'Greater Ricochet':  # Min = .1    Max = .5    Avg = .3
            Max = np.array([.5])
            Min = np.array([.1])
        else:
            Max = Ability.SideTargetMax.copy()
            Min = Ability.SideTargetMin.copy()

    # Manually calculate the Max and Min of Shadow Tendrils
    if Ability.Name in {'Shadow Tendrils'}:
        Max[0] = 0.1 * Max[0] * 2 + .18 * Max[0] * 3 + .216 * Max[0] * 4 + .504 * Max[0] * 5
        Min[0] = 0.1 * Min[0] * 2 + .18 * Min[0] * 3 + .216 * Min[0] * 4 + .504 * Min[0] * 5

    if player.PerkFlanking:
        if Ability.Name in {'Backhand', 'Impact', 'Binding Shot'}:
            Ability.Stun = False  # Abilities above lose their stun effect

            for i in range(0,
                           Ability.nS):  # Increase min by 8% per rank, max by 40% per rank
                Max[i] += 0.4 * player.Fr
                Min[i] += 0.08 * player.Fr

        if Ability.Name in {'Forceful Backhand', 'Deep Impact', 'Tight Bindings'}:
            Ability.Stun = False  # Abilities above lose their stun effect

            for i in range(0,
                           Ability.nS):  # Increase min by 6% per rank, max by 30% per rank
                Max[i] += 0.3 * player.Fr
                Min[i] += 0.06 * player.Fr

    if Ability.Name == 'Debilitate' and player.PerkShieldBashing:
        Max[0] += 0.15 * player.SBr
        Min[0] += 0.15 * player.SBr

    if Ability.Name != 'Bash':  # Bash ability has its own base damage
        Max = Max * player.BaseDamageEffective * (
                    1 + player.Rr * 0.025) * player.BerserkersFury
        Min = Min * player.BaseDamageEffective * (
                    1 + player.Rr * 0.025) * player.BerserkersFury
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

        pForcedCrit = min(player.ForcedCritBuff + player.AbilCritBuff, 1)

        # If the ability Greater Fury was used, calculate new CritBuff and return immediately
        if player.GreaterFuryCritCheck:
            player.AbilCritBuff = (pForcedCrit + (1 - pForcedCrit) * pNatCrit) + (1 - pForcedCrit) * (1 - pNatCrit) * 0.1
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

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {round(Avg[i], 2)}, pForced: {round(pForcedCrit, 4)}, pNat: {round(pNatCrit, 4)}</li>'

    return Avg


def BleedDamAvgCalc(Ability, player, Do):
    """
    Calculates the average hit of a bleed effect of an ability.

    :param player: The Player object
    :param Do: TList object
    :return: Average bleed hits
    """

    Max = Ability.DoTMax.copy()
    Min = Ability.DoTMin.copy()
    Avg = []
    nExtend = 0  # Variable used for bleed extensions

    if player.PerkLunging and Ability.Name in {'Dismember', 'Combust', 'Fragmentation Shot'}:
        # Bleeds of Combust and Fragmentation Shot are multiplied by 1.5 upon walking instead of 2
        if Ability.Name != 'Dismember':
            Ability.BleedOnMove = 1.5

        Max[0] += 0.2 * player.Lr  # Increase max hit by 0.2 for every rank

    # If the player has a boost from berserker or w/e, the aura boost is replaced by the ability boost
    if player.Boost:
        Max *= player.BaseDamage
        Min *= player.BaseDamage
    else:
        Max *= player.BaseBoost * player.BaseDamage
        Min *= player.BaseBoost * player.BaseDamage

    ####################### Bleed boosts #########################
    if player.StrengthCape and Ability.Name == 'Dismember':
        nExtend += 3  # Add 3 hits to the Dismember ability

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability change: Extended {Ability.Name} by 3 hits</li>'

    if player.MSoA and Ability.Name in {'Dismember', 'Blood Tendrils', 'Slaughter'}:
        nExtend += 2  # Add 2 hits to the Dismember, Blood Tendrils and Slaughter abilities

        # If Blood Tendrils, extend damage arrays
        if Ability.Name == 'Blood Tendrils':
            Max = np.append(Max, Max[-3: -1])
            Min = np.append(Min, Min[-3: -1])

            Ability.nD += nExtend
            Ability.nT += nExtend

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability change: Extended {Ability.Name} by 2 hits</li>'

    ################## Calculate averages ########################
    if Ability.Name in {'Massacre', 'Deadshot'}:  # Simply bleed max / amount of hits
        Avg = [Max[0] / Ability.nD] * Ability.nD

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {Ability.nD}x {round(Avg[0], 2)}</li>'

    elif Ability.Name in {'Blood Tendrils', 'Corruption Shot', 'Corruption Blast',
                       'Incendiary Shot'}:  # Simply max + min / 2
        for i in range(0, Ability.nD):
            Avg.append(((Max[i] + Min[i]) / 2))

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {Avg[i]}</li>'

    elif Ability.Name in {'Death\'s Swiftness', 'Sunshine'}:  # Simply avg of max + min
        Avg = [(Max[0] / Ability.nD + Min[0] / Ability.nD) / 2] * Ability.nD

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {Ability.nD}x {round(Avg[0], 2)}</li>'

    else:  # Else the bleed is 1/max + ((max-1)/max) * (1+(max-1)/2)) / amount of hits
        Avg = [(Min[0] / Max[0] * Min[0] + ((Max[0] - Min[0]) / Max[0]) * (
                    Min[0] + (Max[0] - Min[0]) / 2)) / Ability.nD] * (Ability.nD + nExtend)

        Ability.nD += nExtend
        Ability.nT += nExtend

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {Ability.nD}x {round(Avg[0], 2)}</li>'

    # Extend the Timings array if nExtend > 0
    for i in range(0, nExtend):
        Ability.Timings = np.append(Ability.Timings, [Ability.Timings[-1] + 2])

    return Avg


def PunctureDamAvgCalc(Ability, player, Do):
    """
    Calculates the average hit of an puncture effect of an ability.

    :param player: The Player object
    :param Do: TList object
    :return: Average puncture hits
    """

    Avg = []
    if Ability.Puncture and Ability.Name == 'Greater Dazing Shot':
        Max = np.array([7 / 15 * 0.072, 5 / 15 * 0.072, 2 / 15 * 0.072, 1 / 15 * 0.72]) * player.BaseBoost * player.BaseDamage
        Min = np.array([7 / 15 * 0.058, 5 / 15 * 0.058, 2 / 15 * 0.058, 1 / 15 * 0.58]) * player.BaseBoost * player.BaseDamage

        for i in range(0, Ability.nD):
            Avg.append((Max[i] + Min[i]) / 2)

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {Ability.Name} to {round(Avg[i], 2)}</li>'

    return Avg