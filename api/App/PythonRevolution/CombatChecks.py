from App.PythonRevolution import AttackCycle as Attack
from copy import deepcopy


def AbilityBar_verifier(userInput, AbilityBook, bar, dummy, player, logger):
    """
    Verifies the user inputted bar and sets certain properties according.

    :param userInput: All options as provided by the user.
    :param AbilityBook: Book containing all existing abilities.
    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The Logger object.
    :return: Error with message and warning.
    """

    error = False
    error_mes = None
    warning = []

    # Check user ability bar input
    nAbils = len(userInput['Abilities'])  # Number of user inputted abilities

    if nAbils == 0:
        error = True
        error_mes = f'0 abilities in rotation, please select at least 1'

        return error, error_mes, warning

    noBasics = True
    # Put user abilities on the bar object
    for user_ability in userInput['Abilities']:
        ability = deepcopy(AbilityBook[user_ability])

        if ability.Type == 'Basic':
            noBasics = False

        logger.initAbility(ability.Name)

        if ability.Revolution or not player.Afk:
            bar.Rotation.append(ability)

            if ability.Name in {'Surge', 'Escape', 'Balanced Strike'}:
                warning.append(f'{ability.Name} should not be used with revolution')

                if logger.DebugMode:
                    logger.Text += f'<br>\n<li style="color: {logger.TextColor["damage"]};">WARNING: {ability.Name} should not be used with revolution</li>\n'

        else:
            warning.append(f'{ability.Name} is not activated by revolution \n')
            logger.Redundant.extend([ability.Name])

            if logger.DebugMode:
                logger.Text += f'<br>\n<li style="color: {logger.TextColor["damage"]};">WARNING: {ability.Name} is not activated by revolution</li>\n'

    # Check ability compatibility according to equipment
    if noBasics:
        error = True
        error_mes = f'A revolution bar needs at least 1 basic ability to work'

        return error, error_mes, warning

    # Add special abilities to the player object (purple section on the spreadsheet)
    SpecialAbils = []

    # Aftershock
    if player.PerkAftershock:
        SpecialAbils.append('Aftershock')

    # Pocket item
    if player.Pocket != 0:
        SpecialAbils.append(player.Pocket)

    for user_special_ability in SpecialAbils:
        special_ability = deepcopy(AbilityBook[user_special_ability])

        logger.initAbility(special_ability.Name)

        player.SpecialAbils.update({special_ability.Name: special_ability})

    # Create a list of ability names which are on the bar and their required weapon types and styles
    bar.AbilNames = [ability.Name for ability in bar.Rotation]
    bar.AbilStyles = [ability.Style for ability in bar.Rotation]

    # Sets the amount of abilities on the ability bar
    bar.N = len(bar.Rotation)

    # Check for duplicates and nonallowables
    for i in range(0, bar.N):
        InvalidIDX = None

        for j in range(0, len(bar.Invalid)):
            if bar.Rotation[i].Name in bar.Invalid[j]:
                InvalidIDX = j
                break

        for j in range(0, bar.N):  # Compare it with all other abilities
            if j == i:  # (same ability --> meaningless)
                continue

            # USE THIS CODE IF USER IS ALLOWED TO PUT IN DUPLICATE ABILITIES
            # if bar.Rotation[i].Name == bar.Rotation[j].Name:
            #     error = True
            #     error_mes = f'{bar.Rotation[i].Name} has multiple appearances on the ability bar'
            #
            #     return error, error_mes, warning

            # If ability j also in disallowed group with idx DisallowedIDX, return error
            if InvalidIDX is not None and bar.Rotation[j].Name in bar.Invalid[InvalidIDX]:
                error = True
                error_mes = f'{bar.Rotation[i].Name} and {bar.Rotation[j].Name} cannot appear together'

                return error, error_mes, warning

    # Check ability compatibility according to cb style
    if all(styles in ['Constitution', 'Defence', 'ANY'] for styles in bar.AbilStyles):
        bar.Style = 'Typeless'
    elif all(styles in ['Magic', 'Constitution', 'Defence', 'ANY'] for styles in bar.AbilStyles):
        bar.Style = 'Magic'
    elif all(styles in ['Ranged', 'Constitution', 'Defence', 'ANY'] for styles in bar.AbilStyles):
        bar.Style = 'Ranged'
    elif all(styles in ['Strength', 'Attack', 'Constitution', 'Defence', 'ANY'] for styles in bar.AbilStyles):
        bar.Style = 'Melee'
    else:
        error = True
        error_mes = f'The ability bar consists of abilities of varying combat styles<br>\n'

        return error, error_mes, warning

    # Set various player values depending on bar style
    if bar.Style == 'Melee':
        player.BaseDamageEffective *= player.StrengthPrayerBoost
        player.BashBaseDamage *= player.StrengthPrayerBoost

        if player.Aura == 'Berserker':
            player.BaseBoost = 1.1

        player.LevelBoost = player.StrengthLevelBoost

    elif bar.Style == 'Ranged':
        player.BaseDamageEffective *= player.RangedPrayerBoost
        player.BashBaseDamage *= player.RangedPrayerBoost

        if player.Aura == 'Reckless':
            player.BaseBoost = 1.1

        player.LevelBoost = player.RangedLevelBoost

    elif bar.Style == 'Magic':
        player.BaseDamageEffective *= player.MagicPrayerBoost
        player.BashBaseDamage *= player.MagicPrayerBoost

        if player.Aura == 'Maniacal':
            player.BaseBoost = 1.1

        player.LevelBoost = player.MagicLevelBoost

    elif bar.Style == 'Typeless':
        player.BaseDamageEffective *= max(player.StrengthPrayerBoost, player.RangedPrayerBoost, player.MagicPrayerBoost)
        player.BashBaseDamage *= max(player.StrengthPrayerBoost, player.RangedPrayerBoost, player.MagicPrayerBoost)

        if player.Aura in {'Berserker', 'Maniacal', 'Reckless'}:
            player.BaseBoost = 1.1

        player.LevelBoost = max(player.StrengthLevelBoost, player.RangedLevelBoost, player.MagicLevelBoost)

    # Check for Dragon Breath effect
    if dummy.nTarget > 1 and 'Dragon Breath' in bar.AbilNames:
        player.DragonBreathGain = True

    # Upgrade special abilities (option check)
    for special_ability_name in player.SpecialAbils.keys():
        special_ability = player.SpecialAbils[special_ability_name]

        special_ability.AbilityUpgrades(player, logger)

        # Get AoE hits
        if all([dummy.nTarget > 1 and special_ability.AoE]):
            special_ability.AoECheck(dummy, player)

    # Upgrade abilities (option check)
    for ability in bar.Rotation:
        ability.AbilityUpgrades(player, logger)

        # Get AoE hits
        if any([ability.Name == 'Greater Ricochet', all([dummy.nTarget > 1 and ability.AoE])]):
            ability.AoECheck(dummy, player)

    bar.AbilEquipment = [ability.Equipment for ability in bar.Rotation]

    # Check ability compatibility according to equipment
    if not player.Switcher and all(equipment in bar.AbilEquipment for equipment in ['2h', 'dual', 'shield']):
        error = True
        error_mes = f'The ability bar consists of 2h, dual and shield abilities'

        return error, error_mes, warning

    elif not player.Switcher and all(equipment in bar.AbilEquipment for equipment in ['2h', 'dual']):
        error = True
        error_mes = f'The ability bar consists of 2h and dual abilities'

        return error, error_mes, warning

    elif not player.Switcher and all(equipment in bar.AbilEquipment for equipment in ['2h', 'shield']):
        error = True
        error_mes = f'The ability bar consists of 2h and shield abilities'

        return error, error_mes, warning

    elif not player.Switcher and all(equipment in bar.AbilEquipment for equipment in ['shield', 'dual']):
        error = True
        error_mes = f'The ability bar consists of shield and dual abilities'

        return error, error_mes, warning

    elif sum(equipment in bar.AbilEquipment for equipment in ['2h', 'dual', 'shield']) > 1:
        weapon = 'multiple weapons, covered in sweat'
    elif '2h' in bar.AbilEquipment:
        weapon = 'a 2h weapon'
    elif 'dual' in bar.AbilEquipment:
        weapon = 'dual weapons'
    elif 'shield' in bar.AbilEquipment:
        weapon = 'a shield'
    else:
        weapon = 'anything'

    if player.Ring == 'StalkersRing' and bar.Style in {'Ranged', 'Typeless'} and \
            weapon in {'a 2h weapon', 'anything', 'shield'} and not player.Switcher:
        player.InitCritBuff = 0.03

    if logger.DebugMode:
        logger.Text += f'<li style="color: {logger.TextColor["initialisation"]};">Ability bar consists of {bar.Style} abilities and can be used with {weapon}</li>'

    return error, error_mes, warning


