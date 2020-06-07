import numpy as np


# The AbilityBar class: Used for activating abilities
class AbilityBar:

    def __init__(self, opt, player, Do):
        self.GCDStatus = False      # When True, the ability bar is on a global cooldown
        self.GCDTime = 0            # Time before the global cooldown wears of
        self.GCDMax = 1.8           # Maximum time of a global cooldown
        self.Adrenaline = 100       # Amount of adrenaline that has been generated, starting with 100
        self.FireStatus = False     # When True, a chosen ability is allowed to be used
        self.FireN = None           # The index of the ability to be fired in the current tick
        self.Rotation = []          # Contains the abilities put on the bar
        self.N = 0                  # Amount of abilities on the bar
        self.AbilNames = []         # A list of names of abilities on the bar
        self.AbilEquipment = []     # A list of equipment allowed for using the abilities
        self.AbilStyles = []        # A list of ability styles
        self.Basic = 8              # Adrenaline generated by a basic ability
        self.Threshold = 15         # Adrenaline used for a threshold ability

        if player.RoV:  # If the user selected the Ring of Vigour option
            self.Ultimate = 90   # Adrenaline used for an ultimate ability

            if Do.HTMLwrite:
                Do.Text += f'<li style="color: {Do.init_color};">Behaviour change: Ult adrenaline cost reduced to 90</li>'
        else:
            self.Ultimate = 100  # Adrenaline used for an ultimate ability

        # Groups of abilities which share a cooldown
        self.SharedCDs = [
            ['Surge', 'Escape'],
            ['Forceful Backhand', 'Stomp', 'Tight Bindings', 'Rout', 'Deep Impact', 'Horror'],
            ['Backhand', 'Kick', 'Binding Shot', 'Demoralise', 'Impact', 'Shock'],
            ['Fragmentation Shot', 'Combust'],
            ['Metamorphosis', 'Sunshine'],
            ['Destroy', 'Hurricane']
        ]

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
            ['Lesser Concentrated Blast', 'Concentrated Blast'],
            ['Lesser Snipe', 'Snipe'],
            ['Lesser Fragmentation Shot', 'Fragmentation Shot'],
            ['Lesser Needle Strike', 'Needle Strike'],
            ['Lesser Dazing Shot', 'Dazing Shot', 'Greater Dazing Shot']
        ]

    # CHECK GLOBAL COOLDOWN STATUS
    def TimerCheck(self, Do):
        if self.GCDStatus:  # If the ability bar is on a global cooldown
            self.GCDTime -= .6  # Subtract tick time

            if self.GCDTime <= 0.01:  # If the GCD time reached zero
                self.GCDTime = 0
                self.GCDStatus = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.nor_color};">Global cooldown ended</li>\n'

    # CHECK IF AN ABILITY IS ALLOWED TO FIRE
    def AdrenalineStatus(self, Type):
        if Type == 'Basic':  # If type is Basic add 8 adrenaline to the ability bar
            self.Adrenaline += self.Basic

            if self.Adrenaline > 100:  # If the adrenaline is over 100, cap it to 100
                self.Adrenaline = 100

            self.FireStatus = True  # Allowed to fire

        # Elif type is Threshold and adrenaline is equal to or more than 50
        elif Type == 'Threshold' and self.Adrenaline >= 50:
            self.Adrenaline -= self.Threshold

            self.FireStatus = True  # Allowed to fire

        # Elif type is Ultimate and adrenaline is equal to 100
        elif Type == 'Ultimate' and self.Adrenaline == 100:
            self.Adrenaline -= self.Ultimate

            self.FireStatus = True  # Allowed to fire

        else:  # Else the ability is not allowed to fire whatsoever
            self.FireStatus = False  # Not allowed to fire

    # CHECK IF LINKED ABILITIES HAVE TO GO ON COOLDOWN OR NOT
    def SharedCooldowns(self, FireAbility, Do):
        for i in range(0, len(self.SharedCDs)):  # For all shared cooldown groups
            if FireAbility.Name in self.SharedCDs[i]:  # If the already fired ability is in such a group
                # Get the index of the ability in that specific list
                FireAbilityIDX = self.SharedCDs[i].index(FireAbility.Name)

                # Assign the complete list to a new variable
                shared_cooldown_list = self.SharedCDs[i].copy()

                # Pop the fired ability of the list
                shared_cooldown_list.pop(FireAbilityIDX)

                for j in range(0, len(shared_cooldown_list)):  # For every remaining ability in the list
                    if shared_cooldown_list[j] in self.AbilNames:  # If its currently on the ability bar
                        # Get its index on the ability bar
                        idx = self.AbilNames.index(shared_cooldown_list[j])

                        # Activate ability cooldown
                        self.Rotation[idx].cdStatus = True
                        self.Rotation[idx].cdTime = self.Rotation[idx].cdMax

                        if Do.HTMLwrite:
                            Do.Text += f'<li style="color: {Do.nor_color};">{self.Rotation[idx].Name} went on cooldown</li>\n'

                # Break when the ability was in a group and the cooldowns have been sorted
                # The ability will never occur in 2 groups (would not make sense)
                break