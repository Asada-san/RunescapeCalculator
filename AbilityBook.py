from PythonRevolution.Objects import Ability
import pandas as pd

##############################################################
################ Create ability objects once #################
##############################################################

# Get table from excel file WITH ALL ABILITY INFORMATION
tab_excel = pd.read_excel('AbilityInfo.xlsx')
rows, columns = tab_excel.shape  # Shape of excel table

AbilityBook = {}
rowIDX = 0
nTables = 6  # There are 6 tables each corresponding to a different cb skill

for i in range(0, nTables):
    # Store the name and the corresponding row in a dict
    while rowIDX <= rows - 1 and str(tab_excel.iloc[rowIDX][0]) != 'nan':
        ability = Ability.Ability(tab_excel.iloc[rowIDX])  # Create the ability object
        AbilityBook.update({ability.Name: ability})
        rowIDX += 1

    rowIDX += 2  # Skip NaN row and headers