def PostAttackStatuses(player, dummy, FireAbility, logger):
    """
    Checks and sets various statuses.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param FireAbility: The ability activated in the current attack cycle.
    :param logger: The Logger object.
    """

    # (Global) Cooldown shenanigans
    player.Bar.putOnGlobalCooldown()

    if logger.DebugMode:
        logger.Text += f'<li style="color: {logger.TextColor["normal"]};">{FireAbility.Name} went on cooldown</li>' \
                f'<li style="color: {logger.TextColor["normal"]};">GCD activated</li>'

    # if player.KerapacWristWraps and FireAbility.Name == 'Dragon Breath':
    #     player.DragonBreathCombustTime = 10

    if FireAbility.Boost:
        player.addBoost(FireAbility)

    if FireAbility.Boost1:
        player.addBoost1(FireAbility)

    if player.Gloves.Name in {'Gloves of Passage', 'Enhanced gloves of Passage'} and FireAbility.Name in {'Smash', 'Havoc'}:
        player.GlovesOfPassageTime = player.GlovesOfPassageMax
        player.GlovesOfPassageBoost += .2

    if FireAbility.Bleed:
        dummy.isBleeding = True

    if not dummy.StunBindImmune:

        if FireAbility.StunDuration:
            dummy.StunTime = FireAbility.StunDuration

            if logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy is Stunned for {dummy.StunTime}s</li>'

        if FireAbility.BindDuration:
            dummy.BindTime = FireAbility.BindDuration

            if logger.DebugMode:
                logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy is Bound for {dummy.BindTime}s</li>'

    return None


