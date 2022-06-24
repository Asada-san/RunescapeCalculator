class Settings:
    """
    The Loop object. Used for finding repeating cycles in the simulation loop.
    """

    def __init__(self, userInput):

        self.run = True  # True if we want to keep the while loop running
        self.Debug = userInput['Debug']  # When True, lots of info is printed to the HTML file
        # self.Debug = True

        # Check user input for a possible value for simulation time and starting adrenaline
        if 1 <= userInput['simulationTime'] <= 3600:
            self.FindCycle = False
            self.nMax = round(userInput['simulationTime'] / .6, 0)
        else:
            self.FindCycle = True  # True if we want to find a cycle
            self.nMax = 6000  # Max amount of ticks to run the while loop for
