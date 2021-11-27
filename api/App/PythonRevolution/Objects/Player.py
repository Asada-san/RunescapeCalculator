import numpy as np


class Player:
    """
    The Player class. A player attacks the dummy.
    """

    def __init__(self, userInput):
        self.nStall = 0
        self.Cooldown = []                          # List of abilities which are currently on cooldown
        self.ChanAbil = False                       # When True, the player used a channeled ability
        self.ChanTime = 0                           # Duration of the channeled ability
        self.GreaterChain = False                   # True when greater chain has been activated
        self.GreaterChainDuration = 0               # Time for the greater chain effect to take effect
        self.GreaterChainTargets = []               # Target numbers hit by Greater Chain minus main target
        self.BaseBoost = 1                          # Base damage boost for all abilities
        self.LevelBoost = 0                         # Amount of boosted combat levels
        self.Boost = False                          # True if a damage boosting ability has been used
        self.BoostX = 1                             # Damage output multiplier
        self.BoostTime = 0                          # Amount of time of damage boost
        self.Boost1 = False                         # True if the player does more damage on the next ability only
        self.Boost1X = 1                            # Damage output multiplier for the next ability only
        self.AbilCritBuff = 0                       # Critical hit buff for next ability
        self.CritStack = 0                          # Critical hit stack used for Fury and (Greater) Concentrated Blast
        self.ChannelCritStack = 0                   # Critical hit stack used for magic channeling abilities whilst wearing the Channeler's Ring
        self.GreaterFuryCritCheck = False           # True if Greater Fury was used in an attack cycle
        self.CritAdrenalineBuff = False             # True if Meteor Strike, Tsunami or Incendiary Shot were used in an attack cycle
        self.CritAdrenalineBuffTime = 0             # Timer for adrenaline buff due to the above ^
        self.BasicAdrenalineGain = 0                # Adrenaline boost for basic abilities due to the above ^
        self.DragonBreathGain = False               # True if Dragon Breath is on the bar and there are more than 2 dummies
        # self.DragonBreathCombustTime = 0            # Timer for Combust boost due to the Dragon Breath ability

        self.Switcher = userInput['switchStatus']                   # True if the user want to use both 2h and dual weapons
        self.Afk = not userInput['afkStatus']                       # True if the player intends to afk

        # self.KerapacWristWraps = userInput['KerapacWristWraps']     # True if the user selected Kerapac's Wrist Wraps

        self.Cape = userInput['Cape']                   # Cape selected by the user

        if self.Cape == 0:
            self.Cape = ''

        self.MSoA = userInput['MSoA']                   # True if the user selected the Masterwork Spear of Annihilation
        self.Ring = userInput['Ring']                   # Ring selected by the user

        if self.Ring == 'ReaversRing':
            self.InitCritBuff = 0.05
        else:
            self.InitCritBuff = 0

        self.Aura = userInput['Aura']                   # Aura selected by the user
        self.CoE = userInput['CoE']                     # True if the user selected the Conservation of Energy Relic

        if 0.1 <= userInput['BerserkersFury'] <= 5.5:
            self.BerserkersFury = 1 + userInput['BerserkersFury'] / 100
        else:
            self.BerserkersFury = 1                     # Damage multiplier due to the Berserkers Fury relic

        self.Pr = userInput['Precise']                  # Precise rank
        self.PerkPrecise = self.Pr > 0                  # True if user selected the Precise perk

        self.Er = userInput['Equilibrium']              # Equilibrium rank
        self.PerkEquilibrium = self.Er > 0              # True if the user selected the Equilibrium perk

        self.Br = userInput['Biting']                   # Biting rank
        self.PerkBiting = self.Br > 0                   # True if the user selected the Biting perk
        self.ForcedCritBuff = self.Br * 0.02            # Increase Forced Critical Hit buff by .02 per Biting rank

        if userInput['Level20Gear']:                    # True if the user selected level 20 gear
            self.ForcedCritBuff *= 1.1                  # Biting perk crit buff increased 1.1x

        if userInput['Grimoire']:                       # True if the user selected the Grimoire
            self.ForcedCritBuff += 0.12                 # ADDITIVE: Add .12 to Forced Critical Hit buff
            self.CritCap = 15000                        # Critical hit damage cap increased to 15k
        else:
            self.CritCap = 12000                        # Normal critical hit damage cap

        self.Fr = userInput['Flanking']                 # Flanking rank
        self.PerkFlanking = self.Fr > 0                 # True if the user selected the Flanking perk

        self.Lr = userInput['Lunging']                  # Lunging rank
        self.PerkLunging = self.Lr > 0                  # True if the user selected the Lunging perk

        self.Cr = userInput['Caroming']                 # Caroming rank
        self.PerkCaroming = self.Cr > 0                 # True if the user selected the Caroming perk

        self.Rr = userInput['Ruthless']                 # Ruthless rank
        self.PerkRuthless = self.Rr > 0                 # True if the user selected the Ruthless perk

        self.Ar = userInput['Aftershock']               # Aftershock rank
        self.PerkAftershock = self.Ar > 0               # True if the user selected the Aftershock perk

        self.SBr = userInput['ShieldBashing']           # Shield Bashing rank
        self.PerkShieldBashing = self.SBr > 0           # True if the user selected the Shield Bashing perk

        self.Ur = userInput['Ultimatums']               # Ultimatums rank
        self.PerkUltimatums = self.Ur > 0               # True if the user selected the Ultimatums perk

        self.Ir = userInput['Impatient']                # Ultimatums rank
        self.PerkImpatient = self.Ir > 0                # True if the user selected the Ultimatums perk

        self.PerkPlantedFeet = userInput['PlantedFeet']  # True if the user selected the Planted Feet perk
        self.PerkReflexes = userInput['Reflexes']       # True if the user selected the Reflexes Feet perk

        if 1 <= userInput['baseDamage'] <= 10000:
            self.BaseDamage = userInput['baseDamage']
        else:
            self.BaseDamage = 1000                      # Base weapon damage

        self.BaseDamageEffective = self.BaseDamage

        if 1 <= userInput['ShieldArmourValue'] <= 1000:
            self.ShieldArmourValue = userInput['ShieldArmourValue']
        else:
            self.ShieldArmourValue = 491                # Shield Armour Value

        if 1 <= userInput['DefenceLevel'] <= 200:
            self.DefenceLevel = userInput['DefenceLevel']
        else:
            self.DefenceLevel = 99                      # Defence Level

        self.BashBaseDamage = self.BaseDamageEffective + self.DefenceLevel + self.ShieldArmourValue  # Base Damage for the Bash ability

        if 1 <= userInput['StrengthBoost'] <= 60:
            self.StrengthLevelBoost = userInput['StrengthBoost']
        else:
            self.StrengthLevelBoost = 0                 # Strength Boost of the player in levels

        if 1 <= userInput['RangedBoost'] <= 60:
            self.RangedLevelBoost = userInput['RangedBoost']
        else:
            self.RangedLevelBoost = 0                   # Ranged Boost of the player in levels

        if 1 <= userInput['MagicBoost'] <= 60:
            self.MagicLevelBoost = userInput['MagicBoost']
        else:
            self.MagicLevelBoost = 0                    # Magic Boost of the player in levels

        if userInput['StrengthPrayer'] < 1:
            self.StrengthPrayerBoost = 1
        else:
            self.StrengthPrayerBoost = userInput['StrengthPrayer']    # Boost due to melee prayers

        if userInput['RangedPrayer'] < 1:
            self.RangedPrayerBoost = 1
        else:
            self.RangedPrayerBoost = userInput['RangedPrayer']        # Boost due to ranged prayers

        if userInput['MagicPrayer'] < 1:
            self.MagicPrayerBoost = 1
        else:
            self.MagicPrayerBoost = userInput['MagicPrayer']          # Boost due to magic prayers

    def TimerCheck(self, logger):
        """
        Checks the ability cooldowns, adrenaline buffs, boosts and channeling status.

        :param logger: The Logger object.
        """

        # For all abilities currently on cooldown
        for i in range(len(self.Cooldown) - 1, -1, -1):
            self.Cooldown[i].cdTime -= 1

            if self.Cooldown[i].cdTime == 0:
                self.Cooldown[i].cdStatus = False

                if logger.DebugMode:
                    logger.write(22, self.Cooldown[i].Name)

                self.Cooldown.pop(i)  # Delete it from the cooldown list

        # If the player has an adrenaline buff going
        if self.CritAdrenalineBuffTime:
            self.CritAdrenalineBuffTime -= 1

            if self.CritAdrenalineBuffTime == 0:
                self.CritAdrenalineBuff = False

                if logger.DebugMode:
                    logger.write(23)

        # If the player used a channeled ability and its still active
        if self.ChanAbil:
            self.ChanTime -= 1

            if self.ChanTime == 0:
                self.ChanAbil = False

                if self.GreaterChain:
                    self.resetGreaterChain()

                self.ChannelCritStack = 0

                if logger.DebugMode:
                    logger.write(24)

        # If the player has a boost going on
        if self.Boost:
            self.BoostTime -= 1

            if self.BoostTime == 0:
                self.Boost = False
                self.BoostX = 1

                if logger.DebugMode:
                    logger.write(25)

        # If the player has a Greater Chain effect going on
        if self.GreaterChain:
            self.GreaterChainDuration -= 1

            if self.GreaterChainDuration == 0:
                self.resetGreaterChain()

                if logger.DebugMode:
                    logger.write(26)

        # # If the player has a Greater Chain effect going on
        # if self.DragonBreathCombustTime:
        #     self.DragonBreathCombustTime -= 1
        #
        #     if self.DragonBreathCombustTime == 0:
        #         if logger.DebugMode:
        #             logger.write(49)

    def resetGreaterChain(self):
        self.GreaterChainDuration = 0
        self.GreaterChain = False
        self.GreaterChainTargets = []
