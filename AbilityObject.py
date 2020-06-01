import numpy as np


# The ability class
class Ability:

    def __init__(self, abil_stats):

        ##############################################################
        ################### Reading from Excel #######################
        ##############################################################

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
            self.Timings = np.array([n * 1.8 for n in range(0, self.nD)])

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

        ##############################################################
        ########## Doing it manually for AoE abilities ###############
        ##############################################################

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

    ##############################################################
    ########## Calculate Averages of Standard/Channels ###########
    ##############################################################

    def StandardChannelDamAvgCalc(self, player, Do, Type=None, IDX=None):
        if IDX is None:
            Max = self.DamMax.copy()
            Min = self.DamMin.copy()
        else:
            if Type == 'Normal':
                Max = np.array([self.DamMax[IDX].copy()])
                Min = np.array([self.DamMin[IDX].copy()])
            elif Type == 'StunBind':
                Max = self.StunBindDamMax.copy()
                Min = self.StunBindDamMin.copy()
            else:
                Max = self.SideTargetMax.copy()
                Min = self.SideTargetMin.copy()

        # If the user selected the Flanking Perk, set stun abilities
        if player.PerkFlanking:
            if self.Name in {'Backhand', 'Impact', 'Binding Shot'}:
                self.Stun = False  # Abilities above lose their stun effect

                for i in range(0, self.nS):  # Increase min by 8% per rank, max by 40% per rank
                    Max[i] += 0.4 * player.Fr
                    Min[i] += 0.08 * player.Fr

            if self.Name in {'Forceful Backhand', 'Deep Impact', 'Tight Bindings'}:
                self.Stun = False  # Abilities above lose their stun effect

                for i in range(0, self.nS):  # Increase min by 6% per rank, max by 30% per rank
                    Max[i] += 0.3 * player.Fr
                    Min[i] += 0.06 * player.Fr

        if self.Name != 'Bash':  # Bash ability has its own base damage
            Max = Max * player.BaseDamageEffective
            Min = Min * player.BaseDamageEffective
        else:
            Max *= player.BashBaseDamage
            Min *= player.BashBaseDamage

        # Level boost due to potions/aura's
        Max += 8 * player.LevelBoost
        Min += 4 * player.LevelBoost

        Avg = []
        CritCap = player.CritCap    # Critical hit damage cap
        DmgCap = 10000              # Normal hit damage cap
        # For all hits
        for i in range(0, len(Max)):

            # If the user selected the Precise perk
            if player.PerkPrecise:
                # Increase min by 1.5% per rank
                PrMinIncrease = player.Pr * 0.015 * Max[i]

                Min[i] = Min[i] + PrMinIncrease

            # ---------- Formula used to calculate averages, yoinked from the rs wiki ------------
            if player.Aura == 'Equilibrium':  # If the equilibrium aura is active
                pNatCrit = min(Max[i] / (40 * (Max[i] - Min[i])) + 0.0125, 1)
            elif player.PerkEquilibrium:  # Elif the user selected the equilibrium perk
                pNatCrit = min(((25 - player.Er) * Max[i]) / (500 * (Max[i] - Min[i])) + player.Er / 2000, 1)

                # Increase min by 3% per rank and decrease max by 1% per rank
                EqMinIncrease = player.Er * 0.03 * (Max[i] - Min[i])
                EqMaxDecrease = player.Er * 0.01 * (Max[i] - Min[i])

                Max[i] = Max[i] - EqMaxDecrease
                Min[i] = Min[i] + EqMinIncrease
            else:
                pNatCrit = min((0.05 * Max[i]) / (Max[i] - Min[i]), 1)

            # If the player has a boost from Berserk or w/e, the aura boost is replaced by the ability boost
            if player.Boost:  # If the player has a damage boost
                Max[i] *= player.BoostX * player.Boost1X
                Min[i] *= player.BoostX * player.Boost1X
            else:
                Max[i] *= player.BaseBoost * player.Boost1X
                Min[i] *= player.BaseBoost * player.Boost1X

            CritNatMin = max(Min[i] + (1 - pNatCrit) * (Max[i] - Min[i]), Min[i])

            CritForcedMin = (Min[i] + 0.95 * (Max[i] - Min[i]))
            CritForcedMax = (Min[i] + (0.95 * (Max[i] - Min[i])) / 0.95)

            z1 = (CritCap - CritForcedMin) / (CritForcedMax - CritForcedMin)
            z2 = (CritCap - CritNatMin) / (Max[i] - CritNatMin)

            y = (DmgCap - Min[i]) / (CritNatMin - Min[i])

            pForcedCrit = min(player.ForcedCritBuff + player.AbilCritBuff, 1)

            # If the ability Greater Fury was used, calculate new CritBuff and return immediately
            if player.GreaterFuryCritCheck:
                player.AbilCritBuff = (pForcedCrit + (1 - pForcedCrit) * pNatCrit) + (1 - pForcedCrit) * (1 - pNatCrit) * 0.1

                player.GreaterFuryCritCheck = False

                return None

            # If an adrenaline buff due to Meteor Strike, Tsunami or Incendiary Shot is active, calculate extra adrenaline and return immediately
            if player.CritAdrenalineBuff:
                player.BasicAdrenalineGain += (pForcedCrit + (1 - pForcedCrit) * pNatCrit) * 10

                player.CritAdrenalineBuff = False

                return None

            AvgCalc1 = max(0, min(1 - z1, 1)) * CritCap + min(max(0, z1), 1) * (min(CritCap, CritForcedMin) + min(CritCap, CritForcedMax)) / 2
            AvgCalc2 = max(0, min(1 - z2, 1)) * CritCap + min(max(0, z2), 1) * (min(CritCap, CritNatMin) + min(CritCap, Max[i])) / 2
            AvgCalc3 = max(0, min(1 - y, 1)) * DmgCap + min(max(0, y), 1) * (min(DmgCap, Min[i]) + min(DmgCap, CritNatMin)) / 2

            Avg.append(pForcedCrit * AvgCalc1 + (1 - pForcedCrit) * (pNatCrit * AvgCalc2 + (1 - pNatCrit) * AvgCalc3))
            # ------------------------------------------------------------------------------------

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {round(Avg[i], 2)}, pForced: {round(pForcedCrit, 4)}, pNat: {round(pNatCrit, 4)}</li>'

        # Manually calculate the average of Shadow Tendrils
        if self.Name in {'Shadow Tendrils'}:
            Avg[0] = 0.1 * Avg[0] * 2 + 0.18 * Avg[0] * 3 + 0.216 * Avg[0] * 4 + 0.504 * Avg[0] * 5

        return Avg

    ##############################################################
    ############### Calculate Averages of Bleeds #################
    ##############################################################

    def BleedDamAvgCalc(self, player, Do):
        Max = self.DoTMax.copy()
        Min = self.DoTMin.copy()

        Avg = []

        nExtend = 0  # Variable used for bleed extensions

        # If the user selected the Lunging Perk, set bleeds
        if player.PerkLunging and self.Name in {'Dismember', 'Combust', 'Fragmentation Shot'}:
            # Bleeds of Combust and Fragmentation Shot are multiplied by 1.5 upon walking instead of 2
            if self.Name != 'Dismember':
                self.BleedOnMove = 1.5

            # Increase max hit by 0.2 for every rank
            Max[0] += 0.2 * player.Lr

        # If the player has a boost from berserker or w/e, the aura boost is replaced by the ability boost
        if player.Boost:  # If the player has a damage boost
            Max *= player.BaseDamage
            Min *= player.BaseDamage
        else:
            Max *= player.BaseBoost * player.BaseDamage
            Min *= player.BaseBoost * player.BaseDamage

        ##############################################################
        ####################### Bleed boosts #########################
        ##############################################################

        # If the user selected the strength cape perk, add 3 hits to the Dismember ability
        if player.StrengthCape and self.Name == 'Dismember':
            nExtend += 3

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability change: Extended {self.Name} by 3 hits</li>'

        # If the user selected the MS of Annihilation, add 2 hits to the Dismember, Blood Tendrils and Slaughter abilities
        if player.MSoA and self.Name in {'Dismember', 'Blood Tendrils', 'Slaughter'}:
            nExtend += 2

            # If Blood Tendrils, extend damage arrays
            if self.Name == 'Blood Tendrils':
                Max = np.append(Max, Max[-3: -1])
                Min = np.append(Min, Min[-3: -1])

                self.nD += nExtend  # Increase amount of DoT hits
                self.nT += nExtend  # Increase amount of total hits

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability change: Extended {self.Name} by 2 hits</li>'

        ##############################################################
        ################## Calculate averages ########################
        ##############################################################

        # If Massacre or Deadshot, bleed avg is simply bleed max / amount of hits
        if self.Name in {'Massacre', 'Deadshot'}:
            Avg = [Max[0] / self.nD] * self.nD

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {self.nD}x {round(Avg[0], 2)}</li>'

        # Elif Blood Tendrils, Corruoptions Shot/Blast or Incendiary Shot, bleed avg is simply max + min / 2
        elif self.Name in {'Blood Tendrils', 'Corruption Shot', 'Corruption Blast', 'Incendiary Shot'}:
            for i in range(0, self.nD):
                Avg.append(((Max[i] + Min[i]) / 2))

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {Avg[i]}</li>'

        # Elif Death's Swiftness and Sunshine, max and min or total damage from 16 hits
        elif self.Name in {'Death\'s Swiftness', 'Sunshine'}:

            # If the user selected the Planted Feet weapon perk, remove the bleed and increase duration
            if not player.PerkPlantedFeet:
                Avg = [(Max[0] / self.nD + Min[0] / self.nD) / 2] * self.nD

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {self.nD}x {round(Avg[0], 2)}</li>'
            else:
                self.Bleed = False
                self.BoostTime = 37.8

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.init_color};">Ability change: Extended {self.Name} boost time to {self.BoostTime} hits</li>'

        else:  # Else the bleed is 1/max + ((max-1)/max) * (1+(max-1)/2)) / amount of hits
            Avg = [(Min[0] / Max[0] * Min[0] + ((Max[0] - Min[0]) / Max[0]) * (Min[0] + (Max[0] - Min[0]) / 2)) / self.nD] * (self.nD + nExtend)

            self.nD += nExtend  # Increase amount of DoT hits
            self.nT += nExtend  # Increase amount of total hits

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {self.nD}x {round(Avg[0], 2)}</li>'

        # Extend the Timings array if nExtend > 0
        for i in range(0, nExtend):
            self.Timings = np.append(self.Timings, [self.Timings[-1] + 1.2])

        return Avg

    ##############################################################
    ############# Calculate puncture averages ####################
    ##############################################################

    def PunctureDamAvgCalc(self, player, Do):
        Avg = []

        # If the ability has a puncture effect: Calculate its average hit
        if self.Puncture and self.Name == 'Greater Dazing Shot':
            # Set puncture max and mins
            Max = np.array([7 / 15 * 0.072, 5 / 15 * 0.072, 2 / 15 * 0.072, 1 / 15 * 0.72]) * player.BaseBoost * player.BaseDamage
            Min = np.array([7 / 15 * 0.058, 5 / 15 * 0.058, 2 / 15 * 0.058, 1 / 15 * 0.58]) * player.BaseBoost * player.BaseDamage

            # Set puncture averages
            for i in range(0, self.nD):
                Avg.append((Max[i] + Min[i]) / 2)

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.init_color};">Ability Calculation: Avg hit of {self.Name} to {round(Avg[i], 2)}</li>'

        return Avg

    ##############################################################
    ################ Construct Hit Objects #######################
    ##############################################################

    def ConstructHitObject(self, player, Do):
        # If the ability is a standard or channeled ability
        if self.Standard or self.Channeled:
            DamAvg = self.StandardChannelDamAvgCalc(player, Do)

            # If the ability is a standard ability
            if self.Standard:
                for i in range(0, self.nS):  # For every hit
                    self.Hits.append(self.Hit(self, DamAvg, 1, 1, i, i))

                # If the ability has boosted damage when target is stunned or bound
                if self.StunBindDam:
                    StunBindDamAvg = self.StandardChannelDamAvgCalc(player, Do, 'StunBind', 0)

                    for i in range(0, self.nS):  # For every hit
                        self.HitsStunBind.append(self.Hit(self, StunBindDamAvg, 5, 1, i, i))

            # Else the ability is a channeled ability
            else:
                for i in range(0, self.nS):  # For every hit
                    self.Hits.append(self.Hit(self, DamAvg, 2, 1, i, i))

            # If the ability does different AoE damage for side targets
            if self.SideTarget:
                SideTargetAvg = self.StandardChannelDamAvgCalc(player, Do, 'SideTarget', 0)

                for i in range(0, self.nS):  # For every hit
                    self.SideTargetAvg.append(self.Hit(self, SideTargetAvg, 6, 1, i, i))

        # If the ability has a bleed effect
        if self.Bleed:
            DoTAvg = self.BleedDamAvgCalc(player, Do)

            for i in range(0, self.nD):  # For every DoT hit
                self.DoTHits.append(self.Hit(self, DoTAvg, 3, 1, i, self.nS + i))

        # If the ability has a puncture effect
        if self.Puncture:
            DoTAvg = self.PunctureDamAvgCalc(player, Do)

            for i in range(0, self.nD):  # For every DoT hit
                self.DoTHits.append(self.Hit(self, DoTAvg, 4, 1, i, self.nS + i))

    ##############################################################
    ################### Hit Object Class #########################
    ##############################################################

    # The Hit: Used for defining a single hit
    class Hit:

        def __init__(self, ability, Avg, Type, Target, Index, HitIndex):
            self.Damage = Avg[Index]                                    # Array containing the amount of damage for each hit
            self.Time = ability.Timings[HitIndex] + ability.DelayTime   # Array containing the timing of each hit
            self.Type = Type                                            # Array containing the type of effect (or standard) of each hit
            self.Target = Target                                        # Array containing the target on which each hit should be applied
            self.Index = HitIndex                                       # Array containing the index of the hit
            self.Name = ability.Name                                    # Array containing the name of the ability causing the hit


