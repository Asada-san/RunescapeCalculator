from App.PythonRevolution import AverageDamageCalculator as AVGCalc, CycleChecker as Cycle
from copy import deepcopy
import pprint


def Attack_main(bar, player, dummy, Do, loop):
    """
    The main function of the attack cycle. Checks if an ability is available and if so,
    the dummy is attacked.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param Do: The DoList object.
    :param loop: The Loop object.
    :return: The Ability activated in the current attack cycle.
    """

    FireAbility = None

    # CHECK IF THE PLAYER IS ALLOWED TO ATTACK
    if not bar.GCDStatus and not player.ChanAbil:

        # if loop.FindCycle and not loop.CycleFound and 1 == 2:  # Used for debugging
        if loop.FindCycle and not loop.CycleFound:
            Cycle.CycleCheck(bar, player, dummy, Do, loop)

        # Check for available ability
        for i in range(0, bar.N):
            if not bar.Rotation[i].cdStatus:
                bar.AdrenalineStatus(bar.Rotation[i], player)

                if bar.FireStatus:
                    bar.FireN = i  # Index of ability is equal to for loop i

                    if loop.CycleFound:
                        loop.Rotation.extend([bar.Rotation[i].Name])

                        if not loop.nFA[bar.FireN]:
                            loop.nFA[bar.FireN] = True

                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.nor_color};">Attack status: {bar.Rotation[i].Name} ready</li>\n'

                    break  # Break because firing more than 1 ability wouldn't make sense

                else:
                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.init_color};">Not enough Adrenaline for {bar.Rotation[i].Name}</li>\n'

        # Do stuff based on whether an ability was available or not
        if bar.FireStatus:
            FireAbility = AttackDummy(bar, player, dummy, Do, loop)

        else:
            if loop.CycleFound:
                if len(loop.Rotation) != 0 and 'STALL' in loop.Rotation[-1]:
                    loop.nStall += 1
                    loop.Rotation[-1] = f'<span style="color: {Do.cycle_color}">STALL {loop.nStall}x</span>'
                else:
                    loop.nStall = 1
                    loop.Rotation.extend([f'<span style="color: {Do.cycle_color}">STALL {loop.nStall}x</span>'])

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.imp_color};">No ability available, skip attack</li>\n'

    elif player.ChanAbil:
        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.imp_color};">Player is using a channeled ability</li>\n'

    elif bar.GCDStatus:
        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.imp_color};">GLOBAL COOLDOWN</li>\n'

    return FireAbility


