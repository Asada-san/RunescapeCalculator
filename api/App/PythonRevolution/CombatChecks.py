from App.PythonRevolution import AverageDamageCalculator as AVGCalc, AttackCycle as Attack
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

    # Put user abilities on the bar object
    for user_ability in userInput['Abilities']:
        ability = deepcopy(AbilityBook[user_ability])

        logger.AbilInfo.update({ability.Name: {'damage': 0,
                                               'activations': 0,
                                               'shared%': 0}})

        if ability.Revolution or not player.Afk:
            bar.Rotation.append(ability)

            if ability.Name in {'Surge', 'Escape', 'Balanced Strike'}:
                warning.append(f'{ability.Name} should not be used with revolution')

                if logger.DebugMode:
                    logger.write(9, [ability.Name])
        else:
            warning.append(f'{ability.Name} is not activated by revolution \n')
            logger.Redundant.extend([ability.Name])

            if logger.DebugMode:
                logger.write(10, [ability.Name])

    # Create a list of ability names which are on the bar and their required weapon types and styles
    bar.AbilNames = [ability.Name for ability in bar.Rotation]
    bar.AbilEquipment = [ability.Equipment for ability in bar.Rotation]
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

    if player.Ring == 'StalkersRing' and bar.Style in {'Ranged', 'Typeless'} and \
            weapon in {'a 2h weapon', 'anything', 'shield'} and not player.Switcher:
        player.InitCritBuff = 0.03

    if logger.DebugMode:
        logger.write(11, [bar.Style, weapon])

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

    # Upgrade abilities
    for ability in bar.Rotation:
        ability.AbilityUpgrades(player, logger)

    return error, error_mes, warning


def PostAttackStatuses(bar, player, dummy, FireAbility, logger):
    """
    Checks and sets various statuses.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param FireAbility: The ability activated in the current attack cycle.
    :param logger: The Logger object.
    """

    # (Global) Cooldown shenanigans
    FireAbility.cdStatus = True
    FireAbility.cdTime = FireAbility.cdMax
    bar.GCDStatus = True
    bar.GCDTime = bar.GCDMax
    bar.FireStatus = False
    player.Cooldown.append(FireAbility)
    bar.SharedCooldowns(FireAbility, player, logger)

    if logger.DebugMode:
        logger.write(41, FireAbility.Name)

    # Status checks
    if FireAbility.Name in {'Meteor Strike', 'Tsunami', 'Incendiary Shot'}:
        player.CritAdrenalineBuffTime = 50
    # elif player.KerapacWristWraps and FireAbility.Name == 'Dragon Breath':
    #     player.DragonBreathCombustTime = 10

    if FireAbility.Boost:
        player.Boost = True
        player.BoostX = FireAbility.BoostX
        player.BoostTime = FireAbility.BoostTime

    if not dummy.StunBindImmune:

        if FireAbility.Stun:
            dummy.Stun = True
            dummy.StunTime = FireAbility.StunDur

            if logger.DebugMode:
                logger.write(43, dummy.StunTime)

        if FireAbility.Bind:
            dummy.Bind = True
            dummy.BindTime = FireAbility.BindDur

            if logger.DebugMode:
                logger.write(44, dummy.BindTime)

    return None


def PostAttackCleanUp(bar, player, dummy, logger):
    """
    Check for special effects of abilities and clears the current attack cycle list.

    :param bar: The Bar object.
    :param dummy:  The Dummy object.
    :param player: The Player object.
    :param logger: The DoList object.
    """

    # Special effect of Greater Flurry
    if 'Greater Flurry' in dummy.DamageNames and 'Berserk' in bar.AbilNames:
        IDX = bar.AbilNames.index('Berserk')

        if bar.Rotation[IDX].cdStatus:
            bar.Rotation[IDX].cdTime -= 2

    # Special effect of Needle Strike: 1.07x if next abil is standard or channeled hit
    if 'Needle Strike' in dummy.DamageNames:
        IDX = bar.AbilNames.index('Needle Strike')
        player.Boost1 = True
        player.Boost1X = bar.Rotation[IDX].Boost1X

        if logger.DebugMode:
            logger.write(45)

    # Clear the list of abilities which have inflicted damage on the dummy in the current tick
    dummy.DamageNames.clear()


