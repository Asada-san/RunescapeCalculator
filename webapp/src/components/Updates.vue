<script>
export var updateInfo = [{
    version: 'V2.00.1 - 17-8-2021',
    items: [{
      header: 'Changes in line with the main game update on the 16th of August:',
      subItems: [
        'Greater Concentrated Blast: Decreased average damage for all 3 hits',
        'Greater Ricochet: Decreased average damage of extra hits due to caroming perk when inflicted on main target'
      ]}, {
      header: 'Other changes:',
      subItems: [
        'Spreadsheet links work once again'
      ]
    }]
}]



// <div id="update16">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V2.00.1 - 17-8-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Changes in line with the main game update on the 16th of August:
//   <ul>
//     <li>Greater Concentrated Blast: Decreased average damage for all 3 hits</li>
//     <li>Greater Ricochet: Decreased average damage of extra hits due to caroming perk when inflicted on main target</li>
//   </ul>
// </li>
// <li>Spreadsheet links work once again</li>
// </ul>
// </div>

// <div id="update15" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V2.00.0 - 9-8-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Restyled everything</li>
// <li>If a stall happens because all abilities were on cooldown, you will now be stalled for 3 consecutive ticks before attempting to fire an ability again</li>
// <li>Added Greater Concentrated Blast</li>
// <li>Improved code: check to determine hits that do damage in current tick is only performed once per tick</li>
// <li><a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/api/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a>:
//   Removed useless "delay" column and set values in BleedToMove column to 0 for channeled abilities</li>
// </ul>
// </div>
//
// <div id="update14" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.06.1 - 3-7-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Greater Ricochet effect now works properly</li>
// <li>Bleeds now work properly when using Berserker/Maniacal/Reckless aura</li>
// </ul>
// </div>
//
// <div id="update13" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.06.0 - 27-6-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added the following options:
//   <ul>
//     <li>Channeler's ring</li>
//     <li>Champion's ring</li>
//     <li>Reaver's ring</li>
//     <li>Stalker's ring</li>
//   </ul>
// </li>
// <li>Wild Magic is no longer a channeling ability</li>
// <li>Asphyxiate now stuns</li>
// <li>Fixed several stun and/or bind durations in line with the updated ability tooltips ingame</li>
// <li>Added some more tooltips to the options</li>
// <li>Sped up and simplified the cycle searching algorithm</li>
// <li>Cleaned up other parts of the code making it faster and more readable</li>
// <li>Changed the way critical hit chance increases are handled due to ability/items</li>
// <li>Cleaned up the <a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/api/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a> and the way its loaded</li>
// <li>Added SideTargetDam/SideTargetDamMin/SideTargetDamMax to spreadsheet instead of them being hardcoded</li>
// </ul>
// </div>
//
// <div id="update12" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.7 - 1-4-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Individual ability damage and redundant abilities are now tracked when setting a custom simulation time</li>
// <li>DPT calculation when setting a custom simulation time is now done properly</li>
// <li>Phased out the use of ticks within the code such that it is more efficient</li>
// </ul>
// </div>
//
// <div id="update11" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.61 - 31-3-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Changed some "TrueEfficientWait" times in the spreadsheet to reflect the latest improvements to revolution</li>
// <li>Damage boosting aura's can once again be used</li>
// </ul>
// </div>
//
// <div id="update10" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.6 - 4-3-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added the ability name to the tooltip of the ability images</li>
// <li>Removed the options info section and instead added tooltips to the options</li>
// <li>Moved the options section for a slightly better user experience</li>
// <li>Fixed some formatting issues when clicking on the resulting output</li>
// <li>Greater Dazing Shot stack timer is now more accurate</li>
// <li>Salt the Wound can once again be used and now works properly when there is a boost active</li>
// </ul>
// </div>
//
// <div id="update9" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.5 - 25-1-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Sunshine and Death Swiftness duration is no longer infinite when using Planted Feet</li>
// <li>Changed some efficient wait times (used when using the 'efficient' option) </li>
// <li>Greater Chain now works correctly with channeled abilities</li>
// </ul>
// </div>
//
// <div id="update8" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.4 - 22-1-2021</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Simulation counter now hopefully works properly</li>
// <li>Ring of Vigour and Conservation of Energy now stack</li>
// <li>Added the Ultimatums and Impatient perks</li>
// <li>linking to wiki (CTRL+left click on image) now takes precedence over adding it to the bar</li>
// <li>Block of information when clicking on AADPT number now stays open when running another simulation (click on AADPT number again to close it)</li>
// </ul>
// </div>
//
// <div id="update7" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.3 - 21-12-2020</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added a counter</li>
// </ul>
// </div>
//
// <div id="update6" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.2 - 14-12-2020</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added Greater Chain and Greater Ricochet</li>
// <li>Fixed an issue with Wild Magic</li>
// <li>Set Dragon Breath target cap to 4 and increased its adrenaline gain to 10 when it hits 2 or more targets</li>
// </ul>
// </div>
//
// <div id="update5" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.1 - 18-10-2020</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added the Devotion ability</li>
// </ul>
// </div>
//
// <div id="update4" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.0 - 11-8-2020</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Left clicking on abilities in their respective sections now puts them in the first
//   available slot on the bar</li>
// <li>Left clicking + CTRL now links to the ability's wiki page</li>
// <li>Added a new ability info table which can be seen when clicked on the resulting AADPT number</li>
// <li>Added the Archaeology relics: Heightened Senses, Fury of the Small, Conservation of
//   Energy and Berserker's Fury</li>
// <li>Added Perks: Shield Bashing</li>
// <li>Fixed an issue where bleed abilities would be nulled when using the Planted Feet perk</li>
// <li>Limited AoE abilities to be able to damage max 9 targets except for corruption shot&blast</li>
// <li>Changed seconds to ticks within the code for clarity</li>
// </ul>
// </div>
//
// <div id="update3" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.04.0</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Added Caroming, Ruthless (as a flat damage bonus) and Reflexes perk</li>
// <li>Increased maximum amount of targets to 10</li>
// <li>Added Freedom and Anticipation abilities</li>
// <li>Fixed an issue where planted feet wasn't working</li>
// </ul>
// </div>
//
// <div id="update2" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.03.1</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>Cleaned out/changed/created several directories</li>
// <li>Added Hurricane + Destroy to the shared ability cooldown list</li>
// <li>Fixed an issue where certain abilities would be on cooldown indefinitely</li>
// </ul>
// </div>
//
// <div id="update1" style="display: none;">
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.03.0</strong></p>
// <ul style="margin-top: 10px; margin-right: 15px;">
// <li>All average ability damages are now calculated properly within the code instead of reading
//   values from an excel sheet</li>
// <li>Added Precise, Equilibrium, Biting, Flanking and Lunging perks</li>
// <li>Moved the options block and increased its size</li>
// <li>Rewrote code so all player equipment related options are now assigned to the player object instead of them
//   being all over the place</li>
// <li>Added Concentrated Blast, Fury and Greater Fury effects related to critical hits</li>
// <li>Added a fourth condition for the cycle finder: Forced critical hit boost has to be equal too</li>
// <li>Added Meteor Strike, Sunshine and Incendiary adrenaline boosting effect due to crits --- might be wonky</li>
// <li>Added the aftershock perk and therefore also added the base damage back, and this time properly!</li>
// <li>Added level 20 gear option and Erethdor's Grimoire</li>
// <li>Added 2 defensive abilities: Debilitate and Bash</li>
// <li>Base Ability Damage Boosts are now applied properly and in the right place</li>
// <li>Added Equilibrium aura and made the average hit calculator more accurate</li>
// <li>Widened certain blocks</li>
// <li>Added Berserker, Maniacal and Reckless aura's</li>
// <li>Added Damage boosts from level increasing boosts like the aura's above or potions</li>
// <li>Added Prayer boosts</li>
// <li>Added print more info button in options for python script</li>
// <li>Rewrote code resulting in a slight decrease in python script runtime but increasing the readability of the
//   script</li>
// <li>Made it so ability info is read from excel only once upon startup instead of every time the FIGHT! button is
//   pressed resulting in a significant decrease in execution time, especially for bars with
//   small cycle times</li>
// <li>Moved host from DigitalOcean (paid) to Heroku (free)</li>
// <li>Added Options Info section</li>
// </ul>
//
// <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.02.x and earlier not available</strong></p>

</script>

<style scoped>

</style>