from App.PythonRevolution.Objects.Ability import Ability
from App.PythonRevolution.Objects.Gear import Item
# from App.PythonRotation.Objects import Ability as RotationAbility
import pandas as pd

##############################################################
################ Create ability objects once #################
##############################################################

# Get table from excel file WITH ALL ABILITY INFORMATION
xls = pd.ExcelFile('api/ItemInfo.xlsx')

Gear = {}
NameList = {}

sheets = ['Main-hand', 'Off-hand', 'Pocket', 'Aura', 'Cape', 'Ammo', 'Ring', 'Gloves']
for sheet in sheets:
    items = pd.read_excel(xls, sheet).to_dict(orient='records')

    Gear.update({
        sheet: {}
    })

    NameList.update({
        sheet: []
    })

    for k in range(len(items)):
        Gear[sheet].update({
            items[k]['Name']: Item(items[k])
        })

        if items[k]['Name'] != sheet:
            NameList[sheet].append(items[k]['Name'])

Abilities = {}

abilities = pd.read_excel(xls, 'Ability').to_dict(orient='records')

for k in range(len(abilities)):
    Abilities.update({
        abilities[k]['Name']: Ability(abilities[k])
    })

Special = {}

special = pd.read_excel(xls, 'Special').to_dict(orient='records')

for k in range(len(special)):
    Special.update({
        special[k]['Name']: Ability(special[k])
    })

Objects = {
    'Abilities': Abilities,
    'Special': Special,
    'Gear': Gear
}