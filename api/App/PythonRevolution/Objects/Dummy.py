from App.PythonRevolution import AttackCycle as Attack
import numpy as np
from copy import deepcopy


class Dummy:
    """
    The Dummy class. A dummy mimics a (stationary) monster.
    """

    def __init__(self, userInput):
        if userInput['nTargets'] > 0:
            self.nTarget = int(userInput['nTargets'])            # Number of targets
        else:
            self.nTarget = 1

        self.Damage = 0                 # The total amount of damage done
        self.DamagePreviousTick = 0     # The total amount of damage done up until the last tick
        self.DamagePerTick = []         # List containing the damage done per tick
        self.DamageIncrement = [0]      # List containing the total damage done per tick
        self.DamagePerDummy = [0] * self.nTarget                                # Contains the total damage done to a dummy per dummy
        self.DamagePerDummyIncrement = [[0] for _ in range(0, self.nTarget)]    # List of lists containing the total damage done to a dummy per dummy per tick

        self.StunTime = 0               # Time before a stun wears of
        self.BindTime = 0               # Time before a bind wears of
        self.DamageNames = []           # List of abilities which caused damage to the dummy in the current tick
        self.PHits = [0] * 50           # List of Pending Hits
        self.nPH = 0                    # Amount of Pending Hits
        self.nPuncture = 0              # Amount of puncture stacks on dummy
        self.PunctureTime = 0           # Duration of the Puncture effect before the stack is reset

        self.isBleeding = False

        self.Movement = not userInput['movementStatus']       # True if the dummy can move
        self.StunBindImmune = userInput['stunbindStatus']     # True if the dummy is Stun and Bind immune

    def TimerCheck(self, logger):
        """
        Check the Bind and Stun status of the dummy.

        :param logger: the Logger object.
        """

        if self.StunTime:
            self.StunTime -= 1

            if not self.StunTime:
                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy no longer stunned</li>'

        if self.BindTime:
            self.BindTime -= 1

            if not self.BindTime:
                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy no longer bound</li>'

        if self.PunctureTime:
            self.PunctureTime -= 1

            if not self.PunctureTime:
                self.nPuncture = 0

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["status"]};">Dummy puncture stack reset to 0</li>'

        if self.isBleeding:
            bleedAbil = False
            for i in range(self.nPH - 1, -1, -1):
                if self.PHits[i].Type == 3:
                    bleedAbil = True
                    break

            self.isBleeding = bleedAbil

    def updateTickInfo(self):
        # Get damage done in current tick
        self.DamagePerTick.append(self.Damage - self.DamageIncrement[-1])

        # Calculate new total damage up until current tick
        self.DamageIncrement.append(self.Damage)

        # Calculate new total damage up until current tick
        for i in range(0, self.nTarget):
            self.DamagePerDummyIncrement[i].append(self.DamagePerDummy[i])

    def getResults(self, startTime, cycleTime):
        endTime = startTime + cycleTime

        if startTime > 0:
            self.DamageIncrement = self.DamageIncrement[startTime:endTime + 1]  # -1 because should start at 0

        self.Damage -= self.DamageIncrement[0]
        self.DamageIncrement = [x - self.DamageIncrement[0] for x in self.DamageIncrement]

        self.DamagePerTick = self.DamagePerTick[startTime:endTime]

        for i, dummyList in enumerate(self.DamagePerDummyIncrement):
            dummyList = dummyList[startTime:endTime + 1]
            self.DamagePerDummyIncrement[i] = [x - dummyList[0] for x in dummyList]



