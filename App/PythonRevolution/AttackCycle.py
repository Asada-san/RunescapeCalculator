from App.PythonRevolution import AverageDamageCalculator as AVGCalc, CycleChecker as Cycle
from copy import deepcopy
import pprint


def Attack_main(bar, player, dummy, logger, settings):
    """
    The main function of the attack cycle. Checks if an ability is available and if so,
    the dummy is attacked.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    :return: The Ability activated in the current attack cycle.
    """

    FireAbility = None

    # CHECK IF THE PLAYER IS ALLOWED TO ATTACK
    if not bar.GCDStatus and not player.ChanAbil:

        # if logger.FindCycle and not logger.CycleFound and 1 == 2:  # Used for debugging
        if settings.FindCycle and not logger.CycleFound:
            Cycle.CycleCheck(bar, player, dummy, logger)

        # Check for available ability
        bar.FireNextAbility(player, logger)

        # Do stuff based on whether an ability was available or not
        if bar.FireStatus:

            FireAbility = bar.Rotation[bar.FireN]

            # Count activations
            if logger.CycleFound or not settings.FindCycle:
                logger.AbilInfo[FireAbility.Name]['activations'] += 1

            # Tell if Stun/Bind damage is going to be used
            if logger.DebugMode:
                if not all([FireAbility.StunBindDam, any([dummy.Stun, dummy.Bind])]):
                    logger.write(31, FireAbility.Name)
                else:
                    logger.write(32, FireAbility.Name)

                logger.write(33, round(bar.Adrenaline, 0))  # Adrenaline status

            # Add to cycle rotation
            if logger.CycleFound:
                logger.Rotation.extend([FireAbility.Name])

                if not logger.nFA[bar.FireN]:
                    logger.nFA[bar.FireN] = True

            AttackDummy(FireAbility, bar, player, dummy, logger, settings)

        else:
            if logger.CycleFound:
                if len(logger.Rotation) != 0 and 'STALL' in logger.Rotation[-1]:
                    logger.nStall += 1
                    logger.Rotation[-1] = f'<span style="color: {logger.TextColor["cycle"]}">STALL {logger.nStall}x</span>'
                else:
                    logger.nStall = 1
                    logger.Rotation.extend([f'<span style="color: {logger.TextColor["cycle"]}">STALL {logger.nStall}x</span>'])

            if logger.DebugMode:
                logger.write(38)

    elif player.ChanAbil:
        if logger.DebugMode:
            logger.write(39)

    elif bar.GCDStatus:
        if logger.DebugMode:
            logger.write(40)

    return FireAbility


def AttackDummy(FA, bar, player, dummy, logger, settings):
    """
    Puts all the hits from the current activated ability on the dummy with timers.

    :param FA: Ability object which has currently been fired from the ability bar.
    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    :return: The Ability activated in the current attack cycle.
    """

    # Depending on the type of ability, get its hits and append them to the dummy
    if FA.Standard or FA.Channeled:
        if not all([FA.StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.Hits)
        else:
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.HitsStunBind)

        if any([FA.Bleed, FA.Puncture]):
            EffectCheck(dummy, player, FA, logger)

    elif FA.Bleed:
        EffectCheck(dummy, player, FA, logger)

    else:  # The ability doesn't do any damage: end this function
        return

    # Determine amount of hits pending for dummy, some abilities are cut short to maximise dps
    if not player.Afk and FA.Name == 'Concentrated Blast':
        dummy.nPH += FA.nT - 1
    else:
        dummy.nPH += FA.nT

    # Check for AoE shenanigans
    if any([FA.Name == 'Greater Ricochet', all([dummy.nTarget > 1 and FA.AoE])]):
        AoECheck(dummy, player, FA)

    if FA.Channeled:
        player.ChanAbil = True

        if player.Afk:
            player.ChanTime = FA.TrueWaitTime

        else:
            player.ChanTime = FA.EfficientWaitTime

    # Attack the dummy if a timer equals 0
    PHitCheck(bar, dummy, player, logger, settings)

    return


