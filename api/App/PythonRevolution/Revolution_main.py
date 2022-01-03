from App.PythonRevolution import CombatChecks, CycleChecker as Cycle, \
    AttackCycle as Attack
from App.PythonRevolution.Objects.Logger import Logger
from App.PythonRevolution.Objects.Dummy import Dummy
from App.PythonRevolution.Objects.Player import Player
from App.PythonRevolution.Objects.Bar import AbilityBar
from App.PythonRevolution.Objects.Settings import Settings


def fight_dummy(userInput, AbilityBook):
    """
    Initialises and simulates the player vs dummy fight.

    :param userInput: A dict containing the following:

        ABILITY BAR

        Abilities: list[string]     --> [<ability_name_1>, <ability_name_2>, ..., <ability_name_14>]

        PLAYER

        afkStatus: boolean
        switchStatus: boolean
        baseDamage: float           --> 0 <= x <= 10000

        STRENGTH BOOST

        StrengthBoost: float        --> 0 <= x <= 60
        StrengthPrayer: float       --> [1, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12]

        MAGIC BOOST

        MagicBoost: float           --> 0 <= x <= 60
        MagicPrayer: float          --> [1, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12]

        RANGED BOOST

        RangedBoost: float          --> 0 <= x <= 60
        RangedPrayer: float         --> [1, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12]

        BASH ABILITY

        ShieldArmourValue: float    --> 0 <= x <= 1000
        DefenceLevel: float         --> 0 <= x <= 200

        INVENTION PERKS

        Level20Gear: boolean
        Precise: float              --> [0, 1, 2, 3, 4, 5, 6]
        Equilibrium: float          --> [0, 1, 2, 3, 4]
        Biting: float               --> [0, 1, 2, 3, 4]
        Flanking: float             --> [0, 1, 2, 3, 4]
        Lunging: float              --> [0, 1, 2, 3, 4]
        Caroming: float             --> [0, 1, 2, 3, 4]
        Ruthless: float             --> [0, 1, 2, 3]
        Aftershock: float           --> [0, 1, 2, 3, 4]
        ShieldBashing: float        --> [0, 1, 2, 3, 4]
        Ultimatums: float           --> [0, 1, 2, 3, 4]
        Impatient: float            --> [0, 1, 2, 3, 4]
        Reflexes: boolean
        PlantedFeet: boolean

        EQUIPMENT

        MSoA: boolean               --> Masterwork Spear of Annihilation
        Grimoire: boolean
        StrengthCape: boolean
        Ring: string                --> 'RoV', 'ChampionsRing', 'ChannelersRing', 'ReaversRing', 'StalkersRing'
        Aura: string                --> 'Berserker', 'Maniacal', 'Reckless', 'Equilibrium'
        Cape: string                --> 'StrengthCape', 'Igneous Kal-Ket', 'Igneous Kal-Mej', 'Igneous Kal-Xil'
        Pocket: string              --> 'Book of War', 'Book of Balance', 'Book of Law', 'Book of Wisdom', 'Book of Chaos', 'Ancient Book', 'Scripture of Wen', 'Scripture of Jas', 'Scripture of Ful'

        ARCHAEOLOGY RELICS

        HeightenedSenses: boolean
        FotS: boolean               --> Fury of the Small
        CoE: boolean                --> Conservation of Energy
        BerserkersFury: float       --> 0 <= x <= 5.5

        DUMMY OBJECT

        movementStatus: boolean
        stunbindStatus: boolean
        nTargets: float             --> 1 <= x <= 30

        PYTHON SCRIPT

        simulationTime: float       --> 0 <= x <= 3600
        adrenaline: string          --> 0 <= x <= 100
        Debug: boolean

    :param AbilityBook: Book containing every ability.
    :return: Results, warnings and error messages.
    """

    # cp = cProfile.Profile()
    # cp.enable()

    logger = Logger()
    
    settings = Settings(userInput)

    if settings.Debug:
        logger.DebugMode = True

    if logger.DebugMode:
        logger.write(0)
        logger.write(2, userInput)

    # Initialise Combat Objects
    dummy = Dummy(userInput)
    player = Player(userInput)
    bar = AbilityBar(userInput)

    # Check for correct abilities and initialise the ability bar
    error, error_mes, warning = CombatChecks.AbilityBar_verifier(userInput, AbilityBook, bar, dummy, player, logger)

    # If an error occurred in the Ability Bar verifier, return that error
    if error:
        return {}, warning, error_mes

    # Print start of revolution logger
    if logger.DebugMode:
        logger.write(12)

    # The revolution loop
    while settings.run and logger.n < settings.nMax + logger.CycleTime:

        if logger.n > 300:
            logger.DebugMode = False

        # --------- PRE ATTACKING PHASE -----------------------
        # Status checks
        bar.TimerCheck(logger)  # CHECK GLOBAL COOLDOWN TIMER
        dummy.TimerCheck(logger)  # CHECK STUN AND BIND STATUS TIMERS
        player.TimerCheck(dummy, logger)  # CHECK PLAYER COOLDOWNS/BUFFS/BOOSTS/CHANNEL TIMERS
        # -----------------------------------------------------

        # --------- ATTACKING PHASE ---------------------------
        # Possibly activate an ability and get its hits
        FireAbility = Attack.useAbility(bar, player, dummy, logger, settings)

        if not settings.run:
            break

        # Check for any hits that need to inflict damage in the current tick
        Attack.PHitCheck(bar, dummy, player, logger, settings)
        # -----------------------------------------------------

        # --------- POST ATTACKING PHASE ----------------------
        # Check special cooldown shenanigans involving FireAbility
        if bar.FireStatus:
            CombatChecks.PostAttackStatuses(bar, player, dummy, FireAbility, logger)

        # Check for other ability shenanigans
        CombatChecks.PostAttackCleanUp(bar, player, dummy, logger)
        # -----------------------------------------------------

        # ---------- logger SHENANIGANS -------------------------
        # Increase the current simulation time of the rotation by a tick
        logger.n += 1
        logger.nCheck += 1

        if True:
            dummy.updateTickInfo()
            logger.updateTickInfo()

        # Print total damage and logger time depending if a cycle has been found or not
        if logger.DebugMode:
            logger.write(46, [round(dummy.Damage, 3), logger.n])
        # -----------------------------------------------------

    for name, value in logger.AbilInfo.items():
        if value['activations'] == 0:
            logger.Redundant.append(name)

    if not logger.CycleFound:  # If no cycle has been found, change some result variables
        logger.CycleTime = logger.n

        if settings.FindCycle:
            logger.Rotation = [f'<span style="color: {logger.TextColor["cycle"]}">NO CYCLE HAS BEEN FOUND IN 6000 TICKS!!! DPT RESULT GIVEN INSTEAD!</span>']
        else:
            logger.Rotation = [f'<span style="color: {logger.TextColor["cycle"]}">N/A</span>']

    for entry in logger.AbilInfo:
        if dummy.Damage != 0:
            logger.AbilInfo[entry]['shared%'] = round(logger.AbilInfo[entry]['damage'] / dummy.Damage * 100, 2)

    Results = {  # The output of main
        'AADPTPercentage': round(dummy.Damage / logger.CycleTime / player.BaseDamage * 100, 3),
        'AADPT': round(dummy.Damage / logger.CycleTime, 3),
        'BaseDamage': player.BaseDamage,
        'SimulationTime': int(logger.n),
        'CycleTime': round(logger.CycleTime, 1),
        'CycleConvergenceTime': round(logger.CycleConvergenceTime, 1),
        'CycleDamage': round(dummy.Damage, 2),
        'CycleDamagePerTick': dummy.DamagePerTick,
        'CycleDamageIncrement': dummy.DamageIncrement,
        'CycleFound': logger.CycleFound,
        'CycleRotation': logger.Rotation,
        'CycleRedundant': logger.Redundant,
        'CycleBar': bar.AbilNames,
        'AbilityInfo': logger.AbilInfo,
        'AbilityInfoPerTick': logger.CycleAbilityDamagePerTick,
        'LoggerText': logger.Text,
        'DamagePerDummy': dummy.DamagePerDummyIncrement
    }

    # cp.disable()
    # cp.print_stats(sort='time')

    return Results, warning, error_mes