def AttackDummy(bar, player, dummy, Do, loop):
    """
    Puts all the hits from the current activated ability on the dummy with timers.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param Do: The DoList object.
    :param loop: The Loop object.
    :return: The Ability activated in the current attack cycle.
    """

    FA = bar.Rotation[bar.FireN]  # FireAbility: ability to be fired in the current tick

    if loop.CycleFound or not loop.FindCycle:
        player.AbilInfo[FA.Name]['activations'] += 1

    if Do.HTMLwrite:
        if not all([FA.StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            Do.Text += f'<li style="color: {Do.att_color};">{FA.Name} activated (normal)\n'
        else:
            Do.Text += f'<li style="color: {Do.imp_color};">{FA.Name} activated (stun&bind)\n'

        Do.Text += f'<li style="color: {Do.att_color};">Adrenaline: {round(bar.Adrenaline, 0)}</li>\n'

    # Depending on the type of ability, get its hits
    if FA.Standard or FA.Channeled:
        if not all([FA.StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.Hits)
        else:
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.HitsStunBind)

        if any([FA.Bleed, FA.Puncture]):
            EffectCheck(bar, dummy, player, FA, Do)

    elif FA.Bleed:
        EffectCheck(bar, dummy, player, FA, Do)

    else:  # The ability doesn't do any damage: end this function
        return FA

    # Determine amount of hits pending for dummy, some abilities are cut short to maximise dps
    if not player.Afk and FA.Name == 'Concentrated Blast':
        dummy.nPH += FA.nT - 1
    else:
        dummy.nPH += FA.nT

    # Check for AoE shenanigans
    if any([FA.Name == 'Greater Ricochet', all([dummy.nTarget > 1 and FA.AoE])]):
        AoECheck(bar, dummy, player, FA, Do)

    # Check for Greater Chain effect
    if player.GreaterChain and FA.Name != 'Greater Chain':
        if not FA.Bleed:
            Avg = AVGCalc.StandardChannelDamAvgCalc(FA, player, Do, 'Normal', 0)
            NewHit = deepcopy(FA.Hits[0])
            NewHit.Damage = Avg[0] / 2
        else:
            NewHit = deepcopy(FA.DoTHits[0])
            NewHit.Damage = FA.DoTHits[0].Damage / 2

        NewHit.Name = 'Greater Chain'
        NewHit.Type = 8

        for target in player.GreaterChainTargets:
            NewHit.Target = target
            dummy.PHits[dummy.nPH] = deepcopy(NewHit)
            dummy.nPH += 1

        if not FA.Channeled:
            player.GreaterChain = False
            player.GreaterChainTargets = []
            player.GreaterChainDuration = 0
            player.GreaterChainHitN = 0

    # Attack the dummy if a timer equals 0
    DummyDamage(bar, dummy, player, Do, loop)

    return FA


def EffectCheck(bar, dummy, player, FA, Do):
    """
    Puts the hits from the current activated ability on the dummy with timers (only
    bleeds and punctures).

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param FA: The Ability activated in the current attack cycle.
    :param Do: The DoList object.
    """

    # Determine whether ability has bleed or puncture effect
    if FA.Bleed:
        dummy.PHits[dummy.nPH + FA.nS: dummy.nPH + FA.nT] = deepcopy(FA.DoTHits)

    elif FA.Puncture:
        # Delete puncture effect from pending hits
        # Standard attack already has been added, thus add it to nDoT during the removal
        dummy.nPH += FA.nS

        # Check every ability for puncture type, if so move the hit to idx dummy.nPH - 1 and move i + 1: dummy.nPH 1 slot to the left
        for i in range(dummy.nPH - 1, -1, -1):
            if dummy.PHits[i].Type == 4:
                dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
                dummy.nPH -= 1

        # Decrease nDoT by 1 again for consistency with other effects
        dummy.nPH -= FA.nS

        # Salt the Wound ability effect
        if FA.Name == 'Salt the Wound':
            IDX = bar.AbilNames.index(FA.Name)  # Spot of the ability on the bar
            Hit = deepcopy(FA.Hits[0])  # Copy the hit from the ability to fire

            # Calculate its new average
            Hit.Damage = AVGCalc.StandardChannelDamAvgCalc(bar.Rotation[IDX], player, Do, 'Salt the Wound', FA.Hits[0].Index, dummy.nPuncture)[0]
            dummy.PHits[dummy.nPH] = Hit  # Put the hit with the new average in the pending hits
            dummy.LastStack = dummy.nPuncture
            dummy.nPuncture = 0  # Reset stack
            dummy.PunctureDuration = 0
            dummy.Puncture = False

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.stat_color};">Dummy puncture stack reset to 0</li>\n'

            return
        else:  # Else the Greater Dazing Shot ability has been used, change stack value accordingly
            dummy.PunctureDuration = 15
            dummy.Puncture = True

            # Set puncture stack
            if dummy.nPuncture < 10:  # Stacks are capped at 10
                dummy.nPuncture += 1

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.stat_color};">Dummy puncture stack: {dummy.nPuncture}</li>\n'

        dummy.PHits[dummy.nPH + FA.nS: dummy.nPH + FA.nT] = deepcopy(FA.DoTHits)


def AoECheck(bar, dummy, player, FA, Do):
    """
    Duplicates hits if the ability does AoE damage and there are more than 1 target.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param FA: The Ability activated in the current attack cycle.
    :param Do: The DoList object.
    """

    if dummy.nTarget > 9 and FA.Name not in {'Corruption Blast', 'Corruption Shot'}:
        nDT = 9
    else:
        nDT = dummy.nTarget

    if FA.Name == 'Quake':  # DamMax = 1.88, DamMin = 0.376, DamAvg = 1.128 for side targets
        N = FA.nT

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i: dummy.nPH + i] = deepcopy(FA.SideTargetAvg)
            dummy.PHits[dummy.nPH + i].Target = i + 2

    elif FA.Name == 'Greater Flurry':  # DamMax = 0.94, DamMin = 0.2, DamAvg = 0.57 for ALL! targets
        N = FA.nT

        for i in range(0, nDT):
            dummy.PHits[dummy.nPH + (i - 1) * N: dummy.nPH + i * N] = deepcopy(FA.SideTargetAvg)

            if i > 0:
                for j in range(0, N):
                    dummy.PHits[dummy.nPH + (i - 1) * N + j].Target = i + 1

    elif FA.Name == 'Hurricane':  # First hit on main target equals the hit for all other targets
        N = FA.nT - 1

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i] = deepcopy(dummy.PHits[dummy.nPH - 2])
            dummy.PHits[dummy.nPH + i].Target = i + 2

    elif FA.Name in {'Corruption Blast', 'Corruption Shot'}:  # First hit main target only, than spreading to all other targets
        N = FA.nT - 1

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2

    elif FA.Name in {'Chain', 'Greater Chain', 'Ricochet', 'Greater Ricochet'}:  # Ricochet and Chain only hit up to 3 targets (except when perk)
        N = FA.nT

        if nDT > 3 + player.Cr:  # If number of damageable targets is larger than 3, set nDT to 3.
            nDT = int(3 + player.Cr)

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2

        if FA.Name == 'Greater Ricochet' and dummy.nTarget < 3 + player.Cr:
            player.GreaterRicochet = True
            player.nGreaterRicochet = int(3 + player.Cr - dummy.nTarget)

        if FA.Name == 'Greater Chain':
            player.GreaterChain = True
            player.GreaterChainDuration = 10
            player.GreaterChainTargets = list(range(2, nDT + 1))

    else:
        N = FA.nT

        if FA.Name == 'Dragon Breath' and dummy.nTarget > 4:
            nDT = 4

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2
    
    # Increase dummy.nPH by the amount of hits N every other target nDT - 1 receives
    dummy.nPH += (nDT - 1) * N