def EffectCheck(dummy, player, FA, logger):
    """
    Puts the hits from the current activated ability on the dummy with timers (only
    bleeds and punctures).

    :param player: The Player object.
    :param dummy: The Dummy object.
    :param FA: The Ability activated in the current attack cycle.
    :param logger: The DoList object.
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
            Hit = deepcopy(FA.Hits[0])  # Copy the hit from the ability to fire

            # Calculate its new average
            Hit.DamMax[0] += .18 * dummy.nPuncture  # PunctureStack
            Hit.DamMin[0] += .036 * dummy.nPuncture  # PunctureStack

            Hit.Damage = AVGCalc.StandardChannelDamAvgCalc(Hit, player, logger)[0]

            dummy.PHits[dummy.nPH] = Hit  # Put the hit with the new average in the pending hits
            dummy.nPuncture = 0  # Reset stack
            dummy.PunctureDuration = 0
            dummy.Puncture = False

            if logger.DebugMode:
                logger.write(21)

            return
        else:  # Else the Greater Dazing Shot ability has been used, change stack value accordingly
            dummy.PunctureDuration = 15
            dummy.Puncture = True

            # Set puncture stack
            if dummy.nPuncture < 10:  # Stacks are capped at 10
                dummy.nPuncture += 1

            if logger.DebugMode:
                logger.write(34, dummy.nPuncture)

        dummy.PHits[dummy.nPH + FA.nS: dummy.nPH + FA.nT] = deepcopy(FA.DoTHits)


def AoECheck(dummy, player, FA):
    """
    Duplicates hits if the ability does AoE damage and there are more than 1 target.

    :param player: The Player object.
    :param dummy: The Dummy object.
    :param FA: The Ability activated in the current attack cycle.
    """

    if dummy.nTarget > 9 and FA.Name not in {'Corruption Blast', 'Corruption Shot'}:
        nDT = 9
    else:
        nDT = dummy.nTarget

    if FA.Name == 'Quake':  # DamMax = 1.88, DamMin = 0.376, DamAvg = 1.128 for side targets
        N = FA.nT

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i: dummy.nPH + i] = deepcopy(FA.HitsSideTarget)
            dummy.PHits[dummy.nPH + i].Target = i + 2

    elif FA.Name == 'Greater Flurry':  # DamMax = 0.94, DamMin = 0.2, DamAvg = 0.57 for ALL! targets
        N = FA.nT

        for i in range(0, nDT):
            dummy.PHits[dummy.nPH + (i - 1) * N: dummy.nPH + i * N] = deepcopy(FA.HitsSideTarget)

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

    # Apply Hits of greater Ricochet for which no targets are available back to target 1
    # but halved. Do it here because dummy.nPH is needed and is only set just above.
    if FA.Name == 'Greater Ricochet' and dummy.nTarget < 3 + player.Cr:
        NewHit = deepcopy(dummy.PHits[dummy.nPH - 1])
        NewHit.DamMax /= 2
        NewHit.DamMin /= 2
        NewHit.Damage /= 2
        NewHit.Time += 1  # Hit on target delayed with 1 tick
        NewHit.Target = 1

        for i in range(0, int(3 + player.Cr - dummy.nTarget)):
            dummy.PHits[dummy.nPH] = deepcopy(NewHit)  # Apply the hit on main target
            dummy.nPH += 1


def PHitCheck(bar, dummy, player, logger, settings):
    """
    Check if there are any pending hits.
        True    --> Create HitList with Hit objects that will damage the dummy
                    Remove the Hit from Pending Hits list
                    Perform check for Champion's ring
                    Attack the dummy
        False   --> Do nothing

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The DoList object.
    :param settings: The Setting object.
    """

    if dummy.nPH > 0:  # If there are any Pending Hits
        doAttack = False
        isBleeding = False
        CritChanceHit = False
        HitList = []

        for i in range(dummy.nPH - 1, -1, -1):
            if dummy.PHits[i].Time == 0:
                doAttack = True

                HitList.append(dummy.PHits[i])

                # Shift the current hit to the right and others after that 1 place to the left
                # AKA shifting the Hit into meaninglessness
                dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
                dummy.nPH -= 1

                if dummy.PHits[i].Type not in {3, 4}:
                    CritChanceHit = True

            if dummy.PHits[i].Type == 3:
                isBleeding = True

        if doAttack:
            if player.Ring == 'ChampionsRing' and isBleeding and CritChanceHit:
                player.AbilCritBuff += 0.03  # Champion's ring effect

            DummyDamage(HitList, bar, dummy, player, logger, settings)  # Inflict damage if the time equals 0


def DummyDamage(CurrentHits, bar, dummy, player, logger, settings):
    """
    Checks if a timer of a hit reached 0, if so, damages the target and checks effects.

    :param CurrentHits: Hits that need to inflict damage onto the dummy in the current tick
    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    """

    # Check if dummy takes a hit
    for PHit in CurrentHits:
        standardDamage = PHit.Damage

        if player.Ring == 'ChannelersRing' and bar.Style == 'Magic' and player.ChanAbil and PHit.Type == 2 and not PHit.Name == 'Detonate':
            player.ChannelCritStack += 1
            player.AbilCritBuff += player.ChannelCritStack * 0.04

        # Determine bleed damage multiplier
        if PHit.Type == 3 and dummy.Movement and not any([dummy.Stun, dummy.Bind]):
            PHit.Damage *= PHit.BleedOnMove

        # Determine average hit damage
        if PHit.Type in {1, 2, 5, 6, 7, 8} and any([player.AbilCritBuff > player.InitCritBuff, player.Boost, player.Boost1]):
            PHit.Damage = AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger)[0]

            if any([player.Boost, player.Boost1]):
                if logger.DebugMode:
                    logger.write(27, [PHit.Name, player.BoostX * player.Boost1X])

            # The single hit damage boost works on the first 2 hits on rapid fire fore some reason
            if any([PHit.Name not in ['Rapid Fire', 'Snap Shot'] and player.Boost1, player.Boost1 and int(PHit.Index) == 1]):
                player.Boost1 = False
                player.Boost1X = 1

            # Reset Critical Hit Buff
            player.AbilCritBuff = 0

        elif PHit.Type in {3, 4} and player.BaseBoost > 1 and player.Boost:
            if PHit.Index == 0 and player.Boost1:
                player.Boost1 = False
                player.Boost1X = 1

            PHit.Damage = AVGCalc.BleedDamAvgCalc(PHit, player, logger)[0]

        # Add the damage to the total damage
        if PHit.Type != 4:
            dummy.Damage += PHit.Damage
        else:
            dummy.PunctureDamage += PHit.Damage

        # Check for Greater Chain effect
        if player.GreaterChain:
            AbilNames = [PHit.Name for PHit in CurrentHits]

            if 'Greater Chain' not in AbilNames:

                if player.ChanAbil and PHit.Type == 2:
                    CurrentHits.extend(getGreaterChainHits(PHit, player))
                elif PHit.Name != 'Sunshine':
                    CurrentHits.extend(getGreaterChainHits(PHit, player))
                    player.resetGreaterChain()

        # Set some cycle data
        if logger.CycleFound or not settings.FindCycle:
            logger.AbilInfo[PHit.Name]['damage'] += PHit.Damage
            logger.AbilInfo['Boosted']['damage'] += PHit.Damage - standardDamage

            if PHit.Type != 4:
                logger.CycleDamage += PHit.Damage
            else:
                logger.CyclePunctureDamage += PHit.Damage

        if logger.DebugMode:
            if dummy.nTarget == 1:
                logger.write(28, [PHit.Name, PHit.Type, round(PHit.Damage, 3)])
            else:
                logger.write(29, [PHit.Name, PHit.Type, int(PHit.Target), round(PHit.Damage, 3)])

        # Critical hit chance checks
        if PHit.Name in {'Concentrated Blast', 'Fury'}:
            if player.CritStack == 3:  # If the stack reached 3, reset
                player.CritStack = 0
            player.CritStack += 1  # Increase stack
            player.AbilCritBuff += 0.05 * player.CritStack

        elif PHit.Name == 'Greater Fury' or all([player.CritAdrenalineBuffTime > 0, PHit.Type in {1, 2}]):

            if player.CritAdrenalineBuffTime > 0:
                player.CritAdrenalineBuff = True  # We need to perform a check
                AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger)
                bar.Adrenaline += round(player.BasicAdrenalineGain / 1, 0)

                if logger.DebugMode:
                    logger.write(30, [round(player.BasicAdrenalineGain / 1, 0), round(bar.Adrenaline, 0)])

                player.BasicAdrenalineGain -= round(player.BasicAdrenalineGain / 1, 0)

            if PHit.Name == 'Greater Fury':
                player.GreaterFuryCritCheck = True  # We need to perform a check
                AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger)

        # Append to list of hits that did do damage in the current tick for effect checks
        dummy.DamageNames.append(PHit.Name)

    return None


def getGreaterChainHits(PHit, player):
    """
    Copies the Hit object and puts it in a list GreaterChainTargets times.

    :param PHit: The Hit object.
    :param player: The Player object.
    :return PHitList: List containing copied Hits.
    """

    PHitList = []

    NewHit = deepcopy(PHit)
    NewHit.Damage /= 2

    # NewHit.Type = 8

    for target in player.GreaterChainTargets:
        NewHit.Target = target
        PHitList.append(NewHit)

    return PHitList
