from App.PythonRevolution import AttackCycle as Attack
import numpy as np


class Dummy:
    """
    The Dummy class. A dummy mimics a (stationary) monster.
    """

    def __init__(self, userInput):
        self.Damage = 0                 # The amount of damage done - puncture damage
        self.PunctureDamage = 0         # The amount of puncture damage done
        self.Stun = False               # When True, the dummy is in a stunned state
        self.StunTime = 0               # Time before a stun wears of
        self.Bind = False               # When True, the dummy is in a bind state
        self.BindTime = 0               # Time before a bind wears of
        self.DamageNames = []           # List of abilities which caused damage to the dummy in the current tick
        self.PHits = [0] * 50           # List of Pending Hits
        self.nPH = 0                    # Amount of Pending Hits
        self.Puncture = False           # True if a Puncture effect has been applied on the dummy
        self.nPuncture = 0              # Amount of puncture stacks on dummy
        self.PunctureDuration = 0       # Duration of the Puncture effect before the stack is reset
        self.LastStack = 0              # Stack number when the Salt the Wound ability has been used

        self.nTarget = int(userInput['nTargets'])             # Number of targets
        self.Movement = not userInput['movementStatus']       # True if the dummy can move
        self.StunBindImmune = userInput['stunbindStatus']     # True if the dummy is Stun and Bind immune

    def TimerCheck(self, logger):
        """
        Check the Bind and Stun status of the dummy.

        :param logger: the Logger object.
        """

        if self.Stun:
            self.StunTime -= 1

            if self.StunTime == 0:
                self.Stun = False

                if logger.DebugMode:
                    logger.write(19)

        if self.Bind:
            self.BindTime -= 1

            if self.BindTime == 0:
                self.Bind = False

                if logger.DebugMode:
                    logger.write(20)

        if self.Puncture:
            self.PunctureDuration -= 1

            if self.PunctureDuration == 0:
                self.Puncture = False
                self.nPuncture = 0

                if logger.DebugMode:
                    logger.write(21)
