from PythonRevolution import CycleChecker as Cycle
import pprint
import numpy as np
from copy import deepcopy


def Attack_main(bar, player, dummy, Do, loop):
    FireAbility = None

    # CHECK IF THE PLAYER IS ALLOWED TO ATTACK
    # If no GCD and player is not using channeled ability
    if not bar.GCDStatus and not player.ChanAbil:

        ##############################################################
        ################# Check for possible Cycle ###################
        ##############################################################

        # if loop.FindCycle and not loop.CycleFound and 1 == 2:  # Used for debugging
        if loop.FindCycle and not loop.CycleFound:  # If we want to find a cycle and the cycle has not yet been found
            Cycle.CycleCheck(bar, player, dummy, Do, loop)

        ##############################################################
        ############### Check for available ability ##################
        ##############################################################

        # For all abilities on the ability bar
        for i in range(0, bar.N):

            # If the ability is not on cooldown
            if not bar.Rotation[i].cdStatus:
                # Check if the ability is allowed to fire according to its type and current adrenaline
                bar.AdrenalineStatus(bar.Rotation[i].Type)

                # If the ability is allowed to fire
                if bar.FireStatus:
                    bar.FireN = i  # Index of ability is equal to for loop i

                    # If a cycle has been found
                    if loop.CycleFound:
                        loop.Rotation.extend([bar.Rotation[i].Name])

                        if not loop.nFA[bar.FireN]:
                            loop.nFA[bar.FireN] = True

                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.nor_color};">Attack status: {bar.Rotation[i].Name} ready</li>\n'

                    break  # Break because firing more than 1 ability wouldn't make sense

                else:  # Else there is not enough adrenaline
                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.init_color};">Not enough Adrenaline for {bar.Rotation[i].Name}</li>\n'

        ##############################################################
        ## Do stuff based on whether an ability was available or not #
        ##############################################################

        # If an ability is allowed to fire, ATTACK THE DUMMY!!!
        if bar.FireStatus:
            FireAbility = AttackDummy(bar, player, dummy, Do, loop)
        # Else there was insufficient adrenaline or all abilities were on cooldown
        else:
            if loop.CycleFound:  # If a cycle has been found, print STALL xN
                if len(loop.Rotation) != 0 and 'STALL' in loop.Rotation[-1]:
                    loop.nStall += 1
                    loop.Rotation[-1] = f'<span style="color: {Do.cycle_color}">STALL {loop.nStall}x</span>'
                else:
                    loop.nStall = 1
                    loop.Rotation.extend([f'<span style="color: {Do.cycle_color}">STALL {loop.nStall}x</span>'])

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.imp_color};">No ability available, skip attack</li>\n'

    elif player.ChanAbil:  # Elif the player is using a channeled ability
        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.imp_color};">Player is using a channeled ability</li>\n'

    elif bar.GCDStatus:  # Elif the ability bar is on global cooldown
        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.imp_color};">GLOBAL COOLDOWN</li>\n'

    return FireAbility


