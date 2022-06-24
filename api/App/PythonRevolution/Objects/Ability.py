import numpy as np
import math
from copy import deepcopy, copy


class Ability():
    """
    The Ability class. An ability contains all the properties of a RuneScape ability.
    """

    def __init__(self, data):
        """
        Sets the properties of each ability according to data read from an Excel sheet.
        :param abil_stats: Ability data read from an Excel sheet.
        """

        self.Parent = None

        self.Name = data['Name']                   # Name of the ability
        self.Revolution = data['Revolution']             # True if the ability is activated by revolution
        self.Style = data['Style']                  # Determines which combat style weapon can be used to fire the ability
        self.Level = data['Level']                  # Level required to unlock the ability
        self.Type = data['Type']                   # Basic, Threshold or Ultimate
        self.Member = data['Member']                 # True if its a members only ability

        self.cdMax = data['Cooldown']                  # Maximum cooldown time of the ability
        self.cdTime = 0                            # Current cooldown time of the ability

        self.Equipment = data['Equipment']              # Determines if the weapon required is a 2h, duals or both

        self.nT = data['TotalHits']                     # Total amount of hits
        self.nS = data['StandardHits']                     # Total amount of standard hits
        self.nD = data['DoTHits']                    # Total amount of special hits (DoT effects)

        self.TrueWaitTime = data['TrueWaitTime']          # The true waiting time before revolution fires a new ability
        self.EfficientWaitTime = data['EfficientWaitTime']     # Waiting time before the user manually fires the next abilitiy

        self.DelayTime = data['DelayTime']             # Normal delay after firing the ability

        self.Standard = data['Standard']              # True if the ability does a standard attack
        self.Channeled = data['Channeled']             # True if the ability has a channel effect

        self.Timings = np.fromstring(data['Timings'].strip('[]'), dtype=float, sep='; ')         # Hit times of the ability

        self.DamMax = np.fromstring(data['DamMax'].strip('[]'), dtype=float, sep='; ')          # Maximum damage of the ability
        self.DamMin = np.fromstring(data['DamMin'].strip('[]'), dtype=float, sep='; ')          # Minimum damage of the ability

        self.pForcedCrit = np.fromstring(data['CriticalHitBuff'].strip('[]'), dtype=float, sep='; ')  # Minimum damage of the ability

        self.Bleed = data['Bleed']                 # True if the ability has a bleed effect
        self.BleedOnMove = data['DoTOnMove']           # Damage multiplier when target moves after bleed attack
        self.Puncture = data['Puncture']              # True if the ability has a puncture effect

        self.StunBindDam = data['StunBindDam']           # True if the ability does extra damage when the dummy is stunned/bound
        self.SideTarget = data['SideTargetDam']  # True if the ability does different damage to side targets
        self.SpecialDamMax = np.fromstring(data['SpecialDamMax'].strip('[]'), dtype=float, sep='; ')  # Maximum damage of the effect
        self.SpecialDamMin = np.fromstring(data['SpecialDamMin'].strip('[]'), dtype=float, sep='; ')  # Maximum damage of the effect
        self.HitsStunBind = []                      # Array containing stun&bind hits
        self.HitsSideTarget = []                    # Array containing side target hits

        self.StunDuration = data['StunDuration']          # Duration of a possible Stun effect
        self.BindDuration = data['BindDuration']          # Duration of a possible Bind effect

        self.Boost1 = data['Boost1']                # True if the ability has a single ability boosting effect
        self.Boost = data['Boost']                 # True if the ability has a ability boosting effect
        self.BoostX = data['BoostX']                # Boost multiplier

        self.EffectDuration = data['EffectDuration']        # Duration of the effect of the ability

        self.AoE = data['AoE']                   # True if the ability does AoE damage
        self.MaxTargets = data['MaxTargets']            # Maximum amount of targets damaged by AoE abilities

        if 0 < data['ActivationChance'] < 1:                  # Hits needed for activation
            self.HitsToActivate = int(math.ceil(math.log(0.5)/math.log(1 - data['ActivationChance'])))
        else:
            self.HitsToActivate = 1

        self.Hits = []                              # Array containing all hits which will be applied to the dummy
        self.nHits = 0                              # Total amount of hits of the ability including multi targets
        self.GreaterChainTargets = []               # Dummy targets affected by the Greater Chain effect

        if self.Type == 'Basic':
            self.AdrenalineGain = 8
        elif self.Type == 'Threshold':
            self.AdrenalineGain = -15
        elif self.Type == 'Ultimate':
            self.AdrenalineGain = -100

        self.SharedCooldownAbilities = []

    def putOnCooldown(self):
        self.cdTime = self.cdMax

        for ability in self.SharedCooldownAbilities:
            ability.cdTime = ability.cdMax

    def AbilityUpgrades(self):
        """
        Further initialises the Ability objects and applies upgrades depending on the
        user input.

        :return: Nothing
        """

        if self.Parent.Biting:
            self.pForcedCrit += self.Parent.Biting * 0.02 * self.Parent.Level20Gear

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Biting): Increased pForcedCrit to {self.pForcedCrit}</li>'

        if self.Parent.Pocket.Name == 'Erethdor\'s Grimoire':
            self.pForcedCrit += 0.12

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Erethdor\'s Grimoire): Increased pForcedCrit to {self.pForcedCrit}</li>'

        if self.Parent.Ring.Name == 'Reaver\'s ring' and self.Equipment != 'None':
            self.pForcedCrit += 0.05

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Reaver\'s ring): Increased pForcedCrit to {self.pForcedCrit}</li>'

        elif self.Parent.Ring.Name == 'Stalker\'s ring' and \
                self.Style not in {'Strength', 'Attack', 'Magic'} and \
                self.Equipment in {'2h', 'any'}:
            self.pForcedCrit += 0.03

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Stalker\'s ring): Increased pForcedCrit to {self.pForcedCrit}</li>'

        elif self.Parent.Ring.Name == 'Channeler\'s ring' and self.Channeled and self.Style == 'Magic':
            for i in range(self.pForcedCrit.size):
                self.pForcedCrit[i] += (i + 1) * 0.04

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Channeler\'s ring): Increased pForcedCrit to {self.pForcedCrit}</li>'

        # Check for Deathspore arrows effect
        if all([self.Parent.Ammo.Name == 'Deathspore arrows', self.Style == 'Ranged',
                self.Equipment in {'2h', 'any'}]):
            self.pForcedCrit += 0.03

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Deathspore arrows): Increased pForcedCrit to {self.pForcedCrit}</li>'

        if self.Parent.FuryOfTheSmall and self.Type == 'Basic':
            self.AdrenalineGain += 1

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Fury of the Small): Increased basic adrenaline gain to {self.AdrenalineGain}</li>'

        # Manually calculate the Max and Min of Shadow Tendrils
        if self.Name in {'Shadow Tendrils'}:
            self.DamMax[0] = 0.1 * self.DamMax[0] * 2 + .18 * self.DamMax[0] * 3 + .216 * self.DamMax[0] * 4 + .504 * self.DamMax[0] * 5
            self.DamMin[0] = 0.1 * self.DamMin[0] * 2 + .18 * self.DamMin[0] * 3 + .216 * self.DamMin[0] * 4 + .504 * self.DamMin[0] * 5

        # Remove last hit from concentrated blast if the user is not afk
        if not self.Parent.Afk and self.Name in {'Lesser Concentrated Blast', 'Concentrated Blast'}:
            self.nT = 2
            self.nS = 2

            self.DamMax = self.DamMax[:2]
            self.DamMin = self.DamMin[:2]

            self.pForcedCrit = self.pForcedCrit[:2]

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Efficient setting): Decreased total hit of {self.Name} by 1</li>'

        # Increase of damageable targets due to Caroming Perk
        if self.Parent.Caroming and self.Name in {'Chain', 'Greater Chain', 'Ricochet', 'Greater Ricochet'}:
            self.MaxTargets += self.Parent.Caroming

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Caroming): Increased max targets to {self.MaxTargets}</li>'

        # Stun ability changes due to perks
        if self.Parent.Flanking:
            if self.Name in {'Backhand', 'Impact', 'Binding Shot'}:
                self.StunDuration = 0  # Abilities above loose their stun effect

                for i in range(0, self.nS):  # Increase min by 8% per rank, max by 40% per rank
                    self.DamMax[i] += 0.4 * self.Parent.Flanking
                    self.DamMin[i] += 0.08 * self.Parent.Flanking

            if self.Name in {'Forceful Backhand', 'Deep Impact', 'Tight Bindings'}:
                self.StunDuration = 0  # Abilities above lose their stun effect

                for i in range(0, self.nS):  # Increase min by 6% per rank, max by 30% per rank
                    self.DamMax[i] += 0.3 * self.Parent.Flanking
                    self.DamMin[i] += 0.06 * self.Parent.Flanking

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Flanking): Removed stun effect and increased Max and Min to {self.DamMax} and {self.DamMin} respectively</li>'

        if self.Name == 'Debilitate' and self.Parent.ShieldBashing:
            self.DamMax[0] += 0.15 * self.Parent.ShieldBashing
            self.DamMin[0] += 0.15 * self.Parent.ShieldBashing

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Shield Bashing): Increased Max and Min to {self.DamMax} and {self.DamMin} respectively</li>'

        # Bleed ability changes due to perks and items
        nExtend = 0

        if self.Parent.Lunging and self.Name in {'Dismember', 'Combust', 'Fragmentation Shot'}:
            # Bleeds of Combust and Fragmentation Shot are multiplied by 1.5 upon walking instead of 2
            if self.Name != 'Dismember':
                self.BleedOnMove = 1.5

            self.DamMax += 0.2 * self.Parent.Lunging / self.nD  # Increase max hit by 0.2 for every rank

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Lunging): Set BleedOnMove to {self.BleedOnMove} and increased Max to {self.DamMax}</li>'

        if (self.Parent.Cape.Name == 'Strength cape' or self.Parent.AnachroniaCapeStand) and self.Name == 'Dismember':
            nExtend += 3  # Add 3 hits to the Dismember ability

            self.DamMax = np.append(self.DamMax, self.DamMax[-4: -1])
            self.DamMin = np.append(self.DamMin, self.DamMin[-4: -1])

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Strength Cape): Extended Max by 3 hits</li>'

        if self.Parent.Cape.Name in {'Igneous Kal-Ket', 'Igneous Kal-Zuk'} and self.Name == 'Overpower':
            self.DamMax = np.append(self.DamMax, self.DamMax)
            self.DamMin = np.append(self.DamMin, self.DamMin)
            self.Timings = np.append(self.Timings, self.Timings)
            self.nS += 1
            self.nT += 1

            self.pForcedCrit = np.append(self.pForcedCrit, [self.pForcedCrit[-1]])

            self.AdrenalineGain = -60

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Zuk Cape): Increased hits to {self.nT} and AdrenalineGain to {self.AdrenalineGain}</li>'

        if self.Parent.Cape.Name in {'Igneous Kal-Xil', 'Igneous Kal-Zuk'} and self.Name == 'Deadshot':
            self.DamMax[0] = 2.1
            self.DamMin[0] = 0.42

            self.DamMax = np.append(self.DamMax, np.full(7, 0.7))
            self.DamMin = np.append(self.DamMin, np.full(7, 0.7))

            self.pForcedCrit = np.append(self.pForcedCrit, np.full(2, 0))

            self.AdrenalineGain = -60

            nExtend += 2

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Zuk Cape): Increased Max and Min to {self.DamMax} and {self.DamMin} respectively and AdrenalineGain to {self.AdrenalineGain}</li>'

        if self.Parent.Cape.Name in {'Igneous Kal-Mej', 'Igneous Kal-Zuk'} and self.Name == 'Omnipower':
            self.DamMax = np.full(4, 1.8)
            self.DamMin = np.full(4, 0.9)

            self.Timings = np.append(self.Timings, [self.Timings + 1] * 3)

            self.pForcedCrit = np.append(self.pForcedCrit, [self.pForcedCrit] * 3)
            
            self.nS = 4
            self.nT = 4

            self.AdrenalineGain = -60

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Zuk Cape): Changed amount of hits to {self.nT} with Max and Min to {self.DamMax} and {self.DamMin} respectively</li>'

        if self.Parent.MainHand.Name == 'Masterwork Spear of Annihilation' and self.Name in {'Dismember', 'Blood Tendrils', 'Slaughter'}:
            nExtend += 2  # Add 2 hits to the Dismember, Blood Tendrils and Slaughter abilities

            self.DamMax = np.append(self.DamMax, self.DamMax[-3: -1])
            self.DamMin = np.append(self.DamMin, self.DamMin[-3: -1])

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Masterwork Spear of Annihilation): Extended Max by 2 hits</li>'

        if nExtend > 0:
            self.nD += nExtend
            self.nT += nExtend

            # Extend the Timings array
            for i in range(0, nExtend):
                self.pForcedCrit = np.append(self.pForcedCrit, [self.pForcedCrit[-1]])
                self.Timings = np.append(self.Timings, [self.Timings[-1] + 2])

        # Other ability changes
        if self.Parent.Reflexes and self.Name == 'Anticipation':
            self.cdMax = 12

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Reflexes): Decreased cooldown to {self.cdMax} ticks</li>'

        if self.Parent.PlantedFeet and self.Name in {'Sunshine', 'Death\'s Swiftness'}:
            self.Bleed = False
            self.EffectDuration = 63

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Planted Feet): Removed bleed effect and changed effect duration to {self.EffectDuration} ticks</li>'

            return

        if self.Parent.Gloves.Name in {'Gloves of Passage', 'Enhanced gloves of Passage'} and self.Name in {'Smash', 'Havoc'}:
            self.Boost1 = True
            self.BoostX = .1
            self.EffectDuration = 2

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Gloves of Passage): Next ability will do 10% extra damage</li>'

        if self.Name == 'Hurricane' and self.Parent.MainHand.Name == 'Dark shard of Leng' and self.Parent.OffHand.Name == 'Dark sliver of Leng':
            self.Equipment = 'any'

            if self.Parent.Logger.DebugMode:
                self.Parent.Logger.Text += f'<li style="color: {self.Parent.Logger.TextColor["initialisation"]};">Ability upgrade {self.Name} (Hurricane): Changed Hurricane equipment requirement to any</li>'

        if self.Name == 'Aftershock' and self.Parent.Aftershock > 1:
            self.DamMax[0] *= self.Parent.Aftershock
            self.DamMin[0] *= self.Parent.Aftershock

        # Creating Hit objects which will be attached to the ability
        if self.nT > 0:

            self.Hits.extend([self.Hit(self, i) for i in range(0, self.nT)])

        if self.StunBindDam:
            self.HitsStunBind.extend([self.Hit(self, i, 'StunBindDam') for i in range(0, self.nT)])

        if self.SideTarget:
            self.HitsSideTarget.extend([self.Hit(self, i, 'SideTarget') for i in range(0, self.nT)])

        self.nHits = len(self.Hits)

    def AoECheck(self, dummy):
        """
        Duplicates hits if the ability does AoE damage and there are more than 1 target.

        :param dummy: The Dummy object.
        """

        if dummy.nTarget > self.MaxTargets:
            nDT = int(self.MaxTargets)
        else:
            nDT = dummy.nTarget

        if self.Name in {'Quake', 'Greater Flurry'}:  # DamMax = 0.94, DamMin = 0.2, DamAvg = 0.57 for ALL! targets
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.HitsSideTarget))

                for j in range(0, self.nT):
                    self.Hits[self.nT*(i + 1) + j].Target = i + 2

        elif self.Name == 'Hurricane':  # First hit on main target equals the hit for all other targets
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[0]))
                self.Hits[-1].Target = i + 2

        elif self.Name in {'Corruption Blast', 'Corruption Shot'}:  # First hit main target only, than spreading to all other targets
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[1:self.nD]))

                for j in range(0, self.nD - 1):
                    self.Hits[self.nD + (self.nD - 1) * i + j].Target = i + 2

        elif self.Name in {'Chain', 'Greater Chain', 'Ricochet', 'Greater Ricochet'}:  # Ricochet and Chain only hit up to 3 targets (except when perk)
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[:1]))

                for j in range(0, self.nT):
                    self.Hits[self.nT*(i + 1) + j].Target = i + 2
                    self.Hits[self.nT*(i + 1) + j].Time += 1

            if self.Name == 'Greater Chain':
                self.GreaterChainTargets = list(range(2, nDT + 1))

            # Apply Hits of greater Ricochet for which no targets are available back to target 1
            # but reduced.
            if self.Name == 'Greater Ricochet' and dummy.nTarget < self.MaxTargets:
                for i in range(0, int(self.MaxTargets - dummy.nTarget)):
                    self.Hits = np.append(self.Hits, deepcopy(self.Hits[0]))
                    self.Hits[-1].Time += 1

                    if i + 1 + dummy.nTarget <= 3:
                        self.Hits[-1].DamageMultiplier *= 0.5
                    else:
                        self.Hits[-1].DamageMultiplier /= 6

        elif self.Name == 'Book of Balance':  # Last hit of Book of Balance is AoE
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[-1]))
                self.Hits[-1].Target = i + 2

        elif self.Name == 'Book of Chaos':  # Book of chaos splits damage across targets
            self.Hits[0].DamMin /= nDT
            self.Hits[0].DamMax /= nDT
            self.Hits[0].Damage /= nDT

            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[-1]))
                self.Hits[-1].Target = i + 2

        else:
            for i in range(0, nDT - 1):
                self.Hits = np.append(self.Hits, deepcopy(self.Hits[0:self.nT]))

                for j in range(0, self.nT):
                    self.Hits[self.nT * (i + 1) + j].Target = i + 2

        self.nHits = len(self.Hits)

    class Hit:
        """
        The Hit object class used for defining a single hit of an ability.
        """

        def __init__(self, Abil, HitIndex, Special=None):
            self.Parent = Abil

            self.Special = Special

            self.Time = Abil.Timings[HitIndex] + Abil.DelayTime     # Timing of each hit
            if Abil.Standard:  # Type of effect (or standard) of each hit
                self.Type = 1
            elif Abil.Channeled:
                self.Type = 2
            elif Abil.Bleed:
                self.Type = 3
            else:
                self.Type = 10

            if Abil.Standard and Abil.Bleed and HitIndex > 0:
                self.Type = 3
            elif Abil.Standard and Abil.Puncture and HitIndex > 0:
                self.Type = 4

            self.Target = 1                                         # Target on which each hit should be applied, initialised as #1
            self.Index = HitIndex                                   # Index of the hit
            self.DamageMultiplier = 1
            self.pForcedCritExtra = 0  # Champions ring

            self.pForcedCrit = self.Parent.pForcedCrit[self.Index]
            self.pNatCrit = None

            self.DamMaxBonus = 0
            self.DamMinBonus = 0

            self._Damage = self.Damage

        @property
        def Damage(self):

            if not hasattr(self, '_Damage') or self._Damage is None:

                if self.Type in {1, 2}:
                    if self.Parent.Name != 'Bash':  # Bash ability has its own base damage
                        if self.Special in {'StunBindDam', 'SideTarget'}:
                            Max = self.Parent.SpecialDamMax[self.Index] * self.Parent.Parent.BaseDamageEffective
                            Min = self.Parent.SpecialDamMin[self.Index] * self.Parent.Parent.BaseDamageEffective
                        else:
                            Max = (self.Parent.DamMax[self.Index] + self.DamMaxBonus) * self.Parent.Parent.BaseDamageEffective
                            Min = (self.Parent.DamMin[self.Index] + self.DamMinBonus) * self.Parent.Parent.BaseDamageEffective
                    else:
                        Max = self.Parent.DamMax[self.Index] * self.Parent.Parent.BashBaseDamage
                        Min = self.Parent.DamMin[self.Index] * self.Parent.Parent.BashBaseDamage

                    CritCap = self.Parent.Parent.CritCap  # Critical hit damage cap
                    DmgCap = 10000  # Normal hit damage cap

                    if self.Parent.Parent.Precise:  # Increase min by 1.5% per rank
                        Min += self.Parent.Parent.Precise * 0.015 * Max

                    # ---------- Formula used to calculate averages, yoinked from the rs wiki ------------
                    if self.Parent.Parent.Aura == 'Equilibrium':  # If the equilibrium aura is active
                        self.pNatCrit = min(Max / (40 * (Max - Min)) + 0.0125, 1)
                    elif self.Parent.Parent.Equilibrium:  # Increase min by 3% per rank and decrease max by 1% per rank
                        self.pNatCrit = min(((25 - self.Parent.Parent.Equilibrium) * Max) / (500 * (Max - Min)) + self.Parent.Parent.Equilibrium / 2000, 1)

                        EqMinIncrease = self.Parent.Parent.Equilibrium * 0.03 * (Max - Min)
                        EqMaxDecrease = self.Parent.Parent.Equilibrium * 0.01 * (Max - Min)
                        Max = Max - EqMaxDecrease
                        Min = Min + EqMinIncrease
                    else:
                        self.pNatCrit = min((0.05 * Max) / (Max - Min), 1)

                    CritNatMin = max(Min + (1 - self.pNatCrit) * (Max - Min), Min)

                    CritForcedMin = (Min + 0.95 * (Max - Min))
                    # CritForcedMax = (Min + (0.95 * (Max - Min)) / 0.95)
                    CritForcedMax = Max

                    z1 = (CritCap - CritForcedMin) / (CritForcedMax - CritForcedMin)
                    z2 = (CritCap - CritNatMin) / (Max - CritNatMin)

                    y = (DmgCap - Min) / (CritNatMin - Min)

                    pForcedCrit = min(self.pForcedCrit, 1)

                    AvgCalc1 = max(0, min(1 - z1, 1)) * CritCap + min(max(0, z1), 1) * (min(CritCap, CritForcedMin) + min(CritCap, CritForcedMax)) / 2
                    AvgCalc2 = max(0, min(1 - z2, 1)) * CritCap + min(max(0, z2), 1) * (min(CritCap, CritNatMin) + min(CritCap, Max)) / 2
                    AvgCalc3 = max(0, min(1 - y, 1)) * DmgCap + min(max(0, y), 1) * (min(DmgCap, Min) + min(DmgCap, CritNatMin)) / 2

                    Avg = pForcedCrit * AvgCalc1 + (1 - pForcedCrit) * (self.pNatCrit * AvgCalc2 + (1 - self.pNatCrit) * AvgCalc3)
                    # ------------------------------------------------------------------------------------

                    if self.Parent.Parent.Logger.DebugMode:
                        self.Parent.Parent.Logger.Text += f'<li style="color: {self.Parent.Parent.Logger.TextColor["initialisation"]};">Ability Calculation: Avg hit of {self.Parent.Name} to {round(Avg, 2)}, pForced: {round(pForcedCrit, 4)}, pNat: {round(self.pNatCrit, 4)}</li>'

                    self._Damage = Avg

                elif self.Type in {3}:

                    if self.Parent.Name != 'Magma Tempest':
                        Max = self.Parent.DamMax[self.Index] * self.Parent.Parent.BaseDamage * self.Parent.Parent.GlovesOfPassageBoost
                        Min = self.Parent.DamMin[self.Index] * self.Parent.Parent.BaseDamage * self.Parent.Parent.GlovesOfPassageBoost
                    else:
                        Max = self.Parent.DamMax[self.Index] * self.Parent.Parent.BaseDamageEffective
                        Min = self.Parent.DamMin[self.Index] * self.Parent.Parent.BaseDamageEffective

                    ################## Calculate averages ########################
                    Avg = (Max + Min) / 2

                    if self.Parent.Parent.Logger.DebugMode:
                        self.Parent.Parent.Logger.Text += f'<li style="color: {self.Parent.Parent.Logger.TextColor["initialisation"]};">Ability Calculation: Avg hit of {self.Parent.Name} to {round(Avg, 2)}</li>'

                    self._Damage = Avg

                elif self.Type in {4, 10}:

                    Max = self.Parent.DamMax[self.Index] * self.Parent.Parent.BaseDamage
                    Min = self.Parent.DamMin[self.Index] * self.Parent.Parent.BaseDamage

                    ################## Calculate averages ########################
                    Avg = (Max + Min) / 2

                    if self.Parent.Parent.Logger.DebugMode:
                        self.Parent.Parent.Logger.Text += f'<li style="color: {self.Parent.Parent.Logger.TextColor["initialisation"]};">Ability Calculation: Avg hit of {self.Parent.Name} to {round(Avg, 2)}</li>'

                    self._Damage = Avg

                else:
                    self._Damage = 0

            return self._Damage

        def setDamage(self, damage):
            self._Damage = damage

        def __deepcopy__(self, memo):
            cls = self.__class__
            result = cls.__new__(cls)
            memo[id(self)] = result
            for k, v in self.__dict__.items():
                if k != 'Parent':
                    setattr(result, k, deepcopy(v, memo))
                else:
                    setattr(result, k, copy(v))
            return result


# def SpecialDamAvgCalc(Object, player, logger):
#     """
#     Calculates the average hit of a bleed effect of an ability.
#
#     :param Object: Hit OR Ability class object.
#     :param player: The Player object
#     :param logger: The Logger object
#     :return: Average bleed hits
#     """
#
#     Max = Object.DamMax.copy()
#     Min = Object.DamMin.copy()
#
#     # If the player has a boost from berserker or w/e, the aura boost is replaced by the ability boost
#     if player.PerkAftershock and Object.Name == 'Aftershock':
#         Max *= player.Ar * player.BaseDamage
#         Min *= player.Ar * player.BaseDamage
#     else:
#         Max *= player.BaseDamage
#         Min *= player.BaseDamage
#
#     ################## Calculate averages ########################
#     Avg = (Max + Min) / 2
#
#     if logger.DebugMode:
#         logger.Text += f'<li style="color: {logger.TextColor["initialisation"]};">Special Ability Calculation: Avg hit of {Object.Name} to {Avg}</li>'
#
#     return Avg
