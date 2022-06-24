import numpy as np
from App.PythonRevolution.Objects.Settings import Settings
import os
from copy import deepcopy


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

        self.n = 0                              # Number of ticks in the while loop (iterations)
        self.nCheck = 0                         # Number of ticks after a cycle has been found (iterations)
        self.Rotation = []                      # Array containing ability names in order of activation
        self.RotationTick = []                  # Array containing tick number in which the abilities in logger.Rotation have been activated
        self.CycleTime = 0                      # Cycle time in TICKS
        self.CycleFound = False                 # True if a cycle has been found
        self.ConditionList = []                 # List containing 4 condition to be satisfied
        self.Counter = []                       # List that contains loop.n every CycleChecker iteration
        self.Redundant = []                     # Array containing abilities which are not used in the cycle
        self.CycleLoopTime = 0                  # Current time in ticks when simulating the extra cycle
        self.CycleStart = 0                     # Starting time of the extra cycle
        self.nStall = 0                         # Number of consecutive stalls
        self.CycleConvergenceTime = 0           # The convergence time to the cycle
        self.Cooldowns = []

        # Dict with total damage contribution per ability
        self.AbilInfo = {}

        self.CycleAbilityDamagePerTick = {}

        self.Text = ''

        self.TextColor = {
            'important': 'red',  # Red color for important messages
            'attack': 'yellow',  # Yellow color for Ability activation and adrenaline
            'charge': '#87B0E6',  # Turquoise for abilities/effects that are charging (Like Jas effect)
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
            10: 'special'
        }

    def initAbility(self, name):
        self.AbilInfo.update({name: {'damage': 0,
                                     'activations': 0,
                                     'shared%': 0}})

        self.CycleAbilityDamagePerTick.update({name: {'damage': [0],
                                                      'activations': 0}})

    def updateTickInfo(self):
        for key, value in self.AbilInfo.items():
            self.CycleAbilityDamagePerTick[key]['damage'].append(self.AbilInfo[key]['damage'])

    def getResults(self, startTime, cycleTime):
        endTime = startTime + cycleTime

        i = 0
        k = len(self.RotationTick)

        while self.RotationTick[i] < startTime:
            if i == k - 1:
                break
            else:
                i += 1

        self.Rotation = self.Rotation[i:]

        for ability in self.AbilInfo.keys():
            self.CycleAbilityDamagePerTick[ability]['damage'] = self.CycleAbilityDamagePerTick[ability]['damage'][startTime:endTime + 1]
            self.CycleAbilityDamagePerTick[ability]['damage'] = [x - self.CycleAbilityDamagePerTick[ability]['damage'][0] for x in self.CycleAbilityDamagePerTick[ability]['damage']]
            self.CycleAbilityDamagePerTick[ability]['activations'] = self.Rotation.count(ability)

            self.AbilInfo[ability]['damage'] = self.CycleAbilityDamagePerTick[ability]['damage'][-1]

            self.AbilInfo[ability]['activations'] = max(self.Rotation.count(ability), self.Rotation.count('<span style="color: #B65FCF">' + ability + '</span>'))

    def check_stall(self):
        if len(self.Rotation) != 0 and 'STALL' in self.Rotation[-1]:
            self.nStall += 1
            self.Rotation[-1] = f'<span style="color: {self.TextColor["cycle"]}">STALL {self.nStall}x</span>'
            self.RotationTick[-1] = self.n
        else:
            self.nStall = 1
            self.Rotation.extend([f'<span style="color: {self.TextColor["cycle"]}">STALL {self.nStall}x</span>'])
            self.RotationTick.append(self.n)

    def addRotation(self, name, special=False):
        self.AbilInfo[name]['activations'] += 1

        if special:
            name = '<span style="color: #B65FCF">' + name + '</span>'
            self.RotationTick.append(self.n + 1)
        else:
            self.RotationTick.append(self.n)

        self.Rotation.append(name)
        # self.RotationTick.append(self.n)
