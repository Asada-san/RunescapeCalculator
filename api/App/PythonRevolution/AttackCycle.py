from App.PythonRevolution import AverageDamageCalculator as AVGCalc, CycleChecker as Cycle
from copy import deepcopy
import numpy as np
import pprint


def useAbility(bar, player, dummy, logger, settings):
    """
    This function determines the next available ability on the revolution bar which can be
    activated. The ability is then checked for its hits.

    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    :return: The Ability activated in the current attack cycle.
    """

    FireAbility = None

    mustStall = player.nStall % 3 != 0

    # CHECK IF THE PLAYER IS ALLOWED TO ATTACK
    if not bar.GCDStatus and not player.ChanTime:

        if not mustStall:
            # Check for available ability
            bar.FireNextAbility(player, logger)

            # if logger.FindCycle and not logger.CycleFound and 1 == 2:  # Used for debugging
            if settings.FindCycle and not mustStall:
                Cycle.CycleCheck(bar, player, dummy, logger, settings)

                if not settings.run:
                    return None

        # Do stuff based on whether an ability was available or not
        if bar.FireStatus:
            player.nStall = 0

            FireAbility = bar.Rotation[bar.FireN]

            # Add the ability to the Rotation
            logger.addRotation(FireAbility.Name)

            # Tell if Stun/Bind damage is going to be used
            if logger.DebugMode:
                if not all([FireAbility.StunBindDam, any([dummy.StunTime, dummy.BindTime])]):
                    logger.write(31, FireAbility.Name)
                else:
                    logger.write(32, FireAbility.Name)

                logger.write(33, round(bar.Adrenaline, 0))  # Adrenaline status

            determineHits(FireAbility, player, dummy, logger)

        else:
            player.nStall += 1

            if logger.DebugMode:
                if mustStall:
                    logger.write(50)
                else:
                    logger.write(38)

            if mustStall:
                bar.FireStatus = False

            logger.check_stall()

    else:
        if logger.DebugMode:
            if player.ChanTime:
                logger.write(39)
            elif bar.GCDStatus:
                logger.write(40)

    return FireAbility


def determineHits(FA, player, dummy, logger):
    """
    Puts all the hits from the current activated ability on the dummy with timers.

    :param FA: Ability object which has currently been fired from the ability bar.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :return: The Ability activated in the current attack cycle.
    """

    # Depending on the type of ability, get its hits and append them to the dummy
    if FA.Puncture:
        dummy.PHits[dummy.nPH: dummy.nPH + FA.nHits] = PunctureCheck(dummy, player, FA, logger)

    elif FA.Standard or FA.Channeled or FA.Bleed:
        if not all([FA.StunBindDam,  any([dummy.StunTime, dummy.BindTime])]):
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nHits] = deepcopy(FA.Hits)
        else:
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nHits] = deepcopy(FA.HitsStunBind)
    else:
        return

    # Determine amount of hits pending for dummy, some abilities are cut short to maximise dps
    dummy.nPH += FA.nHits

    # Set Channeling Time on Player object
    if FA.Channeled:
        if player.Afk:
            player.ChanTime = FA.TrueWaitTime

        else:
            player.ChanTime = FA.EfficientWaitTime

    if player.Boost1:
        player.Boost1 = False

        player.Boost = True
        player.BoostX.append(player.Boost1X[1])
        player.BoostTime.append(FA.Hits[0].Time + 2)
        player.BoostName.append(player.Boost1X[0])

    # Status checks
    if FA.Name in {'Meteor Strike', 'Tsunami', 'Incendiary Shot'}:
        player.CritAdrenalineBuffTime = FA.EffectDuration

    # Determine hits with Greater Chain effect
    if FA.Name == 'Greater Chain':
        player.GreaterChainTime = FA.EffectDuration
        player.GreaterChainTargets = FA.GreaterChainTargets

    elif player.GreaterChainTime:  # Check for Greater Chain effect
        if (FA.Standard or FA.Channeled or FA.Bleed) and FA.Name != 'Sunshine':
            NewHits = np.array([])
            nHits = 0

            # Corruption shot only the first hit is now also transmitted to the other targets
            if FA.Name == 'Corruption Blast':
                NewHits = np.append(NewHits, deepcopy(FA.Hits[0]))
                nHits += 1
            else:
                for i in range(0, FA.nHits):
                    if FA.Hits[i].Target == 1:  # Only take hits meant for the first target
                        NewHits = np.append(NewHits, deepcopy(FA.Hits[i]))
                        nHits += 1

            for target in player.GreaterChainTargets:
                NewHitsOneTarget = deepcopy(NewHits)

                for i in range(0, len(NewHits)):
                    if NewHitsOneTarget[i].Type != 3:  # Halved damage
                        NewHitsOneTarget[i].DamMax /= 2
                        NewHitsOneTarget[i].DamMin /= 2
                        NewHitsOneTarget[i].Damage /= 2
                    else:  # Bleeds do their normal damage
                        NewHitsOneTarget[i].DamMax /= 1
                        NewHitsOneTarget[i].DamMin /= 1
                        NewHitsOneTarget[i].Damage /= 1

                    NewHitsOneTarget[i].Target = target
                    NewHitsOneTarget[i].Name = 'Greater Chain'

                dummy.PHits[dummy.nPH: dummy.nPH + nHits] = NewHitsOneTarget
                dummy.nPH += nHits

            # Reset properties related the Greater Chain
            player.resetGreaterChain()

    return


