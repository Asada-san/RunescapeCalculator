from api.App.PythonRevolution.Objects.Bar import Bar
from api.App.PythonRevolution.Objects.Ability import Ability
import math
from copy import deepcopy


class Player:
    """
    The Player class. A player attacks the dummy.
    """

    def __init__(self, data, gear, logger):
        # self.AbilityBook = {}
        self.Logger = logger

        # Main-hand
        if data['MainHand'] in gear['Main-hand'].keys():
            self.MainHand = gear['Main-hand'][data['MainHand']]
        else:
            # self.MainHand = gear['Main-hand']['Main-hand']
            self.MainHand = gear['Main-hand']['Dark shard of Leng']

        # Off-hand
        if data['OffHand'] in gear['Off-hand'].keys():
            self.OffHand = gear['Off-hand'][data['OffHand']]
        else:
            self.OffHand = gear['Off-hand']['Off-hand']

        self.Helm = None
        self.Chest = None
        self.Legs = None
        self.Boots = None
        self.Amulet = None

        self.Ring = None
        self.Cape = None
        self.Aura = None
        self.Gloves = None
        self.Pocket = None
        self.Ammo = None
        ToEquip = ['Gloves', 'Aura', 'Ring', 'Pocket', 'Ammo', 'Cape']

        for slot in ToEquip:
            if data[slot] in gear[slot].keys():
                setattr(self, slot, gear[slot][data[slot]])
            else:
                setattr(self, slot, gear[slot][slot])

        self.Special = {}
        self.PocketHitCounter = 0

        self.Precise = data['Precise']
        self.Equilibrium = data['Equilibrium']
        self.Biting = data['Biting']
        self.Flanking = data['Flanking']
        self.Lunging = data['Lunging']
        self.Caroming = data['Caroming']
        self.Ruthless = data['Ruthless']
        self.Aftershock = data['Aftershock']
        self.ShieldBashing = data['ShieldBashing']
        self.Ultimatums = data['Ultimatums']
        self.Impatient = data['Impatient']
        self.PlantedFeet = data['PlantedFeet']
        self.Reflexes = data['Reflexes']

        self.AsDamage = 0
        self.JasDamage = 0                              # Damage done during the Jas Scripture buff
        self.JasTime = 0                                # Current duration of Jas Scripture buff

        self.Level20Gear = 1.1 if data['Level20Gear'] else 1  # Biting perk crit buff increased 1.1x

        if self.Pocket.Name == 'Erethdor\'s Grimoire':  # True if the user selected the Grimoire
            self.CritCap = 15000  # Critical hit damage cap increased to 15k
        else:
            self.CritCap = 12000  # Normal critical hit damage cap

        self.AnachroniaCapeStand = data['AnachroniaCapeStand']
        self.ChanTime = 0
        self.GreaterChainTime = 0  # Time for the greater chain effect to take effect
        self.GreaterChainTargets = []  # Target numbers hit by Greater Chain minus main target
        self.Bar = Bar(self)
        self.BoostX = []
        self.BoostTime = []  # Amount of time of damage boost
        self.BoostName = []
        self.Boost = False
        self.Boost1 = False
        self.Boost1XAbility = None
        self.BasicAdrenalineGain = 0

        self.Afk = not data['afkStatus']
        self.Switcher = data['switchStatus']
        self.RingOfVigourPassive = data['ringOfVigourPassive']

        if 0.1 <= data['BerserkersFury'] <= 5.5:
            self.BerserkersFury = 1 + data['BerserkersFury'] / 100
        else:
            self.BerserkersFury = 1

        self.FuryOfTheSmall = data['FotS']
        self.ConservationOfEnergy = data['CoE']
        self.MaxAdrenaline = 110 if data['HeightenedSenses'] else 100  # Maximum amount of adrenaline

        # Check user input for a possible value for simulation time and starting adrenaline
        if data['Adrenaline'] != '' and 0 <= data['Adrenaline'] <= self.MaxAdrenaline:
            self.Adrenaline = round(data['Adrenaline'], 0)
        else:
            self.Adrenaline = self.MaxAdrenaline  # Set starting adrenaline

        self.CritAdrenalineBuffTime = 0
        self.GlovesOfPassageMax = 10
        self.GlovesOfPassageBoost = 1
        self.GlovesOfPassageTime = 0

        if 1 <= data['StrengthLevel'] <= 99:
            self.StrengthLevel = data['StrengthLevel']
        else:
            self.StrengthLevel = 99
        if 1 <= data['RangedLevel'] <= 99:
            self.RangedLevel = data['RangedLevel']
        else:
            self.StrengthLevel = 99
        if 1 <= data['MagicLevel'] <= 99:
            self.MagicLevel = data['MagicLevel']
        else:
            self.StrengthLevel = 99

        if 0 <= data['StrengthBoost'] <= 60:
            self.StrengthLevelBoost = data['StrengthBoost']
        else:
            self.StrengthLevelBoost = 0
        if 0 <= data['RangedBoost'] <= 60:
            self.RangedLevelBoost = data['RangedBoost']
        else:
            self.RangedLevelBoost = 0
        if 0 <= data['MagicBoost'] <= 60:
            self.MagicLevelBoost = data['MagicBoost']
        else:
            self.MagicLevelBoost = 0

        self.StrengthPrayerBoost = data['StrengthPrayer']
        self.RangedPrayerBoost = data['RangedPrayer']
        self.MagicPrayerBoost = data['MagicPrayer']

        if 1 <= data['ShieldArmourValue'] <= 1000:
            self.ShieldArmourValue = data['ShieldArmourValue']
        else:
            self.ShieldArmourValue = 491                # Shield Armour Value

        if 1 <= data['DefenceLevel'] <= 160:
            self.DefenceLevel = data['DefenceLevel']
        else:
            self.DefenceLevel = 99                      # Defence Level

        self._BaseDamage = None
        self._BaseDamageEffective = None
        self._BashBaseDamage = None

        if 1 <= data['baseDamage'] <= 10000:
            self.userBaseDamage = data['baseDamage']
        else:
            # Change this into None if the Ability Damage from equipment needs to be calculated
            self.userBaseDamage = 1000  # Base weapon damage

    @property
    def BaseDamage(self):
        if self._BaseDamage is None:
            if self.userBaseDamage is None:
                damage_bonus_class = self.MainHand.Class + 'DamageBonus'
                b = 0  # Sum of all strength bonuses from armour and jewellery

                # Ring
                b += getattr(self.Ring, damage_bonus_class)

                if self.MainHand.Class == 'Melee':
                    S = self.StrengthLevel + self.StrengthLevelBoost  # Strength level

                    ab = self.Aura.Multiplier if self.Aura.Name == 'Berserker aura' and 'Berserk' not in self.BoostName else 1  # Berserker aura boost

                    dm = self.MainHand.Damage  # Main-hand damage

                    # Multiplier for main-hand
                    if self.MainHand.Speed == 'Average':
                        sm = 96 / 149
                    elif self.MainHand.Speed == 'Fast':
                        sm = 192 / 245
                    elif self.MainHand.Speed == 'Fastest':
                        sm = 1
                    else:
                        sm = 0

                    if self.MainHand.Slot != '2h':
                        do = self.OffHand.Damage

                        # Multiplier for off-hand
                        if self.OffHand.Speed == 'Average':
                            so = 96 / 149
                        elif self.OffHand.Speed == 'Fast':
                            so = 192 / 245
                        elif self.OffHand.Speed == 'Fastest':
                            so = 1
                        else:
                            so = 0
                    else:
                        do = 0
                        so = 0

                    self._BaseDamage = math.floor((3.75*S + (dm + do)*(sm + so) + 1.5*b) * ab)

                elif self.MainHand.Class == 'Range':
                    R = self.RangedLevel + self.RangedLevelBoost  # Range level

                    ab = self.Aura.Multiplier if self.Aura.Name == 'Reckless aura' and 'Death\'s Swiftness' not in self.BoostName else 1  # Reckless aura boost

                    tm = self.MainHand.Tier  # Main-hand tier

                    if self.MainHand.Slot != '2h':
                        to = self.OffHand.Tier  # Off-hand tier
                    else:
                        to = tm

                    da = 1500  # Damage of ammo

                    self._BaseDamage = math.floor((3.75*R + min(9.6*tm + 4.8*to, 1.5*da) + 1.5*b) * ab)

                elif self.MainHand.Class == 'Range':
                    M = self.MagicLevel + self.MagicLevelBoost  # Range level

                    ab = self.Aura.Multiplier if self.Aura.Name == 'Maniacal aura' and 'Sunshine' not in self.BoostName else 1  # Maniacal aura boost

                    tm = self.MainHand.Tier  # Main-hand tier
                    sm = 1500  # Damage off main-hand spell

                    if self.MainHand.Slot != '2h':
                        to = self.OffHand.Tier  # Off-hand tier
                        so = 750  # Damage off off-hand spell
                    else:
                        to = tm
                        so = sm

                    self._BaseDamage = math.floor((3.75*M + min(9.6*tm + 4.8*to, sm + 0.5*so) + 1.5*b) * ab)

                else:
                    self._BaseDamage = 13
            else:
                if self.Bar.Style == 'Melee':
                    ab = self.Aura.Multiplier if self.Aura.Name == 'Berserker aura' and 'Berserk' not in self.BoostName else 1  # Berserker aura boost
                elif self.Bar.Style == 'Ranged':
                    ab = self.Aura.Multiplier if self.Aura.Name == 'Reckless aura' and 'Death\'s Swiftness' not in self.BoostName else 1  # Reckless aura boost
                elif self.Bar.Style == 'Magic':
                    ab = self.Aura.Multiplier if self.Aura.Name == 'Maniacal aura' and 'Sunshine' not in self.BoostName else 1  # Maniacal aura boost
                elif self.Bar.Style == 'All' and self.Aura.Name in {'Berserker aura', 'Reckless aura', 'Maniacal aura'}:
                    ab = self.Aura.Multiplier
                else:
                    ab = 1

                self._BaseDamage = self.userBaseDamage * ab

        return self._BaseDamage

    @property
    def BaseDamageEffective(self):
        if self._BaseDamageEffective is None:
            if self.MainHand.Class == 'Melee':
                damage = self.BaseDamage * self.StrengthPrayerBoost
                damage += self.StrengthLevelBoost * 6
                damage *= self.getBoost()
            elif self.MainHand.Class == 'Range':
                damage = self.BaseDamage * self.RangedPrayerBoost
                damage += self.RangedLevelBoost * 6
                damage *= self.getBoost()
            elif self.MainHand.Class == 'Magic':
                damage = self.BaseDamage * self.MagicPrayerBoost
                damage += self.MagicLevelBoost * 6
                damage *= self.getBoost()
            else:
                damage = self.BaseDamage * max(self.StrengthPrayerBoost, self.RangedPrayerBoost, self.MagicPrayerBoost)
                damage += max(self.StrengthLevelBoost, self.RangedLevelBoost, self.MagicLevelBoost) * 6

            self._BaseDamageEffective = damage * self.BerserkersFury * (1 + self.Ruthless * 0.025)

        return self._BaseDamageEffective

    @property
    def BashBaseDamage(self):
        if self._BashBaseDamage is None:
            self._BashBaseDamage = self.BaseDamageEffective + self.DefenceLevel + self.ShieldArmourValue  # Base Damage for the Bash ability

        return self._BashBaseDamage

    def addSpecial(self, SpecialBook):

        specialNames = []

        # Aftershock
        if self.Aftershock:
            specialNames.append('Aftershock')

        # Pocket item
        if self.Pocket.Name != 'Pocket':
            specialNames.append(self.Pocket.Name)

        for name in specialNames:
            special = deepcopy(SpecialBook[name])
            special.Parent = self

            self.Logger.initAbility(special.Name)

            self.Special.update({special.Name: special})

    def TimerCheck(self, dummy, logger):
        """
        Checks the ability cooldowns, adrenaline buffs, boosts and channeling status.

        :param logger: The Logger object.
        """

        self.Bar.TimerCheck(logger)  # Ability cooldowns and Global Cooldown

        # If the player has an adrenaline buff going
        if self.CritAdrenalineBuffTime:
            self.CritAdrenalineBuffTime -= 1

            if not self.CritAdrenalineBuffTime:
                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player adrenaline gain buff has worn out</li>'

        # If the player used a channeled ability and its still active
        if self.ChanTime:
            self.ChanTime -= 1

            if not self.ChanTime:
                if self.GreaterChainTime:
                    self.resetGreaterChain()

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player is no longer performing a channeled ability</li>'

        # If the player has a boost going on
        if self.Boost:
            for i in range(len(self.BoostTime) - 1, -1, -1):
                if self.BoostTime[i] > 0:
                    self.BoostTime[i] -= 1

                    if self.BoostTime[i] == 0:
                        self._BaseDamage = None
                        self._BaseDamageEffective = None
                        # self._BashBaseDamage = None

                        self.BoostTime.pop(i)
                        self.BoostX.pop(i)

                        if logger.DebugMode:
                            logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player damage boost due to {self.BoostName[i]} has been reset</li>'

                        self.BoostName.pop(i)

            if not self.BoostX:
                self.Boost = False

        # If the player has a Greater Chain effect going on
        if self.GreaterChainTime:
            self.GreaterChainTime -= 1

            if not self.GreaterChainTime:
                self.resetGreaterChain()

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player Greater Chain effect has worn off</li>'

        # If the player has a Jas Buff effect going on
        if self.JasTime:
            self.JasTime -= 1

            if not self.JasTime:
                JasAbil = deepcopy(self.Special['Scripture of Jas'])

                JasAbil.Hits[0].setDamage(0.2 * self.JasDamage)

                dummy.PHits[dummy.nPH: dummy.nPH + JasAbil.nHits] = JasAbil.Hits
                dummy.nPH += JasAbil.nHits

                self.JasDamage = 0

        # If the player has a Gloves of Passage effect going on
        if self.GlovesOfPassageTime:
            self.GlovesOfPassageTime -= 1

            if not self.GlovesOfPassageTime:
                self.GlovesOfPassageBoost -= .2

                if logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player damage boost due to Gloves of Passage has been reset</li>'

        # Upgrade special abilities (option check)
        for name in self.Special.keys():
            special = self.Special[name]

            if special.cdTime:
                special.cdTime -= 1

                if not special.cdTime:
                    if logger.DebugMode:
                        logger.Text += f'<li style="color: {logger.TextColor["normal"]};">{special.Name} no longer on cd</li>'

        # # If the player has a Dragon Breath effect going on
        # if self.DragonBreathCombustTime:
        #     self.DragonBreathCombustTime -= 1
        #
        #     if self.DragonBreathCombustTime == 0:
        #         if logger.DebugMode:
        #             logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Player Dragon Breath (Kerapac\'s Wrist Wraps) effect has worn off</li>'

    def FireNextAbility(self, logger):
        """
        Checks if an ability is allowed to fire.

        :param player: The Player object
        :param logger: The Logger object
        """

        # Check for available ability
        for i, Ability in enumerate(self.Bar.Abilities):
            if not Ability.cdTime:

                AdrenalineCostReduction = 0

                if Ability.Type == 'Ultimate':
                    if self.ConservationOfEnergy:
                        AdrenalineCostReduction += 10

                    if self.Ring.Name == 'Ring of vigour' or self.RingOfVigourPassive:
                        AdrenalineCostReduction += 10

                    if self.Aura.Name in {'Invigorate aura',
                                          'Greater invigorate aura',
                                          'Master invigorate aura',
                                          'Supreme invigorate aura'}:
                        AdrenalineCostReduction += Ability.Parent.Aura.Multiplier * 100

                if self.Ultimatums and \
                        Ability.Name in {'Overpower', 'Frenzy', 'Unload', 'Omnipower'} and \
                        self.Cape.Name not in {'Igneous Kal-Ket', 'Igneous Kal-Xil', 'Igneous Kal-Mej', 'Igneous Kal-Zuk'} and \
                        self.Ultimatums * 5 > AdrenalineCostReduction:
                    AdrenalineCostReduction = self.Ultimatums * 5

                if Ability.Type == 'Basic' or Ability.Type == 'Threshold' and self.Adrenaline >= 50 or Ability.Type == 'Ultimate' and self.Adrenaline >= -1 * Ability.AdrenalineGain:
                    self.Adrenaline += Ability.AdrenalineGain + AdrenalineCostReduction

                    if self.Adrenaline > self.MaxAdrenaline:
                        self.Adrenaline = self.MaxAdrenaline

                    if logger.DebugMode:
                        logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Attack status: {Ability.Name} ready</li>'

                    return Ability  # Return because firing more than 1 ability wouldn't make sense

                else:
                    if logger.DebugMode:
                        logger.Text += f'<li style="color: {logger.TextColor["initialisation"]};">Not enough Adrenaline for {Ability.Name}</li>'

        return None

    def addBoost(self, ability):
        self._BaseDamage = None
        self._BaseDamageEffective = None
        self._BashBaseDamage = None

        self.Boost = True
        self.BoostX.append(ability.BoostX)
        self.BoostTime.append(ability.EffectDuration)
        self.BoostName.append(ability)

    def addBoost1(self, ability):
        self.Boost1 = True
        self.Boost1XAbility = ability

    def resetBoost1(self):
        self.Boost1 = False
        self.addBoost(self.Boost1XAbility)

    def getBoost(self):
        boost = 1

        for i, ability in enumerate(self.BoostName):
            if ability.Boost1:
                boost += self.BoostX[i]
            else:
                boost *= (self.BoostX[i] + 1)

        return boost

    def resetGreaterChain(self):
        self.GreaterChainTime = 0
        self.GreaterChainTargets = []