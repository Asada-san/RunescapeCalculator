import numpy as np


# The Dummy class: A dummy mimics a (stationary) monster
class Dummy:

    def __init__(self, opt, Do):
        self.Damage = 0                 # The amount of damage done - puncture damage
        self.PunctureDamage = 0         # The amount of puncture damage done
        self.Stun = False               # When True, the dummy is in a stunned state
        self.StunTime = 0               # Time before a stun wears of
        self.Bind = False               # When True, the dummy is in a bind state
        self.BindTime = 0               # Time before a bind wears of
        self.PH = False                 # When True, the dummy is affected by a Damage over Time ability
        self.DamageNames = []           # List of abilities which caused damage to the dummy in the current tick
        self.PHits = [0] * 50           # List of Pending Hits
        self.nPH = 0                    # Amount of Pending Hits
        self.nPuncture = 0              # Amount of puncture stacks on dummy

        ##############################################################
        ################# Set various user inputs ####################
        ##############################################################

        self.nTarget = int(opt['nTargets'])             # Number of targets
        self.Movement = not opt['movementStatus']       # True if the dummy can move
        self.StunBindImmune = opt['stunbindStatus']     # True if the dummy is Stun and Bind immune

        if Do.HTMLwrite:
            Do.Text += f'<li style="color: {Do.init_color};">User select: Stationary {self.Movement}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Stun&Bind Immune {self.StunBindImmune}</li>' \
                       f'<li style="color: {Do.init_color};">User select: Number of targets: {int(opt["nTargets"])}</li>'

    ##############################################################
    ################## Check for Stuns&Binds #####################
    ##############################################################

    def TimerCheck(self, Do):

        # If the dummy has been stunned
        if self.Stun:
            self.StunTime -= .6  # Subtract tick time

            # If the StunTime reached zero
            if self.StunTime <= 0.01:
                self.StunTime = 0
                self.Stun = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.stat_color};">Dummy no longer stunned</li>\n'

        # If the dummy has been bound
        if self.Bind:
            self.BindTime -= .6  # Subtract tick time

            # If the BindTime reached zero: set its status to False
            if self.BindTime <= 0.01:
                self.Bind = False

                if Do.HTMLwrite:
                    Do.Text += f'<li style="color: {Do.stat_color};">Dummy no longer bound</li>\n'
