import numpy as np
import os


class DoList:
    """
    The DoList object. Used for printing text in HTML used for debugging.
    """

    def __init__(self, opt):
        self.HTMLwrite = opt['HTMLwrite']   # When True, lots of info is printed to the HTML file
        self.Text = ''                      # String containing text to be printed in HTML page
        self.imp_color = 'red'              # Red color for important messages
        self.att_color = 'yellow'           # Yellow color for Ability activation and adrenaline
        self.loop_color = '#4CAF50'         # Green-ish color for loop total damage/time information
        self.dam_color = 'orange'           # Orange color for ability damage
        self.nor_color = '#D0D0D0'          # White-ish color for less important info
        self.init_color = '#707070'         # Dark white color for user select options
        self.start_color = '#FF00FB'        # Purple/Pink color for starting the revolution loop
        self.stat_color = '#00868F'         # Dark green-ish color for dummy stat changes
        self.cycle_color = '#00C7CD'        # Cyan color for cycle related stuff
        self.TypeDict = {                   # Dict for ability type
            1: 'standard',
            2: 'channel',
            3: 'bleed',
            4: 'puncture',
            5: 'standard Stun/Bind',
            6: 'side target',
            7: 'greater ricochet effect',
            8: 'greater chain effect'
        }


class Loop:
    """
    The Loop object. Used for finding repeating cycles in the simulation loop.
    """

    def __init__(self):
        self.SimulationTime = 0         # Runtime of the while loop
        self.n = 0                      # Number of ticks in the while loop
        self.nCheck = 0                 # Number of ticks after a cycle has been found
        # Array consisting of boolean values, a value is true if an ability corresponding to the
        # same idx of the bar has been fired
        self.nFA = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.bool)
        self.cdTimes = np.empty(14, dtype=np.float)     # Array consisting of cd times of all abilities
        self.runLoop = True             # True if we want to keep the while loop running
        self.Rotation = []              # Array containing the cycle rotation
        self.CycleTime = 0              # Cycle time
        self.CycleDamage = 0            # Damage done during 1 cycle time - puncture damage
        self.CyclePunctureDamage = 0    # Puncture damage done during 1 cycle time
        self.CycleFound = False         # True if a cycle has been found
        self.Cycle1More = 0             # Starts at t = CycleTime and when it runs out, runLoop is set to False
        self.ConditionList = []         # List containing 3 condition to be satisfied
        self.Redundant = []             # Array containing abilities which are not used in the cycle
        self.CycleLoopTime = 0          # Current time in when simulating the extra cycle
        self.CycleStart = 0             # Starting time of the extra cycle
        self.nStall = 0                 # Number of consecutive stalls
        self.CycleConvergenceTime = 0   # The convergence time to the cycle
        self.FindCycle = True           # True if we want to find a cycle
        self.nMax = 6000                # Max amount of ticks to run the while loop for
        self.nAC = 0                    # Number of times the loop has initiated an attack cycle
