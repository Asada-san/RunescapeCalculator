from App.PythonRevolution import AverageDamageCalculator as AVGCalc
import numpy as np


class Ability:
    """
    The Ability class. An ability contains all the properties of a RuneScape ability.
    """

    def __init__(self, abil_stats):
        """
        Sets the properties of each ability according to data read from an Excel sheet.
        :param abil_stats: Ability data read from an Excel sheet.
        """

        self.Name = abil_stats[0]                   # Name of the ability
        self.Revolution = abil_stats[1]             # True if the ability is activated by revolution
        self.Style = abil_stats[2]                  # Determines which combat style weapon can be used to fire the ability
        self.Level = abil_stats[3]                  # Level required to unlock the ability
        self.Type = abil_stats[4]                   # Basic, Threshold or Ultimate
        self.Member = abil_stats[5]                 # True if its a members only ability

        self.cdMax = abil_stats[6]      # Maximum cooldown time of the ability
        self.cdStatus = False           # True if the ability is on cooldown
        self.cdTime = 0                 # Current cooldown time of the ability

        self.Equipment = abil_stats[7]              # Determines if the weapon required is a 2h, duals or both

        self.nT = abil_stats[8]                     # Total amount of hits
        self.nS = abil_stats[9]                     # Total amount of standard hits
        self.nD = abil_stats[10]                    # Total amount of special hits (DoT effects)

        self.TrueWaitTime = abil_stats[11]          # The true waiting time before revolution fires a new ability
        self.EfficientWaitTime = abil_stats[12]     # Waiting time before the user manually fires the next abiltiy

        self.Delay = abil_stats[13]                 # True if the ability experiences a delay between firing and actually doing damage
        self.DelayTime = abil_stats[14]             # Normal delay after firing the ability

        self.Standard = abil_stats[15]              # True if the ability does a standard attack
        self.Channeled = abil_stats[16]             # True if the ability has a channel effect

        if self.Name not in {'Death\'s Swiftness', 'Sunshine'}:  # If Death's Swiftness or Sunshine do it manually
            self.Timings = list(map(float, abil_stats[17][1:-1].replace(',', '.').split('; ')))  # Hit times of the ability
        else:
            self.Timings = np.array([n * 3 for n in range(0, self.nD)])

        self.DamMax = np.array(list(map(float, abil_stats[18][1:-1].replace(',', '.').split('; '))))  # Maximum damage of the ability
        self.DamMin = np.array(list(map(float, abil_stats[19][1:-1].replace(',', '.').split('; '))))  # Minimum damage of the ability
        self.DamAvg = []    # Average damage of the ability
        self.Hits = []      # Array containing Standard or Channeled hits

        self.Bleed = abil_stats[20]         # True if the ability has a bleed effect
        self.BleedOnMove = abil_stats[21]   # Damage multiplier when target moves after bleed attack
        self.Puncture = abil_stats[22]      # True if the ability has a puncture effect

        self.DoTMax = np.array(list(map(float, abil_stats[23][1:-1].replace(',', '.').split('; '))))  # Maximum damage of the effect
        self.DoTMin = np.array(list(map(float, abil_stats[24][1:-1].replace(',', '.').split('; '))))  # Minimum damage of the effect
        self.DoTAvg = []    # Average damage of the effect
        self.DoTHits = []   # Array containing DoT effect hits

        self.StunBindDam = abil_stats[25]                   # True if the ability does extra damage when the dummy is stunned/bound
        self.StunBindDamMax = np.array([abil_stats[26]])    # Maximum damage
        self.StunBindDamMin = np.array([abil_stats[27]])    # Minimum damage
        self.HitsStunBind = []      # Array containing stun&bind hits

        self.Stun = abil_stats[28]          # True if the ability has a stun effect
        self.StunDur = abil_stats[29]       # Duration of the stun

        self.Bind = abil_stats[30]          # True if the ability has a bind effect
        self.BindDur = abil_stats[31]       # Duration of the bind

        self.Boost1 = abil_stats[32]        # True if the ability has a single ability boosting effect
        self.Boost1X = abil_stats[33]       # Boost multiplier
        self.Boost = abil_stats[34]         # True if the ability has a ability boosting effect
        self.BoostTime = abil_stats[35]     # Boost duration
        self.BoostX = abil_stats[36]        # Boost multiplier
        self.Special = abil_stats[37]       # True if the ability is a special cunt
        self.AoE = abil_stats[38]           # True if the ability does AoE damage

        ########## Doing it manually for AoE abilities ###############
        if self.Name == 'Quake':
            self.SideTargetMax = np.array([1.88])
            self.SideTargetMin = np.array([0.376])
            self.SideTarget = True
        elif self.Name == 'Greater Flurry':
            self.SideTargetMax = np.array([0.94] * 4)
            self.SideTargetMin = np.array([0.2] * 4)
            self.SideTarget = True
        else:
            self.SideTargetMax = np.array([0])
            self.SideTargetMin = np.array([0])
            self.SideTarget = False

        self.SideTargetAvg = []

    def ConstructHitObject(self, player, dummy, Do):
        """
        Constructs the Hit object depending on the type of hit.

        :param player: The Player object
        :param Do: The DoList object
        :return: Nothing
        """

        if player.PerkReflexes and self.Name == 'Anticipation':
            self.cdMax = 12

        if player.PerkPlantedFeet and self.Name in {'Sunshine', 'Death\'s Swiftness'}:
            self.Bleed = False
            self.BoostTime = 37.8
            return

        if self.Standard or self.Channeled:
            DamAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, Do)

            if self.Standard:
                for i in range(0, self.nS):
                    self.Hits.append(self.Hit(self, DamAvg, 1, 1, i, i))

                if self.StunBindDam:
                    StunBindDamAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, Do, 'StunBind', 0)

                    for i in range(0, self.nS):
                        self.HitsStunBind.append(self.Hit(self, StunBindDamAvg, 5, 1, i, i))

            else:
                for i in range(0, self.nS):
                    self.Hits.append(self.Hit(self, DamAvg, 2, 1, i, i))

            if self.SideTarget:
                SideTargetAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, Do, 'SideTarget', 0)

                for i in range(0, self.nS):
                    self.SideTargetAvg.append(self.Hit(self, SideTargetAvg, 6, 1, i, i))

        if self.Bleed:
            DoTAvg = AVGCalc.BleedDamAvgCalc(self, player, Do)

            for i in range(0, self.nD):
                self.DoTHits.append(self.Hit(self, DoTAvg, 3, 1, i, self.nS + i))

        if self.Puncture:
            DoTAvg = AVGCalc.PunctureDamAvgCalc(self, player, Do)

            for i in range(0, self.nD):
                self.DoTHits.append(self.Hit(self, DoTAvg, 4, 1, i, self.nS + i))

    class Hit:
        """
        The Hit object class used for defining a single hit of an ability.
        """

        def __init__(self, ability, Avg, Type, Target, Index, HitIndex):
            self.Damage = Avg[Index]                                    # Amount of damage for each hit
            self.Time = ability.Timings[HitIndex] + ability.DelayTime   # Timing of each hit
            self.Type = Type                                            # Type of effect (or standard) of each hit
            self.Target = Target                                        # Target on which each hit should be applied
            self.Index = HitIndex                                       # Index of the hit
            self.Name = ability.Name                                    # Name of the ability causing the hit