def PunctureCheck(dummy, player, FA, logger):
    """
    - Removes puncture hits already on the dummy stack
    - Depending on ability:
        Salt the Wound: Determine ability damage depending on puncture stack
        Greater Dazing Shot: Increase puncture stack and determin puncture damage

    :param player: The Player object.
    :param dummy: The Dummy object.
    :param FA: The Ability activated in the current attack cycle.
    :param logger: The DoList object.
    :return: NewHit(s) --> The hits with newly calculated min, max and damage to be
                applied to the dummy
    """

    # Delete puncture effect from pending hits

    # Check every ability for puncture type, if so move the hit to idx dummy.nPH - 1 and move i + 1: dummy.nPH 1 slot to the left
    for i in range(dummy.nPH - 1, -1, -1):
        if dummy.PHits[i].Type == 4:
            dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
            dummy.nPH -= 1

    # Salt the Wound ability effect
    if FA.Name == 'Salt the Wound':
        NewHit = deepcopy(FA.Hits)  # Copy the hit from the ability to fire

        # Calculate its new average
        NewHit[0].DamMax += .18 * dummy.nPuncture  # PunctureStack
        NewHit[0].DamMin += .036 * dummy.nPuncture  # PunctureStack

        NewHit[0].Damage = AVGCalc.StandardChannelDamAvgCalc(NewHit[0], player, logger)[0]

        # dummy.PHits[dummy.nPH] = Hit  # Put the hit with the new average in the pending hits
        dummy.nPuncture = 0  # Reset stack
        dummy.PunctureDuration = 0
        dummy.Puncture = False

        if logger.DebugMode:
            logger.write(21)

        return NewHit

    else:  # Else the Greater Dazing Shot ability has been used, change stack value accordingly
        dummy.PunctureTime = FA.EffectDuration

        # Set puncture stack
        if dummy.nPuncture < 10:  # Stacks are capped at 10
            dummy.nPuncture += 1

        if logger.DebugMode:
            logger.write(34, dummy.nPuncture)

        NewHits = deepcopy(FA.Hits)
        for i in range(0, len(NewHits)-1):
            NewHits[i+1].DamMax *= dummy.nPuncture
            NewHits[i+1].DamMin *= dummy.nPuncture
            NewHits[i+1].Damage *= dummy.nPuncture

        return NewHits


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
            else:
                # Subtract tick time from every PH
                dummy.PHits[i].Time -= 1

            if dummy.PHits[i].Type == 3:
                isBleeding = True

        if doAttack:
            if player.Ring == 'ChampionsRing' and isBleeding and CritChanceHit:
                player.AbilCritBuff += 0.03  # Champion's ring effect

            doDamage(HitList, bar, dummy, player, logger, settings)  # Inflict damage if the time equals 0


