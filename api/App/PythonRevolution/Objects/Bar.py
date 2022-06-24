from copy import deepcopy


class Bar:
    """
    The AbilityBar class containing all the properties the Ability Bar has in RuneScape.
    """

    def __init__(self, parent):
        self.Parent = parent

        self.GCDTime = 0  # Time before the global cooldown wears of
        self.GCDMax = 3  # Maximum time of a global cooldown
        self.Abilities = []  # Contains the abilities put on the bar

        self.AbilNames = []
        self.AbilStyles = []
        self.AbilEquipment = []
        self.AbilTypes = []

        self.Style = ''

        self.CritIncreaseNextAbility = 0

        # Groups of abilities which share a cooldown
        self.SharedCDs = [
            ['Surge', 'Escape'],
            ['Forceful Backhand', 'Stomp', 'Tight Bindings', 'Rout', 'Deep Impact',
             'Horror'],
            ['Backhand', 'Kick', 'Binding Shot', 'Demoralise', 'Impact', 'Shock'],
            ['Fragmentation Shot', 'Combust'],
            ['Metamorphosis', 'Sunshine'],
            ['Destroy', 'Hurricane']
        ]

        if self.Parent.MainHand.Name == 'Dark shard of Leng' and self.Parent.OffHand.Name == 'Dark sliver of Leng':
            self.SharedCDs.pop(self.SharedCDs.index(['Destroy', 'Hurricane']))

        # Groups of abilities which cannot appear together on the ability bar
        self.Invalid = [
            ['Lesser Smash', 'Smash'],
            ['Lesser Havoc', 'Havoc'],
            ['Lesser Sever', 'Sever'],
            ['Lesser Dismember', 'Dismember'],
            ['Fury', 'Greater Fury'],
            ['Barge', 'Greater Barge'],
            ['Flurry', 'Greater Flurry'],
            ['Lesser Combust', 'Combust'],
            ['Lesser Dragon Breath', 'Dragon Breath'],
            ['Lesser Sonic Wave', 'Sonic Wave'],
            ['Lesser Concentrated Blast', 'Concentrated Blast',
             'Greater Concentrated Blast'],
            ['Lesser Snipe', 'Snipe'],
            ['Lesser Fragmentation Shot', 'Fragmentation Shot'],
            ['Lesser Needle Strike', 'Needle Strike'],
            ['Lesser Dazing Shot', 'Dazing Shot', 'Greater Dazing Shot'],
            ['Ricochet', 'Greater Ricochet'],
            ['Chain', 'Greater Chain'],
        ]

    def addAbilities(self, rotation, AbilityBook):
        # Check user ability bar input
        if len(rotation) == 0:
            raise Exception(f'0 abilities in rotation, please select at least 1 basic ability')

        for i, name in enumerate(rotation):
            Ability = deepcopy(AbilityBook[name])
            Ability.Parent = self.Parent

            self.Parent.Logger.initAbility(Ability.Name)

            self.Abilities.append(Ability)

        for ability in self.Abilities:
            self.AbilNames.append(ability.Name)
            self.AbilStyles.append(ability.Style)
            self.AbilTypes.append(ability.Type)

        # Check ability compatibility according to cb style
        magicStyle = rangedStyle = meleeStyle = False
        for style in self.AbilStyles:
            if style in {'Magic'}:
                magicStyle = True
            elif style in {'Ranged'}:
                rangedStyle = True
            elif style in {'Strength', 'Attack'}:
                meleeStyle = True

        if sum([magicStyle, rangedStyle, meleeStyle]) > 1:
            raise Exception(
                f'The ability bar consists of abilities of varying combat styles')
        elif meleeStyle:
            self.Style = 'Melee'
        elif rangedStyle:
            self.Style = 'Ranged'
        elif magicStyle:
            self.Style = 'Magic'
        else:
            self.Style = 'All'

        for group in self.SharedCDs:
            idxGroup = []
            for ability in group:

                if ability in self.AbilNames:
                    idxGroup.append(self.AbilNames.index(ability))

            if len(idxGroup) > 1:
                # Link cooldown attribute
                for idx in idxGroup:
                    for idxToAdd in idxGroup:
                        if idxToAdd != idx:
                            self.Abilities[idx].SharedCooldownAbilities.append(self.Abilities[idxToAdd])

    def validate(self):
        if 'Basic' not in self.AbilTypes:
            raise Exception(f'A revolution bar needs at least 1 basic ability to work')

        # Check for duplicates and nonallowables
        for i, name1 in enumerate(self.AbilNames):  # range(len(AbilNames)):
            InvalidIDX = None

            for j in range(len(self.Invalid)):
                if name1 in self.Invalid[j]:
                    InvalidIDX = j
                    break

            for j, name2 in enumerate(self.AbilNames):  # Compare it with all other abilities
                if j == i:  # (same ability --> meaningless)
                    continue

                # USE THIS CODE IF USER IS ALLOWED TO PUT IN DUPLICATE ABILITIES
                # if bar.Rotation[i].Name == bar.Rotation[j].Name:
                #     error = True
                #     error_mes = f'{bar.Rotation[i].Name} has multiple appearances on the ability bar'
                #
                #     return error, error_mes, warning

                # If ability j also in disallowed group with idx DisallowedIDX, return error
                if InvalidIDX is not None and name2 in self.Invalid[InvalidIDX]:
                    raise Exception(f'{name1} and {name2} cannot appear together')

        for ability in self.Abilities:
            self.AbilEquipment.append(ability.Equipment)

        # Check ability compatibility according to equipment
        if not self.Parent.Switcher:
            if all(equipment in self.AbilEquipment for equipment in ['2h', 'dual', 'shield']):
                raise Exception(f'The ability bar consists of 2h, dual and shield abilities')
            elif all(equipment in self.AbilEquipment for equipment in ['2h', 'dual']):
                raise Exception(f'The ability bar consists of 2h and dual abilities')
            elif all(equipment in self.AbilEquipment for equipment in ['2h', 'shield']):
                raise Exception(f'The ability bar consists of 2h and shield abilities')
            elif all(equipment in self.AbilEquipment for equipment in ['shield', 'dual']):
                raise Exception(f'The ability bar consists of shield and dual abilities')

    def putOnGlobalCooldown(self):
        self.GCDTime = self.GCDMax

    def TimerCheck(self, logger):
        """
        Checks the global cooldown status.

        :param logger: The Logger object
        """

        if self.GCDTime:
            self.GCDTime -= 1

            if not self.GCDTime:
                if self.Parent.Logger.DebugMode:
                    logger.Text += f'<li style="color: {logger.TextColor["normal"]};">Global cooldown ended</li>'

        # For all abilities currently on cooldown
        for Ability in self.Abilities:

            if Ability.cdTime:
                Ability.cdTime -= 1

                if not Ability.cdTime:
                    if self.Parent.Logger.DebugMode:
                        logger.Text += f'<li style="color: {logger.TextColor["normal"]};">{Ability.Name} no longer on cd</li>'