def PostAttackCleanUp(player, dummy, logger):
    """
    Check for special effects of abilities and clears the current attack cycle list.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The DoList object.
    """

    # Special effect of Greater Flurry
    if 'Greater Flurry' in dummy.DamageNames and 'Berserk' in player.Bar.AbilNames:
        IDX = player.Bar.AbilNames.index('Berserk')

        if player.Bar.Rotation[IDX].cdTime:
            player.Bar.Rotation[IDX].cdTime -= 2
            player.Bar.Rotation[IDX].cdTime = max(0,  player.Bar.Abilities[IDX].cdTime)

    # Clear the list of abilities which have inflicted damage on the dummy in the current tick
    dummy.DamageNames.clear()

    # Check for Aftershock perk activation
    if player.Aftershock:
        Aftershock = player.Special['Aftershock']

        if not Aftershock.cdTime:

            if player.AsDamage > 50000:
                dummy.PHits[dummy.nPH: dummy.nPH + Aftershock.nHits] = deepcopy(Aftershock.Hits)
                dummy.nPH += Aftershock.nHits

                # Reset Aftershock damage
                player.AsDamage = 0

                logger.addRotation(Aftershock.Name, True)

            # Put it on cooldown whether it has been activated or not
            Aftershock.putOnCooldown()