def doDamage(CurrentHits, bar, dummy, player, logger, settings):
    """
    Inflicts all the damage of the hits in the CurrentHits list onto the dummy whilst
    checking for certain effects.

    :param CurrentHits: Hits that need to inflict damage onto the dummy in the current tick
    :param bar: The Bar object.
    :param player: The Player object.
    :param dummy: The Dummy object.
    :param logger: The Logger object.
    :param settings: The Settings object.
    """

    # Check if dummy takes a hit
    for PHit in CurrentHits:
        # Check for Deathspore arrows effect
        if all([player.Ammo == 'Deathspore arrows', PHit.Style == 'Ranged', PHit.Equipment in {'2h', 'any'}, PHit.Type in {1, 2}]):
            player.AbilCritBuff += 0.03

        # Determine average hit damage
        if PHit.Type in {1, 2} and any([player.AbilCritBuff > player.InitCritBuff, player.Boost]):
            PHit.Damage = AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger)

            if player.Boost and logger.DebugMode:
                logger.write(27, [PHit.Name, player.getBoost()])

            # Reset Critical Hit Buff
            player.AbilCritBuff = 0

        elif PHit.Type in {3, 4} and any([player.BaseBoost > 1 and player.Boost, player.GlovesOfPassageTime]):
            PHit.Damage = AVGCalc.BleedDamAvgCalc(PHit, player, logger)
            print(PHit.Damage)

        # Determine bleed damage multiplier
        if PHit.Type == 3 and dummy.Movement and not any([dummy.StunTime, dummy.BindTime]):
            PHit.Damage *= PHit.BleedOnMove

        # Add the damage to the total damage and damage per dummy
        dummy.Damage += PHit.Damage
        dummy.DamagePerDummy[PHit.Target - 1] += PHit.Damage

        # Count the damage for the correct ability whether there is a boost active or not
        if player.Boost and PHit.Type in {1, 2}:
            standardDamage = PHit.Damage / player.getBoost()

            logger.AbilInfo[PHit.Name]['damage'] += standardDamage

            for i, name in enumerate(player.BoostName):
                if name == 'Needle Strike':
                    logger.AbilInfo[name]['damage'] += PHit.Damage - (PHit.Damage / (player.BoostX[i] + 1))
                else:
                    logger.AbilInfo[name]['damage'] += standardDamage * player.BoostX[i]
        else:
            logger.AbilInfo[PHit.Name]['damage'] += PHit.Damage

        # Write to the log
        if logger.DebugMode:
            if dummy.nTarget == 1:
                logger.write(28, [PHit.Name, PHit.Type, round(PHit.Damage, 3)])
            else:
                logger.write(29, [PHit.Name, PHit.Type, int(PHit.Target), round(PHit.Damage, 3)])

        # Increase Aftershock damage if using the perk
        if player.PerkAftershock and PHit.Type not in {4, 10}:
            player.ArDamage += PHit.Damage

        # Increase the stored damage for the Jas Buff if it is active
        if player.JasTime:
            player.JasDamage += PHit.Damage

            if logger.DebugMode:
                logger.write(57, player.JasDamage)

        # Critical hit check: Channeller's Ring
        if all([player.Ring == 'ChannelersRing', PHit.Style == 'Magic', player.ChanTime, PHit.Type == 2, PHit.Name != 'Detonate']):
            player.AbilCritBuff += (PHit.Index + 1) * 0.04

        # Critical hit check: (Greater) Concentrated Blast and Fury
        if PHit.Name in {'Concentrated Blast', 'Greater Concentrated Blast', 'Fury'}:
            player.AbilCritBuff += (PHit.Index + 1) * 0.05

        # Critical hit check: Greater Fury, get the AbilCritBuff for the next Hit via the avg damage calculator
        if PHit.Name == 'Greater Fury':
            AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger, 'Greater Fury')

        # Critical hit check: Increased Adrenaline when under the effect of Tsunami/Meteor Strike/Incendiary Shot
        if all([player.CritAdrenalineBuffTime, PHit.Type in {1, 2}]):

            AVGCalc.StandardChannelDamAvgCalc(PHit, player, logger, 'Adrenaline Buff')
            if player.BasicAdrenalineGain > 1:
                bar.Adrenaline += 1

                if logger.DebugMode:
                    logger.write(30, [bar.Adrenaline])

                player.BasicAdrenalineGain -= 1

        # Append to list of hits that did do damage in the current tick for effect checks
        dummy.DamageNames.append(PHit.Name)

        # Check if it is time to activate a pocket slot item
        if PHit.Type in {1, 2} and player.Pocket != 0 and PHit.Target == 1:
            pocketAbil = player.SpecialAbils[player.Pocket]
            print(pocketAbil.cdTime)
            if not pocketAbil.cdTime:

                player.PocketHitCounter += 1

                if player.PocketHitCounter == pocketAbil.HitsToActivate:
                    if pocketAbil.Name not in {'Scripture of Jas', 'Scripture of Ful'}:
                        dummy.PHits[dummy.nPH: dummy.nPH + pocketAbil.nHits] = deepcopy(pocketAbil.Hits)
                        dummy.nPH += pocketAbil.nHits
                    elif pocketAbil.Name == 'Scripture of Jas':
                        player.JasTime = pocketAbil.EffectDuration

                        if logger.DebugMode:
                            logger.write(56)
                    elif pocketAbil.Name == 'Scripture of Ful':
                        player.Boost = True
                        player.BoostX.append(pocketAbil.BoostX)
                        player.BoostTime.append(pocketAbil.EffectDuration)
                        player.BoostName.append(pocketAbil.Name)

                        if logger.DebugMode:
                            logger.write(58)

                    player.PocketHitCounter = 0

                    logger.addRotation(pocketAbil.Name, True)

                    # Put it on cooldown
                    pocketAbil.putOnCooldown()

    return None