def AttackDummy(bar, player, dummy, Do, loop):

    FA = bar.Rotation[bar.FireN]  # FireAbility: ability to be fired in the current tick

    if Do.HTMLwrite:
        if not all([FA.StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            Do.Text += f'<li style="color: {Do.att_color};">{FA.Name} activated (normal)\n'
        else:
            Do.Text += f'<li style="color: {Do.imp_color};">{FA.Name} activated (stun&bind)\n'

        Do.Text += f'<li style="color: {Do.att_color};">Adrenaline: {round(bar.Adrenaline, 0)}</li>\n'

    ##############################################################
    ##### Depending on the type of ability, get its hits #########
    ##############################################################

    # If its a standard or channeled ability
    if FA.Standard or FA.Channeled:
        # Determine which type of ability damage to apply, normal or stun&bind
        if not all([FA.StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.Hits)
        else:
            dummy.PHits[dummy.nPH: dummy.nPH + FA.nS] = deepcopy(FA.HitsStunBind)

        if any([FA.Bleed, FA.Puncture]):  # If standard ability also has an effect
            EffectCheck(bar, dummy, player, FA, Do)
    # Elif the ability has an effect
    elif FA.Bleed:
        EffectCheck(bar, dummy, player, FA, Do)
    # Else the ability doesn't do any damage: end this function
    else:
        return FA

    ##############################################################
    ####### Determine amount of hits pending for dummy ###########
    ##############################################################

    # If the player is semi afk, some abilities are cut short to maximise dps
    if not player.Afk and FA.Name == 'Concentrated Blast':
        dummy.nPH += FA.nT - 1
    else:
        dummy.nPH += FA.nT

    ##############################################################
    ################ Check for AoE shenanigans ###################
    ##############################################################

    # If the user selected more than 1 target
    if dummy.nTarget > 1 and FA.AoE:
        AoECheck(bar, dummy, player, FA, Do)

    ##############################################################
    ############# (Potentially) attack the dummy #################
    ##############################################################

    DummyDamage(bar, dummy, player, Do, loop)  # Inflict damage if time equals 0

    return FA


def EffectCheck(bar, dummy, player, FA, Do):

    ##############################################################
    ### Determine whether ability has bleed or puncture effect ###
    ##############################################################

    if FA.Bleed:  # If the ability has a bleed effect
        dummy.PHits[dummy.nPH + FA.nS: dummy.nPH + FA.nT] = deepcopy(FA.DoTHits)

    elif FA.Puncture:  # Elif the ability has a puncture effect

        ##############################################################
        ########## Delete puncture effect from pending hits ##########
        ##############################################################

        # Standard attack already has been added, thus add it to nDoT during the removal
        dummy.nPH += FA.nS

        # Check every ability for puncture type, if so move the hit to idx dummy.nPH - 1 and move i + 1: dummy.nPH 1 slot to the left
        for i in range(dummy.nPH - 1, -1, -1):
            if dummy.PHits[i].Type == 4:

                dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]

                dummy.nPH -= 1

        # Decrease nDoT by 1 again for consistency with other effects
        dummy.nPH -= FA.nS

        ##############################################################
        ############### Salt the Wound ability effect ################
        ##############################################################

        if FA.Name == 'Salt the Wound':
            IDX = bar.AbilNames.index(FA.Name)  # Spot of the ability on the bar

            Hit = deepcopy(FA.Hits[0])  # Copy the hit from the ability to fire

            # Calculate its new average
            Hit.Damage = bar.Rotation[IDX].StandardChannelDamAvgCalc(player, Do, 'Salt the Wound', FA.Hits[0].Index, dummy.nPuncture)[0]

            dummy.PHits[dummy.nPH] = Hit  # Put the hit with the new average in the pending hits

            dummy.nPuncture = 0  # Reset stack

            return None

        ##############################################################
        #################### Set puncture stack ######################
        ##############################################################

        if dummy.nPuncture < 10:  # Stacks are capped at 10
            dummy.nPuncture += 1

        dummy.PHits[dummy.nPH + FA.nS: dummy.nPH + FA.nT] = deepcopy(FA.DoTHits)

    return None


def AoECheck(bar, dummy, player, FA, Do):
    nDT = dummy.nTarget  # Number of targets which will potentially receive damage

    ######################### Quake ##############################

    if FA.Name == 'Quake':
        # DamMax = 1.88, DamMin = 0.376, DamAvg = 1.128 for side targets

        N = FA.nT

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i: dummy.nPH + i] = deepcopy(FA.SideTargetAvg)
            dummy.PHits[dummy.nPH + i].Target = i + 2

    #################### Greater Flurry ##########################

    elif FA.Name == 'Greater Flurry':
        # DamMax = 0.94, DamMin = 0.2, DamAvg = 0.57 for ALL! targets

        N = FA.nT

        for i in range(0, nDT):
            dummy.PHits[dummy.nPH + (i - 1) * N: dummy.nPH + i * N] = deepcopy(FA.SideTargetAvg)

            if i > 0:
                for j in range(0, N):
                    dummy.PHits[dummy.nPH + (i - 1) * N + j].Target = i + 1

    ###################### Hurricane #############################

    elif FA.Name == 'Hurricane':
        # First hit on main target equals the hit for all other targets, set FA.nT to 1 since its 2

        N = FA.nT - 1

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i] = deepcopy(dummy.PHits[dummy.nPH - 2])
            dummy.PHits[dummy.nPH + i].Target = i + 2

    ################ Corruption Blast/Shot #######################

    elif FA.Name in {'Corruption Blast', 'Corruption Shot'}:
        # First hit only on main target. then spreading to all other targets

        N = FA.nT - 1

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2

    #################### Chain/Ricochet ##########################

    elif FA.Name in {'Chain', 'Ricochet'}:
        # Ricochet and Chain only hit up to 3 targets

        if nDT > 3 + player.Cr:  # If number of damageable targets is larger than 3, set nDT to 3.
            nDT = int(3 + player.Cr)

        N = FA.nT

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2

    #################### Everything else #########################
    
    else:
        N = FA.nT

        for i in range(0, nDT - 1):
            dummy.PHits[dummy.nPH + i * N: dummy.nPH + (i + 1) * N] = deepcopy(dummy.PHits[dummy.nPH - N: dummy.nPH])

            for j in range(0, N):
                dummy.PHits[dummy.nPH + i * N + j].Target = i + 2
    
    # Increase dummy.nPH by the amount of hits N every other target nDT - 1 receives
    dummy.nPH += (nDT - 1) * N

    return None