def DummyDamage(bar, dummy, player, Do, loop):
    """
    Checks if a timer of a hit reached 0, if so, damages the target and checks effects.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param Do: The DoList object.
    :param loop: The Loop object.
    """

    for i in range(dummy.nPH - 1, -1, -1):
        if dummy.PHits[i].Time == 0:
            if all([player.GreaterChain, player.ChanAbil]):
                IDX = bar.AbilNames.index(dummy.PHits[i].Name)
                player.GreaterChainHitN += 1

                Avg = AVGCalc.StandardChannelDamAvgCalc(bar.Rotation[IDX], player, Do, 'Normal', player.GreaterChainHitN)

                NewHit = deepcopy(dummy.PHits[i])
                NewHit.Damage = Avg[0] / 2

                NewHit.Name = 'Greater Chain'
                NewHit.Type = 8

                for target in player.GreaterChainTargets:
                    NewHit.Target = target
                    dummy.PHits[dummy.nPH] = deepcopy(NewHit)
                    dummy.nPH += 1

    # Check if dummy takes a hit
    for i in range(dummy.nPH - 1, -1, -1):
        if dummy.PHits[i].Time == 0:

            # Determine bleed damage multiplier
            if dummy.PHits[i].Type == 3 and dummy.Movement and not any([dummy.Stun, dummy.Bind]):
                IDX = bar.AbilNames.index(dummy.PHits[i].Name)
                dummy.PHits[i].Damage *= bar.Rotation[IDX].BleedOnMove

            # Determine average hit damage
            if dummy.PHits[i].Type in {1, 2} and any([player.AbilCritBuff > 0, player.Boost, player.Boost1]):
                HitDamage = CalcNewAvg(bar, dummy, player, Do, i)

                if Do.HTMLwrite and any([player.Boost, player.Boost1]):
                    Do.Text += f'<li style="color: {Do.att_color};">{dummy.PHits[i].Name} hit boosted {player.BoostX * player.Boost1X}x</li>'

                # The single hit damage boost works on the first 2 hits on rapid fire fore some reason
                if any([dummy.PHits[i].Name not in ['Rapid Fire', 'Snap Shot'] and player.Boost1, player.Boost1 and int(dummy.PHits[i].Index) == 1]):
                    player.Boost1 = False
                    player.Boost1X = 1

            elif dummy.PHits[i].Type in {3, 4} and player.BaseBoost > 1 and player.Boost:
                if dummy.PHits[i].Index == 0 and player.Boost1:
                    player.Boost1 = False
                    player.Boost1X = 1

                HitDamage = CalcNewAvg(bar, dummy, player, Do, i)

            else:
                HitDamage = dummy.PHits[i].Damage

            # Add the damage to the total damage
            if dummy.PHits[i].Type != 4:
                dummy.Damage += HitDamage
            else:
                dummy.PunctureDamage += HitDamage

            if loop.CycleFound:  # If a cycle has been found
                player.AbilInfo[dummy.PHits[i].Name]['damage'] += HitDamage / ((1 + player.AbilCritBuff) * player.BoostX * player.Boost1X)
                player.AbilInfo['Boosted']['damage'] += HitDamage - (HitDamage / ((1 + player.AbilCritBuff) * player.BoostX * player.Boost1X))

                if dummy.PHits[i].Type != 4:
                    loop.CycleDamage += HitDamage
                else:
                    loop.CyclePunctureDamage += HitDamage

            if Do.HTMLwrite:
                if dummy.nTarget == 1:
                    Do.Text += f'<li style="color: {Do.dam_color};">{dummy.PHits[i].Name} ({Do.TypeDict[dummy.PHits[i].Type]}) damage applied: {round(HitDamage, 3)}</li>\n'
                else:
                    Do.Text += f'<li style="color: {Do.dam_color};">{dummy.PHits[i].Name} ({Do.TypeDict[dummy.PHits[i].Type]}) damage applied on target #{int(dummy.PHits[i].Target)}: {round(HitDamage, 3)}</li>\n'

            # Critical hit chance checks
            if dummy.PHits[i].Name in {'Concentrated Blast', 'Fury'}:
                if player.CritStack == 3:  # If the stack reached 3, reset
                    player.CritStack = 0
                else:  # Increase AbilCritBuff
                    if player.AbilCritBuff < 0.15:  # If the AbilCritBuff is smaller than 15%, increase by 5%
                        player.AbilCritBuff += 0.05
                player.CritStack += 1  # Increase stack

            elif dummy.PHits[i].Name == 'Greater Fury' or all([player.CritAdrenalineBuffTime > 0, dummy.PHits[i].Type in {1, 2}]):
                player.CritStack = 0  # Reset stack

                if player.CritAdrenalineBuffTime > 0:
                    player.CritAdrenalineBuff = True  # We need to perform a check
                    CalcNewAvg(bar, dummy, player, Do, i)
                    bar.Adrenaline += round(player.BasicAdrenalineGain / 1, 0)

                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.att_color};">Adrenaline increased by: {round(player.BasicAdrenalineGain / 1, 0)} to: {round(bar.Adrenaline, 0)}</li>\n'

                    player.BasicAdrenalineGain -= round(player.BasicAdrenalineGain / 1, 0)
                    player.AbilCritBuff = 0  # Reset crit buff

                if dummy.PHits[i].Name == 'Greater Fury':
                    player.AbilCritBuff = 0  # Reset crit buff
                    player.GreaterFuryCritCheck = True  # We need to perform a check
                    CalcNewAvg(bar, dummy, player, Do, i)

            elif dummy.PHits[i].Type in {1, 2}:
                player.CritStack = 0  # Reset stack
                player.AbilCritBuff = 0  # Reset crit buff

            # Delete the Hit
            dummy.DamageNames.append(dummy.PHits[i].Name)
            # Shift the current hit to the right and others after that 1 place to the left
            dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
            dummy.nPH -= 1

    # Determine if dummy takes damage outside attack cycle
    if dummy.nPH == 0:
        dummy.PH = False
    else:
        dummy.PH = True

    return None


