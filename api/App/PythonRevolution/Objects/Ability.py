from App.PythonRevolution import AverageDamageCalculator as AVGCalc
import numpy as np
from copy import deepcopy


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

        self.cdMax = abil_stats[6]                  # Maximum cooldown time of the ability
        self.cdStatus = False                       # True if the ability is on cooldown
        self.cdTime = 0                             # Current cooldown time of the ability

        self.Equipment = abil_stats[7]              # Determines if the weapon required is a 2h, duals or both

        self.nT = abil_stats[8]                     # Total amount of hits
        self.nS = abil_stats[9]                     # Total amount of standard hits
        self.nD = abil_stats[10]                    # Total amount of special hits (DoT effects)

        self.TrueWaitTime = abil_stats[11]          # The true waiting time before revolution fires a new ability
        self.EfficientWaitTime = abil_stats[12]     # Waiting time before the user manually fires the next abilitiy

        self.DelayTime = abil_stats[13]             # Normal delay after firing the ability

        self.Standard = abil_stats[14]              # True if the ability does a standard attack
        self.Channeled = abil_stats[15]             # True if the ability has a channel effect

        self.Timings = np.fromstring(abil_stats[16].strip('[]'), dtype=float, sep='; ')         # Hit times of the ability

        self.DamMax = np.fromstring(abil_stats[17].strip('[]'), dtype=float, sep='; ')          # Maximum damage of the ability
        self.DamMin = np.fromstring(abil_stats[18].strip('[]'), dtype=float, sep='; ')          # Minimum damage of the ability
        self.Hits = []                              # Array containing Standard or Channeled hits

        self.Bleed = abil_stats[19]                 # True if the ability has a bleed effect
        self.BleedOnMove = abil_stats[20]           # Damage multiplier when target moves after bleed attack
        self.Puncture = abil_stats[21]              # True if the ability has a puncture effect

        self.DoTMax = np.fromstring(abil_stats[22].strip('[]'), dtype=float, sep='; ')          # Maximum damage of the effect
        self.DoTMin = np.fromstring(abil_stats[23].strip('[]'), dtype=float, sep='; ')          # Minimum damage of the effect
        self.DoTHits = []                           # Array containing DoT effect hits

        self.StunBindDam = abil_stats[24]           # True if the ability does extra damage when the dummy is stunned/bound
        self.StunBindDamMax = np.fromstring(abil_stats[25].strip('[]'), dtype=float, sep='; ')  # Maximum damage of the effect
        self.StunBindDamMin = np.fromstring(abil_stats[26].strip('[]'), dtype=float, sep='; ')  # Maximum damage of the effect
        self.HitsStunBind = []                      # Array containing stun&bind hits

        self.Stun = abil_stats[27]                  # True if the ability has a stun effect
        self.StunDur = abil_stats[28]               # Duration of the stun

        self.Bind = abil_stats[29]                  # True if the ability has a bind effect
        self.BindDur = abil_stats[30]               # Duration of the bind

        self.SideTarget = abil_stats[31]            # True if the ability does different damage to side targets
        self.SideTargetMax = np.fromstring(abil_stats[32].strip('[]'), dtype=float, sep='; ')   # Maximum damage of the effect
        self.SideTargetMin = np.fromstring(abil_stats[33].strip('[]'), dtype=float, sep='; ')   # Maximum damage of the effect
        self.HitsSideTarget = []                    # Array containing side target hits

        self.Boost1 = abil_stats[34]                # True if the ability has a single ability boosting effect
        self.Boost1X = abil_stats[35]               # Boost multiplier
        self.Boost = abil_stats[36]                 # True if the ability has a ability boosting effect
        self.BoostTime = abil_stats[37]             # Boost duration
        self.BoostX = abil_stats[38]                # Boost multiplier
        self.Special = abil_stats[39]               # True if the ability is a special cunt

        self.AoE = abil_stats[40]                   # True if the ability does AoE damage
        self.MaxTargets = abil_stats[41]            # Maximum amount of targets damaged by AoE abilities

        self.FinalHit = []
        self.FinalTotal = 0
        self.GreaterChainTargets = []

    def AbilityUpgrades(self, player, logger):
        """
        Further initialises the Ability objects and applies upgrades depending on the
        user input.

        :param player: The Player object
        :param logger: The Logger object
        :return: Nothing
        """

        # Manually calculate the Max and Min of Shadow Tendrils
        if self.Name in {'Shadow Tendrils'}:
            self.DamMax[0] = 0.1 * self.DamMax[0] * 2 + .18 * self.DamMax[0] * 3 + .216 * self.DamMax[0] * 4 + .504 * self.DamMax[0] * 5
            self.DamMin[0] = 0.1 * self.DamMin[0] * 2 + .18 * self.DamMin[0] * 3 + .216 * self.DamMin[0] * 4 + .504 * self.DamMin[0] * 5

        # Remove last hit from concentrated blast if the user is not afk
        if not player.Afk and self.Name in {'Lesser Concentrated Blast', 'Concentrated Blast'}:
            self.nT = 2
            self.nS = 2

            self.DamMax = self.DamMax[:2]
            self.DamMin = self.DamMin[:2]

        # Increase of damageable targets due to Caroming Perk
        if player.PerkCaroming and self.Name in {'Chain', 'Greater Chain', 'Ricochet', 'Greater Ricochet'}:
            self.MaxTargets += player.Cr

        # Stun ability changes due to perks
        if player.PerkFlanking:
            if self.Name in {'Backhand', 'Impact', 'Binding Shot'}:
                self.Stun = False  # Abilities above loose their stun effect

                for i in range(0, self.nS):  # Increase min by 8% per rank, max by 40% per rank
                    self.DamMax[i] += 0.4 * player.Fr
                    self.DamMin[i] += 0.08 * player.Fr

            if self.Name in {'Forceful Backhand', 'Deep Impact', 'Tight Bindings'}:
                self.Stun = False  # Abilities above lose their stun effect

                for i in range(0, self.nS):  # Increase min by 6% per rank, max by 30% per rank
                    self.DamMax[i] += 0.3 * player.Fr
                    self.DamMin[i] += 0.06 * player.Fr

        if self.Name == 'Debilitate' and player.PerkShieldBashing:
            self.DamMax[0] += 0.15 * player.SBr
            self.DamMin[0] += 0.15 * player.SBr

        # Bleed ability changes due to perks and items
        nExtend = 0

        if player.PerkLunging and self.Name in {'Dismember', 'Combust', 'Fragmentation Shot'}:
            # Bleeds of Combust and Fragmentation Shot are multiplied by 1.5 upon walking instead of 2
            if self.Name != 'Dismember':
                self.BleedOnMove = 1.5

            self.DoTMax += 0.2 * player.Lr / self.nD  # Increase max hit by 0.2 for every rank

        if player.Cape == 'StrengthCape' and self.Name == 'Dismember':
            nExtend += 3  # Add 3 hits to the Dismember ability

            self.DoTMax = np.append(self.DoTMax, self.DoTMax[-4: -1])
            self.DoTMin = np.append(self.DoTMin, self.DoTMin[-4: -1])

            if logger.DebugMode:
                logger.write(14, self.Name)

        if player.Cape == 'IgneousKal-Ket' and self.Name == 'Overpower':
            self.DamMax = np.append(self.DamMax, self.DamMax)
            self.DamMin = np.append(self.DamMin, self.DamMin)
            self.Timings = np.append(self.Timings, self.Timings)
            self.nS += 1
            self.nT += 1

            if logger.DebugMode:
                logger.write(51, self.Name)

        if player.Cape == 'IgneousKal-Xil' and self.Name == 'Deadshot':
            self.DamMax[0] = 2.1
            self.DamMin[0] = 0.42

            self.DoTMax = np.full(7, 0.7)
            self.DoTMin = np.full(7, 0.7)

            nExtend += 2

            if logger.DebugMode:
                logger.write(52, self.Name)

        if player.Cape == 'IgneousKal-Mej' and self.Name == 'Omnipower':
            self.DamMax = np.full(4, 1.8)
            self.DamMin = np.full(4, 0.9)

            self.Timings = np.append(self.Timings, [self.Timings + 1] * 3)
            
            self.nS = 4
            self.nT = 4

            if logger.DebugMode:
                logger.write(53, self.Name)

        if player.MSoA and self.Name in {'Dismember', 'Blood Tendrils', 'Slaughter'}:
            nExtend += 2  # Add 2 hits to the Dismember, Blood Tendrils and Slaughter abilities

            self.DoTMax = np.append(self.DoTMax, self.DoTMax[-3: -1])
            self.DoTMin = np.append(self.DoTMin, self.DoTMin[-3: -1])

            if logger.DebugMode:
                logger.write(15, self.Name)

        if nExtend > 0:
            self.nD += nExtend
            self.nT += nExtend

            # Extend the Timings array
            for i in range(0, nExtend):
                self.Timings = np.append(self.Timings, [self.Timings[-1] + 2])

        # Other ability changes
        if player.PerkReflexes and self.Name == 'Anticipation':
            self.cdMax = 12

        if player.PerkPlantedFeet and self.Name in {'Sunshine', 'Death\'s Swiftness'}:
            self.Bleed = False
            self.BoostTime = 63
            return

        # Creating Hit objects which will be attached to the ability
        AvgDam = []
        Type = 0

        if self.nS > 0:
            if self.Style == 'Special':
                DamAvg = AVGCalc.SpecialDamAvgCalc(self, player, logger)
                Type = 10
                self.Hits.extend([self.Hit(self, DamAvg, Type, i, i) for i in range(0, self.nS)])
            else:
                DamAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, logger)

                if self.Standard:
                    Type = 1
                elif self.Channeled:
                    Type = 2

                self.Hits.extend([self.Hit(self, DamAvg, Type, i, i) for i in range(0, self.nS)])

        if self.StunBindDam:
            StunBindDamAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, logger, 'StunBind')

            self.HitsStunBind.extend([self.Hit(self, StunBindDamAvg, 5, i, i) for i in range(0, self.nS)])

        if self.SideTarget:
            SideTargetAvg = AVGCalc.StandardChannelDamAvgCalc(self, player, logger, 'SideTarget')

            self.HitsSideTarget.extend([self.Hit(self, SideTargetAvg, 6, i, i) for i in range(0, self.nS)])

        if self.nD > 0:
            if self.Bleed:
                AvgDam = AVGCalc.BleedDamAvgCalc(self, player, logger)
                Type = 3
            elif self.Puncture:
                AvgDam = AVGCalc.PunctureDamAvgCalc(self, player, logger)
                Type = 4

            self.DoTHits.extend([self.Hit(self, AvgDam, Type, i, self.nS + i) for i in range(0, self.nD)])

        self.FinalHit = np.append(deepcopy(self.Hits), deepcopy(self.DoTHits))
        self.FinalTotal = len(self.FinalHit)

    def AoECheck(self, dummy, player):
        """
        Duplicates hits if the ability does AoE damage and there are more than 1 target.

        :param player: The Player object.
        :param dummy: The Dummy object.
        """

        if dummy.nTarget > self.MaxTargets:
            nDT = int(self.MaxTargets)
        else:
            nDT = dummy.nTarget

        if self.Name in {'Quake', 'Greater Flurry'}:  # DamMax = 0.94, DamMin = 0.2, DamAvg = 0.57 for ALL! targets
            for i in range(0, nDT - 1):
                self.FinalHit = np.append(self.FinalHit, deepcopy(self.HitsSideTarget))

                for j in range(0, self.nT):
                    self.FinalHit[self.nT*(i + 1) + j].Target = i + 2

        elif self.Name == 'Hurricane':  # First hit on main target equals the hit for all other targets
            for i in range(0, nDT - 1):
                self.FinalHit = np.append(self.FinalHit, deepcopy(self.Hits[0]))
                self.FinalHit[-1].Target = i + 2

        elif self.Name in {'Corruption Blast', 'Corruption Shot'}:  # First hit main target only, than spreading to all other targets
            for i in range(0, nDT - 1):
                self.FinalHit = np.append(self.FinalHit, deepcopy(self.DoTHits[1:]))

                for j in range(0, self.nD - 1):
                    self.FinalHit[self.nD + (self.nD - 1) * i + j].Target = i + 2

        elif self.Name in {'Chain', 'Greater Chain', 'Ricochet', 'Greater Ricochet'}:  # Ricochet and Chain only hit up to 3 targets (except when perk)
            for i in range(0, nDT - 1):
                self.FinalHit = np.append(self.FinalHit, deepcopy(self.Hits))

                for j in range(0, self.nT):
                    self.FinalHit[self.nT*(i + 1) + j].Target = i + 2
                    self.FinalHit[self.nT*(i + 1) + j].Time += 1

            if self.Name == 'Greater Chain':
                self.GreaterChainTargets = list(range(2, nDT + 1))

            # Apply Hits of greater Ricochet for which no targets are available back to target 1
            # but reduced.
            if self.Name == 'Greater Ricochet' and dummy.nTarget < self.MaxTargets:
                HitNumber = dummy.nTarget + 1

                for i in range(0, int(self.MaxTargets - dummy.nTarget)):
                    self.FinalHit = np.append(self.FinalHit, deepcopy(self.Hits))
                    if HitNumber <= 3:
                        self.FinalHit[HitNumber - 1].DamMax *= 0.5
                        self.FinalHit[HitNumber - 1].DamMin *= 0.5
                        self.FinalHit[HitNumber - 1].Damage *= 0.5
                    else:
                        self.FinalHit[HitNumber - 1].DamMax *= 0.15
                        self.FinalHit[HitNumber - 1].DamMin *= 0.25
                        self.FinalHit[HitNumber - 1].Damage /= 6

                    HitNumber += 1
        else:
            for i in range(0, nDT - 1):
                if self.Name != 'Magma Tempest':
                    self.FinalHit = np.append(self.FinalHit, deepcopy(self.Hits))
                else:
                    self.FinalHit = np.append(self.FinalHit, deepcopy(self.DoTHits))

                for j in range(0, self.nT):
                    self.FinalHit[self.nT * (i + 1) + j].Target = i + 2

        self.FinalTotal = len(self.FinalHit)

    class Hit:
        """
        The Hit object class used for defining a single hit of an ability.
        """

        def __init__(self, Abil, Avg, Type, Index, HitIndex):
            if Type in {1, 2}:
                self.DamMin = np.array([Abil.DamMin[HitIndex]])
                self.DamMax = np.array([Abil.DamMax[HitIndex]])
            elif Type in {3, 4}:
                self.DoTMin = np.array([Abil.DoTMin[HitIndex-Abil.nS]])
                self.DoTMax = np.array([Abil.DoTMax[HitIndex-Abil.nS]])
            elif Type in {5}:
                self.DamMin = np.array([Abil.StunBindDamMin[HitIndex]])
                self.DamMax = np.array([Abil.StunBindDamMax[HitIndex]])
            elif Type in {6}:
                self.DamMin = np.array([Abil.SideTargetMin[HitIndex]])
                self.DamMax = np.array([Abil.SideTargetMax[HitIndex]])

            self.BleedOnMove = Abil.BleedOnMove

            self.Damage = Avg[Index]                                # Amount of damage for each hit
            self.Time = Abil.Timings[HitIndex] + Abil.DelayTime     # Timing of each hit
            self.Type = Type                                        # Type of effect (or standard) of each hit
            self.Target = 1                                         # Target on which each hit should be applied, initialised as #1
            self.Index = HitIndex                                   # Index of the hit
            self.Name = Abil.Name                                   # Name of the ability causing the hit