def DummyDamage(bar, dummy, player, Do, loop):

    ##############################################################
    ################ Check if dummy takes a hit ##################
    ##############################################################

    # For every Pending Hit
    for i in range(dummy.nPH - 1, -1, -1):

        # If a DoT time reached zero: do damage
        if dummy.PHits[i].Time <= 0.01:

            ##############################################################
            ############ Determine bleed damage multiplier ###############
            ##############################################################

            # If cause is a bleed and the dummy is able to move and there are no stuns/binds active on the dummy
            if dummy.PHits[i].Type == 3 and dummy.Movement and not any([dummy.Stun, dummy.Bind]):
                IDX = bar.AbilNames.index(dummy.PHits[i].Name)

                dummy.PHits[i].Damage *= bar.Rotation[IDX].BleedOnMove

            ##############################################################
            ############### Determine average hit damage #################
            ##############################################################

            # If its a standard or channeled hit and there is a Critical hit buff or boost active
            if dummy.PHits[i].Type in {1, 2} and any([player.AbilCritBuff > 0, player.Boost, player.Boost1]):

                # Recalculate the average hit
                HitDamage = CalcNewAvg(bar, dummy, player, Do, i)

                if Do.HTMLwrite and any([player.Boost, player.Boost1]):
                    Do.Text += f'<li style="color: {Do.att_color};">{dummy.PHits[i].Name} hit boosted {player.BoostX * player.Boost1X}x</li>'

                # The single hit damage boost works on the first 2 hits on rapid fire fore some reason
                if any([dummy.PHits[i].Name not in ['Rapid Fire', 'Snap Shot'] and player.Boost1, player.Boost1 and int(dummy.PHits[i].Index) == 1]):
                    player.Boost1 = False
                    player.Boost1X = 1

            # Elif using the Reckless, Maniacal or Berserker aura's and an ability damage boosting ability has been used
            elif dummy.PHits[i].Type in {3, 4} and player.BaseBoost > 1 and player.Boost:

                # If a new bleed effect has been initiated and there was a single boost, reset it
                if dummy.PHits[i].Index == 0 and player.Boost1:
                    player.Boost1 = False
                    player.Boost1X = 1

                # Recalculate the average hit
                HitDamage = CalcNewAvg(bar, dummy, player, Do, i)

            else:

                # Damage is normal average damage
                HitDamage = dummy.PHits[i].Damage

            ##############################################################
            ############ Add the damage to the total damage ##############
            ##############################################################

            if dummy.PHits[i].Type != 4:
                dummy.Damage += HitDamage
            else:
                dummy.PunctureDamage += HitDamage

            if loop.CycleFound:  # If a cycle has been found
                if dummy.PHits[i].Type != 4:
                    loop.CycleDamage += HitDamage
                else:
                    loop.CyclePunctureDamage += HitDamage

            if Do.HTMLwrite:
                if dummy.nTarget == 1:
                    Do.Text += f'<li style="color: {Do.dam_color};">{dummy.PHits[i].Name} ({Do.TypeDict[dummy.PHits[i].Type]}) damage applied: {round(HitDamage, 3)}</li>\n'
                else:
                    Do.Text += f'<li style="color: {Do.dam_color};">{dummy.PHits[i].Name} ({Do.TypeDict[dummy.PHits[i].Type]}) damage applied on target #{int(dummy.PHits[i].Target)}: {round(HitDamage, 3)}</li>\n'

            ##############################################################
            ################ Critical hit chance checks ##################
            ##############################################################

            # If the hit was caused by Concentrated Blast or Fury
            if dummy.PHits[i].Name in {'Concentrated Blast', 'Fury'}:
                if player.CritStack == 3:  # If the stack reached 3, reset
                    player.CritStack = 0
                else:  # Increase AbilCritBuff
                    if player.AbilCritBuff < 0.15:  # If the AbilCritBuff is smaller than 15%, increase by 5%
                        player.AbilCritBuff += 0.05
                player.CritStack += 1  # Increase stack

            # Elif the hit was caused by Greater Fury
            elif dummy.PHits[i].Name == 'Greater Fury' or all([player.CritAdrenalineBuffTime > 0, dummy.PHits[i].Type in {1, 2}]):
                player.CritStack = 0  # Reset stack

                # If there is an adrenaline boost (crit dependent) due to Meteor Strike, Sunshine or Incendiary Shot
                if player.CritAdrenalineBuffTime > 0:
                    player.CritAdrenalineBuff = True  # We need to perform a check

                    # Calculate the average adrenaline gain
                    CalcNewAvg(bar, dummy, player, Do, i)

                    # Add the adrenaline gain to the total adrenaline
                    bar.Adrenaline += round(player.BasicAdrenalineGain / 1, 0)

                    if Do.HTMLwrite:
                        Do.Text += f'<li style="color: {Do.att_color};">Adrenaline increased by: {round(player.BasicAdrenalineGain / 1, 0)} to: {round(bar.Adrenaline, 0)}</li>\n'

                    # Subtract the added adrenaline from the gained adrenaline due to the boost
                    player.BasicAdrenalineGain -= round(player.BasicAdrenalineGain / 1, 0)

                    player.AbilCritBuff = 0  # Reset crit buff

                if dummy.PHits[i].Name == 'Greater Fury':
                    player.AbilCritBuff = 0  # Reset crit buff

                    player.GreaterFuryCritCheck = True  # We need to perform a check

                    # Calculate the average crit change used for next attack cycle
                    CalcNewAvg(bar, dummy, player, Do, i)

            elif dummy.PHits[i].Type in {1, 2}:
                player.CritStack = 0  # Reset stack
                player.AbilCritBuff = 0  # Reset crit buff

            ##############################################################
            ##################### Delete the Hit #########################
            ##############################################################

            # Append the name of the ability to the list of damaging abilities in the current tick
            dummy.DamageNames.append(dummy.PHits[i].Name)

            # Shift the current hit to the right and others after that 1 place to the left
            dummy.PHits[i: dummy.nPH - 1], dummy.PHits[dummy.nPH - 1] = dummy.PHits[i + 1: dummy.nPH], dummy.PHits[i]

            # For every hit, the number of Pending Hits left decreases by 1
            dummy.nPH -= 1

    ##############################################################
    #### Determine if dummy takes damage outside attack cycle ####
    ##############################################################

    if dummy.nPH == 0:  # If there are no hits left to be done, set DoT to False
        dummy.PH = False
        dummy.nPuncture = 0

    elif 4 not in [Hit.Type for Hit in dummy.PHits[0: dummy.nPH]]:  # Elif the are no puncture DoTs anymore in the list
        dummy.nPuncture = 0
        dummy.PH = True

    else:
        dummy.PH = True

    return None


def CalcNewAvg(bar, dummy, player, Do, i):

    ##############################################################
    ############# Calculate new avg depending on type ############
    ##############################################################

    IDX = bar.AbilNames.index(dummy.PHits[i].Name)  # Spot of the ability on the bar

    if dummy.PHits[i].Type in {1, 2}:

        if not all([bar.Rotation[IDX].StunBindDam,  any([dummy.Stun, dummy.Bind])]):
            Avg = bar.Rotation[IDX].StandardChannelDamAvgCalc(player, Do, 'Normal', dummy.PHits[i].Index)
        else:
            Avg = bar.Rotation[IDX].StandardChannelDamAvgCalc(player, Do, 'StunBind', dummy.PHits[i].Index)

    elif dummy.PHits[i].Type in {3, 4}:

        Avg = bar.Rotation[IDX].BleedDamAvgCalc(player, Do)

    ##############################################################
    ########### Return the new Average if its not None ###########
    ##############################################################

    if Avg is not None:
        return Avg[0]
    else:
        return None
