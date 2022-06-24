from App.PythonRevolution import CycleChecker as Cycle
from copy import deepcopy, copy
import numpy as np
import pprint


def useAbility(player, dummy, logger, settings):
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

    mustStall = logger.nStall % 3 != 0

    # CHECK IF THE PLAYER IS ALLOWED TO ATTACK
    if not player.Bar.GCDTime and not player.ChanTime:

        if not mustStall:
            # Check for available ability
            FireAbility = player.FireNextAbility(logger)

            # Do stuff based on whether an ability was available or not
            if FireAbility is not None:
                FireAbility.putOnCooldown()

                # if logger.FindCycle and not logger.CycleFound and 1 == 2:  # Used for debugging
                if settings.FindCycle and not mustStall:
                    Cycle.CycleCheck(player, dummy, logger, settings)

                    if not settings.run:
                        return None

                logger.nStall = 0

                # Add the ability to the Rotation
                logger.addRotation(FireAbility.Name)

                # Tell if Stun/Bind damage is going to be used
                if logger.DebugMode:
                    if not all([FireAbility.StunBindDam, any([dummy.StunTime, dummy.BindTime])]):
                        logger.Text += f'<li style="color: {logger.TextColor["attack"]};">{FireAbility.Name} activated (normal)'
                    else:
                        logger.Text += f'<li style="color: {logger.TextColor["important"]};">{FireAbility.Name} activated (stun&bind)'

                    logger.Text += f'<li style="color: {logger.TextColor["attack"]};">Adrenaline: {player.Adrenaline}</li>'

                determineHits(FireAbility, player, dummy, logger)

            else:
                logger.nStall += 1

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["important"]};">Skip attack: No ability available</li>'

            return FireAbility

        else:
            logger.nStall += 1

            if logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["important"]};">Skip attack: Extra stall due to jagex clunkyness</li>'

            logger.check_stall()

    else:
        if logger.DebugMode:
            if player.ChanTime:
                logger.Text += f'<li style="color: {logger.TextColor["important"]};">Player is using a channeled ability</li>'
            elif player.Bar.GCDTime:
                logger.Text += f'<li style="color: {logger.TextColor["important"]};">GLOBAL COOLDOWN</li>'

    return None


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
                        NewHitsOneTarget[i].DamageMultiplier /= 2

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
        if dummy.PHits[i].Parent.Puncture and dummy.PHits[i].Index > 0:
            dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
            dummy.nPH -= 1

    # Salt the Wound ability effect
    if FA.Name == 'Salt the Wound':
        NewHit = deepcopy(FA.Hits)  # Copy the hit from the ability to fire

        # Calculate its new average
        if dummy.nPuncture > 0:
            NewHit[0].DamMaxBonus = .18 * dummy.nPuncture  # PunctureStack
            NewHit[0].DamMinBonus = .036 * dummy.nPuncture  # PunctureStack
            NewHit[0]._Damage = None

            # dummy.PHits[dummy.nPH] = Hit  # Put the hit with the new average in the pending hits
            dummy.nPuncture = 0  # Reset stack
            dummy.PunctureDuration = 0
            dummy.Puncture = False

            if logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy puncture stack reset to 0</li>'

        return NewHit

    else:  # Else the Greater Dazing Shot ability has been used, change stack value accordingly
        dummy.PunctureTime = FA.EffectDuration

        # Set puncture stack
        if dummy.nPuncture < 10:  # Stacks are capped at 10
            dummy.nPuncture += 1

        if logger.DebugMode:
            logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy puncture stack: {dummy.nPuncture}</li>'

        # NewHits = deepcopy(FA.Hits)
        # for i in range(0, len(NewHits)-1):
        #     NewHits[i+1].Damage *= dummy.nPuncture

        return deepcopy(FA.Hits)  # NewHits


def PHitCheck(player, dummy, logger, settings):
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
        HitList = []

        for i in range(dummy.nPH - 1, -1, -1):
            if dummy.PHits[i].Time == 0:
                doAttack = True

                HitList.append(dummy.PHits[i])

                # Shift the current hit to the right and others after that 1 place to the left
                # AKA shifting the Hit into meaninglessness
                dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]
                dummy.nPH -= 1

            else:
                # Subtract tick time from every PH
                dummy.PHits[i].Time -= 1

        if doAttack:
            doDamage(HitList, player, dummy, logger, settings)  # Inflict damage if the time equals 0


