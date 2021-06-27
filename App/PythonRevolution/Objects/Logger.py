import numpy as np
from App.PythonRevolution.Objects.Settings import Settings
import os


class Logger:
    """
    The Loop object. Used for finding repeating cycles in the simulation loop.
    """

    # __instance = None

    def __init__(self):
        # """ Virtually private constructor. """
        # if HTML.__instance is not None:
        #     raise Exception("This class is a singleton!")
        # else:
        #     HTML.__instance = self

        self.DebugMode = False

        self.SimulationTime = 0                 # Runtime of the while loop
        self.n = 0                              # Number of ticks in the while loop
        self.nCheck = 0                         # Number of ticks after a cycle has been found

        # Array consisting of boolean values, a value is true if an ability corresponding to the
        # same idx of the bar has been fired
        self.nFA = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.bool)

        self.Rotation = []                      # Array containing the cycle rotation
        self.CycleTime = 0                      # Cycle time in TICKS
        self.CycleDamage = 0                    # Damage done during 1 cycle time - puncture damage
        self.CyclePunctureDamage = 0            # Puncture damage done during 1 cycle time
        self.CycleFound = False                 # True if a cycle has been found
        self.Cycle1More = 0                     # Starts at t = CycleTime and when it runs out, runLoop is set to False
        self.ConditionList = []                 # List containing 4 condition to be satisfied
        self.Counter = []                       # List that contains loop.n every CycleChecker iteration
        self.Redundant = []                     # Array containing abilities which are not used in the cycle
        self.CycleLoopTime = 0                  # Current time in ticks when simulating the extra cycle
        self.CycleStart = 0                     # Starting time of the extra cycle
        self.nStall = 0                         # Number of consecutive stalls
        self.CycleConvergenceTime = 0           # The convergence time to the cycle

        # Dict with total damage contribution per ability
        self.AbilInfo = {'Boosted': {'damage': 0,
                                     'activations': 'NA',
                                     'shared%': 0}}

        self.Text = ''

        self.TextColor = {
            'important': 'red',  # Red color for important messages
            'attack': 'yellow',  # Yellow color for Ability activation and adrenaline
            'loop': '#4CAF50',  # Green-ish color for loop total damage/time information
            'damage': 'orange',  # Orange color for ability damage
            'normal': '#D0D0D0',  # White-ish color for less important info
            'initialisation': '#707070',  # Dark white color for user select options
            'start': '#FF00FB',  # Purple/Pink color for starting the revolution loop
            'status': '#00868F',  # Dark green-ish color for dummy status changes
            'cycle': '#00C7CD',  # Cyan color for cycle related stuff
        }

        self.TypeDict = {  # Dict for ability type
            1: 'standard',
            2: 'channel',
            3: 'bleed',
            4: 'puncture',
            5: 'stun&bind',
            6: 'side target',
            7: 'greater ricochet effect',
            8: 'greater chain effect'
        }

    # @staticmethod
    # def getInstance(opt=None):
    #     """ Static access method. """
    #     if HTML.__instance is None:
    #         HTML(opt)
    #     return HTML.__instance

    def write(self, x, var=None):

        if x == 0:
            string = \
                '----------------------------------------------------------------------------' \
                '----------------------------------------------------------------------------' \
                '----------------------------------------------------------------------------' \
                '----------------------------------------------------------------------------' \
                '--------------------------------------------------------<br><br>' \
                '<ul style="width: 850px;">'

        elif x == 1:
            string = \
                f'<li style="color: {self.TextColor["initialisation"]};">User select: Stationary {var[0]}</li>' \
                f'<li style="color: {self.TextColor["initialisation"]};">User select: Stun&Bind Immune {var[1]}</li>' \
                f'<li style="color: {self.TextColor["initialisation"]};">User select: Number of targets: {var[2]}</li>'

        elif x == 2:
            string = ''

            for key in var:
                string += f'<li style="color: {self.TextColor["initialisation"]};">User select: {key} --- {var[key]}</li>'

        # elif x == 3:
        #     string = ''
        #
        # elif x == 4:
        #     string = ''
        #
        # elif x == 5:
        #     string = ''
        #
        # elif x == 6:
        #     string = ''
        #
        # elif x == 7:
        #     string = ''
        #
        # elif x == 8:
        #     string = ''

        elif x == 9:
            string = f'<br>\n<li style="color: {self.TextColor["damage"]};">WARNING: {var[0]} should not be used with revolution</li>\n'

        elif x == 10:
            string = f'<br>\n<li style="color: {self.TextColor["damage"]};">WARNING: {var[0]} is not activated by revolution</li>\n'

        elif x == 11:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability bar consists of {var[0]} abilities and can be used with {var[1]}</li>'

        elif x == 12:
            string = \
                f'<br><li style="color: {self.TextColor["start"]}"> INITIALISATION COMPLETE: starting loop<br><br>' \
                f'<li style="color: {self.TextColor["loop"]}; white-space: pre-wrap;">' \
                f'Total damage: 0' \
                f'<span style="float: right; margin-right: 18px;">Time: 0</span></li><br>'

        elif x == 13:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability Calculation: Avg hit of {var[0]} to {var[1]}, pForced: {var[2]}, pNat: {var[3]}</li>'

        elif x == 14:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability change: Extended {var} by 3 hits</li>'

        elif x == 15:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability change: Extended {var} by 2 hits</li>'

        elif x == 16:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability Calculation: Avg hit of {var[0]} to {var[1]}x {var[2]}</li>'

        elif x == 17:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Ability Calculation: Avg hit of {var[0]} to {var[1]}</li>'

        elif x == 18:
            string = f'<li style="color: {self.TextColor["normal"]};">Global cooldown ended</li>'

        elif x == 19:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy no longer stunned</li>'

        elif x == 20:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy no longer bound</li>'

        elif x == 21:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy puncture stack reset to 0</li>'

        elif x == 22:
            string = f'<li style="color: {self.TextColor["normal"]};">{var} no longer on cd</li>'

        elif x == 23:
            string = f'<li style="color: {self.TextColor["normal"]};">Player adrenaline gain buff has worn out</li>'

        elif x == 24:
            string = f'<li style="color: {self.TextColor["normal"]};">Player is no longer performing a channeled ability</li>'

        elif x == 25:
            string = f'<li style="color: {self.TextColor["normal"]};">Player damage boost has been reset</li>'

        elif x == 26:
            string = f'<li style="color: {self.TextColor["normal"]};">Player Greater Chain effect has worn off</li>'

        elif x == 27:
            string = f'<li style="color: {self.TextColor["attack"]};">{var[0]} hit boosted {var[1]}x</li>'

        elif x == 28:
            string = f'<li style="color: {self.TextColor["damage"]};">{var[0]} ({self.TypeDict[var[1]]}) damage applied: {var[2]}</li>'

        elif x == 29:
            string = f'<li style="color: {self.TextColor["damage"]};">{var[0]} ({self.TypeDict[var[1]]}) damage applied on target #{var[2]}: {var[3]}</li>'

        elif x == 30:
            string = f'<li style="color: {self.TextColor["attack"]};">Adrenaline increased by: {var[0]} to: {var[1]}</li>'

        elif x == 31:
            string = f'<li style="color: {self.TextColor["attack"]};">{var} activated (normal)'

        elif x == 32:
            string = f'<li style="color: {self.TextColor["important"]};">{var} activated (stun&bind)'

        elif x == 33:
            string = f'<li style="color: {self.TextColor["attack"]};">Adrenaline: {var}</li>'

        elif x == 34:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy puncture stack: {var}</li>'

        elif x == 35:
            string = f'<li style="color: {self.TextColor["cycle"]};">CYCLE FOUND, EXTENDING RUN BY 1x CYCLETIME: {var}s</li>'

        elif x == 36:
            string = f'<li style="color: {self.TextColor["normal"]};">Attack status: {var} ready</li>'

        elif x == 37:
            string = f'<li style="color: {self.TextColor["initialisation"]};">Not enough Adrenaline for {var}</li>'

        elif x == 38:
            string = f'<li style="color: {self.TextColor["important"]};">No ability available, skip attack</li>'

        elif x == 39:
            string = f'<li style="color: {self.TextColor["important"]};">Player is using a channeled ability</li>'

        elif x == 40:
            string = f'<li style="color: {self.TextColor["important"]};">GLOBAL COOLDOWN</li>'

        elif x == 41:
            string = \
                f'<li style="color: {self.TextColor["normal"]};">{var} went on cooldown</li>' \
                f'<li style="color: {self.TextColor["normal"]};">GCD activated</li>'

        elif x == 42:
            string = f'<li style="color: {self.TextColor["normal"]};">{var} went on cooldown</li>'

        elif x == 43:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy is Stunned for {var}s</li>'

        elif x == 44:
            string = f'<li style="color: {self.TextColor["status"]};">Dummy is Bound for {var}s</li>'

        elif x == 45:
            string = f'<li style="color: {self.TextColor["attack"]};">Needle Strike boost active!</li>'

        elif x == 46:
            string = \
                f'<br>\n<li style="color: {self.TextColor["loop"]}; white-space: pre-wrap;">' \
                f'Total damage: {var[0]}' \
                f'<span style="float: right; margin-right: 18px;">Time: {var[1]}</span></li><br>'

        elif x == 47:
            string = \
                f'<br>\n<li style="color: {self.TextColor["cycle"]}; white-space: pre-wrap;">' \
                f'Cycle damage: {var[0]}' \
                f'<span style="float: right; margin-right: 18px;">Cycle Time: {var[1]}</span></li><br>'

        elif x == 48:
            string = f'<li style="color: {self.TextColor["cycle"]};">VERIFICATION LOOP COMPLETED: RETURN RESULTS</li>'

        # elif x == 49:
        #     string =
        #
        # elif x == 50:
        #     string =
        #
        # elif x == 51:
        #     string =
        #
        # elif x == 52:
        #     string =

        else:
            string = f'NO CORRESPONDING STRING FOUND!'

        self.Text += string
