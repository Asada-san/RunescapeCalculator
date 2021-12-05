let spreadsheet = '<a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/api/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>Spreadsheet</strong></a>'

    // {
    // version: '',
    // data: '',
    // items: [{
    //     header: '',
    //     subItems: [
    //
    //     ]}, {
    //     header: '',
    //     subItems: [
    //
    //     ]}
    // ]}

export var updateInfo = [{
    version: 'V2.01.0',
    date: '12-12-2021',
    items: [{
        header: 'Abilities:',
        subItems: [
            'Removed the following abilities which are not activated by revolution: Bladed Dive, Surge, Detonate, Escape, Balanced Strike',
            'Added the effects of Deadshot, Omnipower and Overpower when wearing a Igneous cape',
            '(Greater) Chain and (Greater) Ricochet secondary hits are now delayed by 1 tick',
            'Fourth puncture hit is now .1x its previous value',
            'Wild magic is now a channeled ability',
            'Added Magma Tempest --> even though it has varying damage for each hit, it is still seen as a bleed such that it will never crit'
        ]}, {
        header: 'Options:',
        subItems: [
            'Added the 3 Igneous capes from the Zuk fight and moved them under 1 option together with the strength cape as "Cape"',
            'Increased the maximum amount of dummies to 30 (up from 10)'
        ]}, {
        header: 'Calculations:',
        subItems: [
            'Damaging AoE hits are now calculated once instead of every time an AoE ability is activated',
            'Greater Chain effect now is applied to the correct targets',
            'Greater Chain effect is now applied as soon as the next ability after Greater Chain has been fired instead of when the damage actually occures on the target, simplifying shit a lot',
            'Damage done on secondary targets due to the Greater chain effect is now seen as Greater Chain damage instead of whatever the fired ability was'
        ]}, {
        header: 'Layout:',
        subItems: [
            'Text color of warning box when including an ability which is not fired by revolution is changed from white to black',
            'Decreased the width of the elements holding the abilities by 50 pixels'
        ]}, {
        header: spreadsheet + ':',
        subItems: [
            'Added Magma Tempest values',
            'Added MaxTargets column indicating the maximum amount of targets damaged by AoE abilities'
        ]}, {
        header: 'Charts (Note that these only show information about 1 cycle rotation):',
        subItems: [
            'Added the option to select charts in a dropdown menu',
            'Added a line chart showing the total damage over time',
            'Added a line chart showing total damage per ability over time',
            'Added a bar chart showing damage per tick over time'
        ]}, {
        header: 'Other:',
        subItems: [
            'Added a download data button on the result card with which .json file can be downloaded containing data resulting from the simulated fight'
        ]}
    ]}, {
    version: 'V2.00.1',
    date: '17-8-2021',
    items: [{
        header: 'Changes in line with the main game update on the 16th of August:',
        subItems: [
            'Greater Concentrated Blast: Decreased average damage for all 3 hits',
            'Greater Ricochet: Decreased average damage of extra hits due to caroming perk when inflicted on main target'
        ]}, {
        header: 'Other changes:',
        subItems: [
            'Spreadsheet links work once again'
        ]}
    ]}, {
    version: 'V2.00.0',
    date: '3-7-2021',
    items: [{
        header: 'General:',
        subItems: [
            'Restyled everything',
            'If a stall happens because all abilities were on cooldown, you will now be stalled for 3 consecutive ticks before attempting to fire an ability again',
            'Added Greater Concentrated Blast',
            'Improved code: check to determine hits that do damage in current tick is only performed once per tick'
        ]}, {
        header: spreadsheet + ':',
        subItems: [
            'Removed useless "delay" column and set values in BleedToMove column to 0 for channeled abilities'
        ]}
    ]}, {
    version: 'V1.06.1',
    date: '3-7-2021',
    items: [{
        header: 'Changes:',
        subItems: [
            'Greater Ricochet effect now works properly',
            'Bleeds now work properly when using Berserker/Maniacal/Reckless aura'
        ]}
    ]}, {
    version: 'V1.06.0',
    date: '27-6-2021',
    items: [{
        header: 'New ring options:',
        subItems: [
            'Channeler\'s ring',
            'Champion\'s ring',
            'Reaver\'s ring',
            'Stalker\'s ring'
        ]}, {
        header: 'General changes:',
        subItems: [
            'Wild Magic is no longer a channeling ability',
            'Asphyxiate now stuns',
            'Fixed several stun and/or bind durations in line with the updated ability tooltips ingame',
            'Added some more tooltips to the options',
            'Sped up and simplified the cycle searching algorithm',
            'Cleaned up other parts of the code making it faster and more readable',
            'Changed the way critical hit chance increases are handled due to ability/items',
            'Cleaned up the ' + spreadsheet + ' and the way its loaded',
            'Added SideTargetDam/SideTargetDamMin/SideTargetDamMax to spreadsheet instead of them being hardcoded'
        ]}
    ]}, {
    version: 'V1.05.7',
    date: '1-4-2021',
    items: [{
        header: '',
        subItems: [
            'Individual ability damage and redundant abilities are now tracked when setting a custom simulation time',
            'DPT calculation when setting a custom simulation time is now done properly',
            'Phased out the use of ticks within the code such that it is more efficient'
        ]}
    ]}, {
    version: 'V1.05.61',
    date: '31-3-2021',
    items: [{
        header: 'Changes:',
        subItems: [
            'Changed some "TrueEfficientWait" times in the ' + spreadsheet + ' to reflect the latest improvements to revolution',
            'Damage boosting aura\'s can once again be used'
        ]}
    ]}, {
    version: 'V1.05.6',
    date: '4-3-2021',
    items: [{
        header: 'Changes:',
        subItems: [
            'Added the ability name to the tooltip of the ability images',
            'Removed the options info section and instead added tooltips to the options',
            'Moved the options section for a slightly better user experience',
            'Fixed some formatting issues when clicking on the resulting output',
            'Greater Dazing Shot stack timer is now more accurate',
            'Salt the Wound can once again be used and now works properly when there is a boost active'
        ]}
    ]}, {
    version: 'V1.05.5',
    date: '25-1-2021',
    items: [{
        header: 'Changes:',
        subItems: [
            'Sunshine and Death Swiftness duration is no longer infinite when using Planted Feet',
            'Changed some efficient wait times (used when using the \'efficient\' option)',
            'Greater Chain now works correctly with channeled abilities'
        ]}
    ]}, {
    version: 'V1.05.4',
    date: '22-1-2021',
    items: [{
        header: 'Changes:',
        subItems: [
            'Simulation counter now hopefully works properly',
            'Ring of Vigour and Conservation of Energy now stack',
            'Added the Ultimatums and Impatient perks',
            'linking to wiki (CTRL+left click on image) now takes precedence over adding it to the bar',
            'Block of information when clicking on AADPT number now stays open when running another simulation (click on AADPT number again to close it)'
        ]}
    ]}, {
    version: 'V1.05.3',
    date: '21-12-2020',
    items: [{
        header: 'Changes:',
        subItems: [
            'Added a counter'
        ]}
    ]}, {
    version: 'V1.05.2',
    date: '14-12-2020',
    items: [{
        header: 'Changes:',
        subItems: [
            'Added Greater Chain and Greater Ricochet',
            'Fixed an issue with Wild Magic',
            'Set Dragon Breath target cap to 4 and increased its adrenaline gain to 10 when it hits 2 or more targets'
        ]}
    ]}, {
    version: 'V1.05.1',
    date: '18-10-2020',
    items: [{
        header: 'Changes:',
        subItems: [
            'Added the Devotion ability'
        ]}
    ]}, {
    version: 'V1.05.0',
    date: '11-8-2020',
    items: [{
        header: 'Changes:',
        subItems: [
            'Left clicking on abilities in their respective sections now puts them in the first available slot on the bar',
            'Left clicking + CTRL now links to the ability\'s wiki page',
            'Added a new ability info table which can be seen when clicked on the resulting AADPT number',
            'Added the Archaeology relics: Heightened Senses, Fury of the Small, Conservation of Energy and Berserker\'s Fury',
            'Added Perks: Shield Bashing',
            'Fixed an issue where bleed abilities would be nulled when using the Planted Feet perk',
            'Limited AoE abilities to be able to damage max 9 targets except for corruption shot & blast',
            'Changed seconds to ticks within the code for clarity'
        ]}
    ]}, {
    version: 'V1.04.0',
    date: '',
    items: [{
        header: 'Changes:',
        subItems: [
            'Added Caroming, Ruthless (as a flat damage bonus) and Reflexes perk',
            'Increased maximum amount of targets to 10',
            'Added Freedom and Anticipation abilities',
            'Fixed an issue where planted feet wasn\'t working'
        ]}
    ]}, {
    version: 'V1.03.1',
    date: '',
    items: [{
        header: '',
        subItems: [
            'Cleaned out/changed/created several directories',
            'Added Hurricane + Destroy to the shared ability cooldown list',
            'Fixed an issue where certain abilities would be on cooldown indefinitely'
        ]}
    ]}, {
    version: 'V1.03.0',
    date: '',
    items: [{
        header: '',
        subItems: [
            'All average ability damages are now calculated properly within the code instead of reading values from an excel sheet',
            'Added Precise, Equilibrium, Biting, Flanking and Lunging perks',
            'Moved the options block and increased its size',
            'Rewrote code so all player equipment related options are now assigned to the player object instead of them being all over the place',
            'Added Concentrated Blast, Fury and Greater Fury effects related to critical hits',
            'Added a fourth condition for the cycle finder: Forced critical hit boost has to be equal too',
            'Added Meteor Strike, Sunshine and Incendiary adrenaline boosting effect due to crits --- might be wonky',
            'Added the aftershock perk and therefore also added the base damage back, and this time properly!',
            'Added level 20 gear option and Erethdor\'s Grimoire',
            'Added 2 defensive abilities: Debilitate and Bash',
            'Base Ability Damage Boosts are now applied properly and in the right place',
            'Added Equilibrium aura and made the average hit calculator more accurate',
            'Widened certain blocks',
            'Added Berserker, Maniacal and Reckless aura\'s',
            'Added Damage boosts from level increasing boosts like the aura\'s above or potions',
            'Added Prayer boosts',
            'Added print more info button in options for python script',
            'Rewrote code resulting in a slight decrease in python script runtime but increasing the readability of the script',
            'Made it so ability info is read from excel only once upon startup instead of every time the FIGHT! button is pressed resulting in a significant decrease in execution time, especially for bars with small cycle times',
            'Moved host from DigitalOcean (paid) to Heroku (free)',
            'Added Options Info section'
        ]}
    ]}, {
    version: 'V1.02.x and earlier not available',
    date: '',
    items: [

    ]}
]