def doDamage(CurrentHits, player, dummy, logger, settings):
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

        if player.Ring.Name == 'Champion\'s ring' and dummy.isBleeding and PHit.Type in {1, 2}:
            PHit.pForcedCrit += 0.03  # Champion's ring effect
            PHit._Damage = None

        if player.Bar.CritIncreaseNextAbility and PHit.Type in {1, 2}:
            PHit.pForcedCrit += player.Bar.CritIncreaseNextAbility
            player.Bar.CritIncreaseNextAbility = 0
            PHit._Damage = None

        # Determine average hit damage
        if player.Boost1:
            if PHit.Type in {1, 2}:
                player.resetBoost1()
            else:
                player.Boost1 = False

        if PHit.Type in {1, 2} and any([player.Boost]):
            PHit._Damage = None

            if player.Boost and logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["attack"]};">{PHit.Parent.Name} hit boosted {player.getBoost()}x</li>'

        elif PHit.Type == 3 and ((player.Boost and player.Aura.Name in {'Berserker aura', 'Reckless aura', 'Maniacal aura'}) or player.GlovesOfPassageTime):
            PHit._Damage = None

        # Determine bleed damage multiplier
        if PHit.Type == 3 and dummy.Movement and not any([dummy.StunTime, dummy.BindTime]):
            PHit.DamageMultiplier *= PHit.Parent.BleedOnMove

        # Determine puncture multiplier
        if PHit.Type == 4:
            PHit.DamageMultiplier *= dummy.nPuncture

        damage = PHit.Damage * PHit.DamageMultiplier

        # Add the damage to the total damage and damage per dummy
        dummy.Damage += damage
        dummy.DamagePerDummy[PHit.Target - 1] += damage

        # Count the damage for the correct ability whether there is a boost active or not
        if player.Boost and PHit.Type in {1, 2}:
            standardDamage = damage / player.getBoost()

            logger.AbilInfo[PHit.Parent.Name]['damage'] += standardDamage

            for i, ability in enumerate(player.BoostName):
                if PHit.Parent.Boost1:
                    logger.AbilInfo[ability.Name]['damage'] += damage - (damage / (player.BoostX[i] + 1))
                else:
                    logger.AbilInfo[ability.Name]['damage'] += standardDamage * player.BoostX[i]
        else:
            logger.AbilInfo[PHit.Parent.Name]['damage'] += damage

        # Write to the log
        if logger.DebugMode:
            logger.Text += f'<li style="color: {logger.TextColor["damage"]};">{PHit.Parent.Name} damage applied on target #{int(PHit.Target)}: {round(damage, 3)}</li>'

        # Crit increase due to chance of ability critting meaning next abil crit chance is 100% +
        # Crit increase due to chance of ability not critting meaning next abil crit chance is 10%
        #
        # Total increase - forced crit OR NOT forced crit AND natural crit * 0.1 OR NOT forced crit AND NOT natural crit * 1
        if PHit.Parent.Name == 'Greater Fury':
            player.Bar.CritIncreaseNextAbility = (PHit.pForcedCrit + (1 - PHit.pForcedCrit) * PHit.pNatCrit) + \
                                                 (1 - PHit.pForcedCrit) * (1 - PHit.pNatCrit) * 0.1

        if PHit.Parent.Name in {'Fury', 'Concentrated Blast', 'Greater Concentrated Blast'}:
            player.Bar.CritIncreaseNextAbility += (PHit.Index + 1) * 0.05

        # Increase Aftershock damage if using the perk
        if player.Aftershock and PHit.Type not in {4, 10}:
            player.AsDamage += PHit.Damage

        # Increase the stored damage for the Jas Buff if it is active
        if player.JasTime:
            player.JasDamage += PHit.Damage

            if logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["charge"]};">Jas buff damage increased to: {player.JasDamage}</li>'

        # Critical hit check: Increased Adrenaline when under the effect of Tsunami/Meteor Strike/Incendiary Shot
        if all([player.CritAdrenalineBuffTime, PHit.Type in {1, 2}]):

            player.BasicAdrenalineGain += (PHit.pForcedCrit + (1 - PHit.pForcedCrit) * PHit.pNatCrit) * 2

            if player.BasicAdrenalineGain > 1 and player.Adrenaline < player.MaxAdrenaline:
                player.Adrenaline += 1

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["attack"]};">Adrenaline increased by 1 to: {player.Adrenaline}</li>'

                player.BasicAdrenalineGain -= 1

        # Append to list of hits that did do damage in the current tick for effect checks
        dummy.DamageNames.append(PHit.Parent.Name)

        if player.Aura.Name == 'Inspiration aura' and not (PHit.Type == 3 and PHit.Parent.Name == 'Greater Dazing Shot'):
            player.Adrenaline += player.Aura.Multiplier * 100

        # Check if it is time to activate a pocket slot item
        if PHit.Type in {1, 2} and player.Pocket.Name != 'Pocket' and PHit.Target == 1:
            pocketAbil = player.Special[player.Pocket.Name]

            if not pocketAbil.cdTime:

                player.PocketHitCounter += 1

                if player.PocketHitCounter == pocketAbil.HitsToActivate:
                    if pocketAbil.Name not in {'Scripture of Jas', 'Scripture of Ful'}:
                        dummy.PHits[dummy.nPH: dummy.nPH + pocketAbil.nHits] = deepcopy(pocketAbil.Hits)
                        dummy.nPH += pocketAbil.nHits
                    elif pocketAbil.Name == 'Scripture of Jas':
                        player.JasTime = pocketAbil.EffectDuration

                        if logger.DebugMode:
                            logger.Text += f'<li style="color: {logger.TextColor["attack"]};">Jas buff activated</li>'
                    elif pocketAbil.Name == 'Scripture of Ful':
                        player.addBoost(pocketAbil)

                        if logger.DebugMode:
                            logger.Text += f'<li style="color: {logger.TextColor["attack"]};">Ful buff activated</li>'

                    player.PocketHitCounter = 0

                    logger.addRotation(pocketAbil.Name, True)

                    # Put it on cooldown
                    pocketAbil.putOnCooldown()

    return None
