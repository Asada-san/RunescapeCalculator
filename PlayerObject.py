import numpy as np


# The Player class: A player attacks the dummy
class Player:

    def __init__(self, opt, Do):
        self.Cooldown = []                  # List of abilities which are currently on cooldown
        self.ChanAbil = False               # When True, the player used a channeled ability
        self.ChanTime = 0                   # Duration of the channeled ability
        self.BaseBoost = 1                  # Base damage boost for all abilities
        self.LevelBoost = 0                 # Amount of boosted combat levels
        self.Boost = False                  # True if a damage boosting ability has been used
        self.BoostX = 1                     # Damage output multiplier
        self.BoostTime = 0                  # Amount of time of damage boost
        self.Boost1 = False                 # True if the player does more damage on the next ability only
        self.Boost1X = 1                    # Damage output multiplier for the next ability only
        self.AbilCritBuff = 0               # Critical hit buff for next ability
        self.CritStack = 0                  # Critical hit stack used for Fury and Concentrated Blast
        self.GreaterFuryCritCheck = False   # True if Greater Fury was used in an attack cycle
        self.CritAdrenalineBuff = False     # True if Meteor Strike, Tsunami or Incendiary Shot were used in an attack cycle
        self.CritAdrenalineBuffTime = 0     # Timer for adrenaline buff due to the above ^
        self.BasicAdrenalineGain = 0        # Adrenaline boost for basic abilities due to the above ^

        ##############################################################
        ############ Set various user selected options ###############
        ##############################################################

        self.Switcher = opt['switchStatus']         # True if the user want to use both 2h and dual weapons
        self.Afk = not opt['afkStatus']             # True if the player intends to afk
        self.StrengthCape = opt['StrengthCape']     # True if the user selected the Strength Cape
        self.RoV = opt['RoV']                       # True if the user selected the Ring of Vigour
        self.MSoA = opt['MSoA']                     # True if the user selected the Masterwork Spear of Annihilation
        self.Aura = opt['Aura']                     # Aura selected by the user

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">User select: Switcher {self.Switcher}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Efficient {self.Afk}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Str Cape {self.StrengthCape}</li>' \
                       f'<li style="color: {Do.init_color};">User select: RoV {self.RoV}</li>' \
                       f'<li style="color: {Do.init_color};">User select: MSoA {self.MSoA}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Aura {self.Aura}</li>'

        ##############################################################
        ##### Set various perk and critical hit related stuff ########
        ##############################################################

        self.Pr = opt['Precise']                # Precise rank
        self.PerkPrecise = self.Pr > 0          # True if user selected the Precise perk

        self.Er = opt['Equilibrium']            # Equilibrium rank
        self.PerkEquilibrium = self.Er > 0      # True if the user selected the Equilibrium perk

        self.Br = opt['Biting']                 # Biting rank
        self.PerkBiting = self.Br > 0           # True if the user selected the Biting perk
        self.ForcedCritBuff = self.Br * 0.02    # Increase Forced Critical Hit buff by .02 per Biting rank

        if opt['Level20Gear']:                  # True if the user selected level 20 gear
            self.ForcedCritBuff *= 1.1          # Biting perk crit buff increased 1.1x

        if opt['Grimoire']:                     # True if the user selected the Grimoire
            self.ForcedCritBuff += 0.12         # ADDITIVE: Add .12 to Forced Critical Hit buff
            self.CritCap = 15000                # Critical hit damage cap increased to 15k
        else:
            self.CritCap = 12000                # Normal critical hit damage cap

        self.Fr = opt['Flanking']               # Flanking rank
        self.PerkFlanking = self.Fr > 0         # True if the user selected the Flanking perk

        self.Lr = opt['Lunging']                # Lunging rank
        self.PerkLunging = self.Lr > 0          # True if the user selected the Lunging perk

        self.Ar = opt['Aftershock']             # Aftershock rank
        self.PerkAftershock = self.Ar > 0       # True if the user selected the Aftershock perk

        self.PerkPlantedFeet = opt['PlantedFeet']   # True if the user selected the Planted Feet perk

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">User select: Precise Perk {self.PerkPrecise}, {self.Pr}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Equilibrium Perk {self.PerkEquilibrium}, {self.Er}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Biting Perk {self.PerkBiting}, {self.Br}</li>' \
                       f'<li style="color: {Do.init_color};">User select: CritBuff {round(self.ForcedCritBuff, 3)}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Flanking Perk {self.PerkFlanking}, {self.Fr}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Lunging Perk {self.PerkLunging}, {self.Lr}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Aftershock Perk {self.PerkAftershock}, {self.Ar}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Planted Feet Perk {self.PerkPlantedFeet}</li>'\

        ##############################################################
        ########## Set various base damage related stuff #############
        ##############################################################

        # Determine Base Damage of the player
        if opt['baseDamage'] != '' and 0 <= opt['baseDamage'] <= 10000:
            self.BaseDamage = opt['baseDamage']     # Base weapon damage of the player
        else:
            self.BaseDamage = 1000

        self.BaseDamageEffective = self.BaseDamage

        # Determine Shield Armour Value of the player
        if opt['ShieldArmourValue'] != '' and 0 <= opt['ShieldArmourValue'] <= 1000:
            self.ShieldArmourValue = opt['ShieldArmourValue']
        else:
            self.ShieldArmourValue = 491

        # Determine Defence Level of the player
        if opt['DefenceLevel'] != '' and 0 <= opt['DefenceLevel'] <= 200:
            self.DefenceLevel = opt['DefenceLevel']
        else:
            self.DefenceLevel = 99

        self.BashBaseDamage = self.BaseDamageEffective + self.DefenceLevel + self.ShieldArmourValue  # Base Damage for the Bash ability

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">User select: Base Damage: {self.BaseDamage}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Bash Base Damage: {self.BashBaseDamage}</li>'

        ##############################################################
        ############# Set various boost related stuff ################
        ##############################################################

        # Strength Boosts
        if opt['StrengthBoost'] != '' and 0 <= opt['StrengthBoost'] <= 60:
            self.StrengthLevelBoost = opt['StrengthBoost']  # Strength Boost of the player in levels
        else:
            self.StrengthLevelBoost = 0

        self.StrengthPrayerBoost = opt['StrengthPrayer']

        # Ranged Boosts
        if opt['RangedBoost'] != '' and 0 <= opt['RangedBoost'] <= 60:
            self.RangedLevelBoost = opt['RangedBoost']  # Ranged Boost of the player in levels
        else:
            self.RangedLevelBoost = 0

        self.RangedPrayerBoost = opt['RangedPrayer']

        # Magic Boosts
        if opt['MagicBoost'] != '' and 0 <= opt['MagicBoost'] <= 60:
            self.MagicLevelBoost = opt['MagicBoost']  # Magic Boost of the player in levels
        else:
            self.MagicLevelBoost = 0

        self.MagicPrayerBoost = opt['MagicPrayer']

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">User select: Strength Level Boost: {self.StrengthLevelBoost}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Magic Prayer Boost: {self.StrengthPrayerBoost}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Ranged Level Boost: {self.RangedLevelBoost}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Ranged Prayer Boost: {self.RangedPrayerBoost}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Magic Level Boost: {self.MagicLevelBoost}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Magic Prayer Boost: {self.MagicPrayerBoost}</li>'

    def TimerCheck(self, Do):

        ############### Check ability cooldowns ######################

        # For all abilities currently on cooldown
        for i in range(len(self.Cooldown) - 1, -1, -1):
            self.Cooldown[i].cdTime -= .6  # Subtract tick time

            # If the cooldown reached zero: reset
            if self.Cooldown[i].cdTime <= 0.01:
                self.Cooldown[i].cdTime = 0
                self.Cooldown[i].cdStatus = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.nor_color};">{self.Cooldown[i].Name} no longer on cd</li>\n'

                self.Cooldown.pop(i)  # Delete it from the cooldown list

        ########### Check player adrenaline buff status ##############

        # If the player has an adrenaline buff going
        if self.CritAdrenalineBuffTime:
            self.CritAdrenalineBuffTime -= .6  # Subtract tick time

            # If the adrenaline buff time reached zero: reset
            if self.CritAdrenalineBuffTime <= 0.01:
                self.CritAdrenalineBuffTime = 0
                self.CritAdrenalineBuff = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.nor_color};">Player adrenaline gain buff has worn out</li>\n'

        ############# Check player channeling status #################

        # If the player used a channeled ability and its still active
        if self.ChanAbil:
            self.ChanTime -= .6  # Subtract tick time

            # If the channeled ability time reached zero: reset
            if self.ChanTime <= 0.01:
                self.ChanTime = 0
                self.ChanAbil = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.nor_color};">Player is no longer performing a channeled ability</li>\n'

        ################ Check player boost status ###################

        # If the player has a boost going on
        if self.Boost:
            self.BoostTime -= .6  # Subtract tick time

            # If the channeled ability time reached zero: reset
            if self.BoostTime <= 0.01:
                self.BoostTime = 0
                self.Boost = False
                self.BoostX = 1

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.nor_color};">Player damage boost has been reset</li>\n'