def CalcNewAvg(bar, dummy, player, Do, i):

    ##############################################################
    ############# Calculate new avg depending on type ############
    ##############################################################

    if dummy.PHits[i].Type in {7, 8}:
        return dummy.PHits[i].Damage

    IDX = bar.AbilNames.index(dummy.PHits[i].Name)  # Spot of the ability on the bar

    if dummy.PHits[i].Name == 'Salt the Wound':
        Avg = AVGCalc.StandardChannelDamAvgCalc(bar.Rotation[IDX], player, Do, 'Salt the Wound', dummy.PHits[i].Index, dummy.LastStack)
        dummy.LastStack = 0

    elif dummy.PHits[i].Type in {1, 2}:

        # if dummy.PHits[i].Name == 'Greater Ricochet' and dummy.PHits[i].Target == 1:
        #     nRedundantHits = 3 + player.Cr - dummy.nTarget
        #     Avg = bar.Rotation[IDX].StandardChannelDamAvgCalc(player, Do, 'Greater Ricochet', 0, nRedundantHits)

        if not all([bar.Rotation[IDX].StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            Avg = AVGCalc.StandardChannelDamAvgCalc(bar.Rotation[IDX], player, Do, 'Normal', dummy.PHits[i].Index)
        else:
            Avg = AVGCalc.StandardChannelDamAvgCalc(bar.Rotation[IDX], player, Do, 'StunBind', dummy.PHits[i].Index)

    elif dummy.PHits[i].Type in {3, 4}:

        Avg = AVGCalc.BleedDamAvgCalc(bar.Rotation[IDX], player, Do)

    ##############################################################
    ########### Return the new Average if its not None ###########
    ##############################################################

    if Avg is not None:
        return Avg[0]
    else:
        return None
