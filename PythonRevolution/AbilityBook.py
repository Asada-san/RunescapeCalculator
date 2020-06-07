import PythonRevolution.Objects.Ability as Ability
import pandas as pd

##############################################################
################ Create ability objects once #################
##############################################################

# Get table from excel file WITH ALL ABILITY INFORMATION
tab_excel = pd.read_excel('PythonRevolution/AbilityInfo.xlsx')
rows, columns = tab_excel.shape  # Shape of excel table

AbilityBook = {}
rowIDX = 0
nTables = 6  # There are 6 tables each corresponding to a different cb skill

# For every table in the excel file
for i in range(0, nTables):

    # Store the name and the corresponding row in a dict
    while rowIDX <= rows - 1 and str(tab_excel.iloc[rowIDX][0]) != 'nan':

        # Create the ability object
        ability = Ability.Ability(tab_excel.iloc[rowIDX])

        AbilityBook.update({ability.Name: ability})

        rowIDX += 1

    rowIDX += 2  # Skip NaN row and headers
