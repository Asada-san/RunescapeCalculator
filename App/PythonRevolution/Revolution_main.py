from App.PythonRevolution import CombatChecks, CycleChecker as Cycle, \
    AttackCycle as Attack
from App.PythonRevolution.Objects import Loop, Dummy, Bar, Player


def fight_dummy(user_input, AbilityBook):
    """
    Initialises and simulates the player vs dummy fight.

    :param user_input: A dict containing the following:

        PLAYER OBJECT RELATED

        Abilities: array[string]

        afkStatus: boolean
        switchStatus: boolean
        baseDamage: float
        ShieldArmourValue: float
        DefenceLevel: float
        StrengthBoost: float
        MagicBoost: float
        RangedBoost: float
        StrengthPrayer: float
        MagicPrayer: float
        RangedPrayer: float

        HeightenedSenses: boolean
        FotS: boolean               --> Fury of the Small
        CoE: boolean                --> Conservation of Energy
        BerserkersFury: float
        StrengthCape: boolean
        RoV: boolean                --> Ring of Vigour
        MSoA: boolean               --> Masterwork Spear of Annihilation
        Aura: string
        Level20Gear: boolean
        Grimoire: boolean
        Precise: float
        Equilibrium: float
        Biting: float
        Flanking: float
        Lunging: float
        Caroming: float
        Ruthless: float
        Aftershock: float
        ShieldBashing: float
        Ultimatums: float
        Impatient: float
        Reflexes: boolean
        PlantedFeet: boolean

        DUMMY OBJECT RELATED

        movementStatus: boolean
        stunbindStatus: boolean
        nTargets: float

        SCRIPT RELATED

        simulationTime: string
        adrenaline: string
        HTMLwrite: boolean

    :param AbilityBook: Book containing every ability.
    :return: Results, warnings and error messages.
    """

    # cp = cProfile.Profile()
    # cp.enable()

    tick = .6  # Tick rate of RuneScape in seconds
    Do = Loop.DoList(user_input)

    # Start writing HTML text
    if Do.HTMLwrite:
        Do.Text = '----------------------------------------------------------------------------' \
                  '----------------------------------------------------------------------------' \
                  '----------------------------------------------------------------------------' \
                  '----------------------------------------------------------------------------' \
                  '--------------------------------------------------------<br><br>' \
                  '<ul style="width: 850px;">\n'

    # Create Combat Objects
    dummy = Dummy.Dummy(user_input, Do)
    player = Player.Player(user_input, Do)
    bar = Bar.AbilityBar(user_input, player, Do)

    # Get loop stuff
    loop = Loop.Loop()

    # Check user input for a possible value for simulation time and starting adrenaline
    if 1 <= user_input['simulationTime'] <= 3600 and 0 <= user_input['Adrenaline'] <= 100:
        # Don't look for repeating cycles
        loop.FindCycle = False

        loop.nMax = round(user_input['simulationTime'] / .6, 0)  # Set max runtime in ticks
        bar.Adrenaline = round(user_input['Adrenaline'], 0)  # Set starting adrenaline

        if Do.HTMLwrite:
            Do.Text += (
                f'<li style="color: {Do.init_color};">User select: Simulation Time: {user_input["simulationTime"]}</li>'
                f'<li style="color: {Do.init_color};">User select: Adrenaline: {user_input["Adrenaline"]}</li>')

    # Check for correct abilities and initialise the ability bar
    error, error_mes, warning = CombatChecks.AbilityBar_verifier(user_input, AbilityBook, bar, dummy, player, Do, loop)

    # If an error occurred in the Ability Bar verifier, return that error
    if error:
        return {}, warning, error_mes

    # Print start of revolution loop
    if Do.HTMLwrite:
        Do.Text += (f'<br><li style="color: {Do.start_color}"> INITIALISATION COMPLETE: starting loop<br><br>'
                    f'<li style="color: {Do.loop_color}; white-space: pre-wrap;">'
                    f'Total damage: 0'
                    f'<span style="float: right; margin-right: 18px;">Time: 0</span></li><br>')

    # The revolution loop
    while loop.runLoop and loop.n < loop.nMax + loop.CycleTime:

        if loop.SimulationTime > 300:
            Do.HTMLwrite = False

        # --------- PRE ATTACKING PHASE -----------------------
        # Status checks
        CombatChecks.TimerStatuses(bar, player, dummy, Do, loop)
        # -----------------------------------------------------

        # --------- ATTACKING PHASE ---------------------------
        # Perform the attack
        FireAbility = Attack.Attack_main(bar, player, dummy, Do, loop)
        # -----------------------------------------------------

        # --------- POST ATTACKING PHASE ----------------------
        # Check special cooldown phenomena involving FireAbility
        if bar.FireStatus:
            CombatChecks.PostAttackStatuses(bar, player, dummy, FireAbility, Do)

        # Check for other ability phenomena
        CombatChecks.PostAttackCleanUp(bar, player, dummy, Do)
        # -----------------------------------------------------

        # ---------- LOOP SHENANIGANS -------------------------
        # Increase the current simulation time of the rotation by a tick
        loop.SimulationTime += 1

        loop.n += 1
        loop.nCheck += 1

        # If a cycle has been found
        if loop.CycleFound:
            Cycle.CycleRotation(bar, player, dummy, Do, loop)

        # Print total damage and loop time depending if a cycle has been found or not
        if not loop.CycleFound:
            if Do.HTMLwrite:
                Do.Text +=(f'<br>\n<li style="color: {Do.loop_color}; white-space: pre-wrap;">'
                           f'Total damage: {round(dummy.Damage + dummy.PunctureDamage, 3)}'
                           f'<span style="float: right; margin-right: 18px;">Time: {round(loop.SimulationTime * .6, 1)}</span></li><br>\n')
        else:
            loop.CycleLoopTime += .6  # Add tick time

            if Do.HTMLwrite:
                Do.Text += (f'<br>\n<li style="color: {Do.cycle_color}; white-space: pre-wrap;">'
                            f'Cycle damage: {round(loop.CycleDamage + loop.CyclePunctureDamage, 3)}'
                            f'<span style="float: right; margin-right: 18px;">Cycle Time: {round(loop.CycleLoopTime, 1)}</span></li><br>\n')
        # -----------------------------------------------------

    if not loop.CycleFound:  # If no cycle has been found, change some result variables
        loop.CycleTime = loop.SimulationTime
        loop.CycleDamage = dummy.Damage
        loop.CyclePunctureDamage = dummy.PunctureDamage

    if player.PerkAftershock:
        # Increase max by 0.396 per rank and min 0.24 per rank
        AS_DamAvg = (0.396 * player.Ar + 0.24 * player.Ar) / 2 * player.BaseDamageEffective
        loop.CycleDamage += (loop.CycleDamage * AS_DamAvg / 50000) * dummy.nTarget

    loop.CycleDamage += loop.CyclePunctureDamage

    if loop.CycleDamage != 0:
        for entry in player.AbilInfo:
            player.AbilInfo[entry]['shared%'] = round(player.AbilInfo[entry]['damage'] / loop.CycleDamage * 100, 2)

    Results = {  # The output of main
        'AADPTPercentage': round(loop.CycleDamage / (loop.CycleTime / tick) / player.BaseDamage * 100, 3),
        'AADPT': round(loop.CycleDamage / (loop.CycleTime / tick), 3),
        'BaseDamage': player.BaseDamage,
        'SimulationTime': int(loop.n),
        'CycleTime': round(loop.CycleTime, 1),
        'CycleConvergenceTime': round(loop.CycleConvergenceTime, 1),
        'CycleDamage': round(loop.CycleDamage, 2),
        'CycleRotation': loop.Rotation,
        'CycleRedundant': loop.Redundant,
        'CycleBar': bar.AbilNames,
        'AbilityInfo': player.AbilInfo,
        'LoopText': Do.Text
    }

    # cp.disable()
    # cp.print_stats(sort='time')

    return Results, warning, error_mes


