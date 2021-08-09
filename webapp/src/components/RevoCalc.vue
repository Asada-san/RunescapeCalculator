<template>
  <div :style="centerStyle">
    <div class="accordion" role="tablist">
      <b-card no-body class="mb-1" id="card-header" bg-variant="dark" text-variant="white" style="text-align: left;">
        <h2 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Revolution Bar <span style="font-size:small;">V2.00.0</span></h2>
<!--        <p style="text-align: center; margin-left: 15px; margin-right: 15px; color: pink;">If something doesn't work please contact me on Discord:-->
<!--            <strong style="color: #4CAF50">Micky#5858</strong>, Reddit:-->
<!--            <a style="color: #4CAF50" href="https://www.reddit.com/user/ftwmickywtf"><strong>u/FTWmickyWTF</strong></a>-->
<!--            or ingame: <a style="color: #4CAF50" href="https://apps.runescape.com/runemetrics/app/overview/player/asada-san"><strong>Asada-san</strong></a>.-->
<!--        </p>-->

        <b-card no-body class="mb-0" bg-variant="dark" text-variant="white" >
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button-group class="accordion-button-group">
              <b-button v-b-toggle.accordion-1 class="accordion-button" variant="secondary">General Info</b-button>
              <b-button v-b-toggle.accordion-2 class="accordion-button" variant="secondary">Important Notes</b-button>
              <b-button v-b-toggle.accordion-3 class="accordion-button" variant="secondary">Changelog</b-button>
            </b-button-group>
          </b-card-header>
          <b-collapse id="accordion-1" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text>
                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;">
                  Look through the combat sections for the abilities you want to put on the bar. If you want more information
                  about a certain ability, hold CTRL and click on it, this will open its RS3 wiki page in a new window. <br><br>

                  Constructing the revolution bar is as simple as:</p>
                  <ul>
                    <li>Clicking on abilities to make them appear in the first available slot on the bar.</li>
                    <li>Dragging them onto a slot.</li>
                    <li>Left clicking on an ability on the bar removes it.</li>
                    <li>The "clear bar" button removes all abilities from the bar.</li>
                    <li>Switching abilities on the bar can be done by dragging and dropping.</li>
                  </ul>
                <p style="margin-left: 15px; margin-right: 15px;">
                  Also, have a look at the options section for perks, boosts and much more.<br><br>

                  When you've set up your desired bar with the proper options, you should click on the FIGHT! button. A fight between a player and
                  a dummy will now be simulated resulting in an Average Ability Damage Per Tick (AADPT) output (in both a number and a percentage
                  of the base ability damage as calculated
                  <a href="https://runescape.wiki/w/Ability_damage#Calculating_ability_damage" target="_blank" style="color: #4CAF50"><strong>on the rs3 wiki</strong></a>).
                  Clicking on the result card will allow you to view some more interesting information.<br><br>

                  If anything is wrong or if you have any suggestions please let me know by contacting me on either
                  Discord: <strong style="color: #4CAF50">Micky#5858</strong>, Reddit: <a style="color: #4CAF50" href="https://www.reddit.com/user/ftwmickywtf"><strong>u/FTWmickyWTF</strong></a> or ingame:
                  <a style="color: #4CAF50" href="https://apps.runescape.com/runemetrics/app/overview/player/asada-san"><strong>Asada-san</strong></a>.
                </p>
              </b-card-text>
            </b-card-body>
          </b-collapse>

          <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li style="color: red;">The more damage boosting options are used, the more probable it is that the output damage is wrong due to orders in which
                  these are applied. If you notice any errors, please let me know! (see general info for places to contact me)</li>
                  <li>Average ability damages are used for the calculating the AADPT.</li>
                  <li>Tuska's Wrath does its normal damage only. When fighting slayer creatures, please
                  don't let revolution activate this ability, but instead activate it manually once every
                  2 minutes.</li>
                  <li>As the resulting A ... Ability ... DPT suggests, auto attacks are not taken into account.</li>
                  <li>All ability information used to determine the AADPT is summarized on a <a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a>.</li>
                  <li>The code (including html, js, css and python files) have been uploaded to <a href="https://github.com/Asada-san/RunescapeCalculator" target="_blank" style="color: #4CAF50"><strong>Github</strong></a>. You're free to use it however you want.</li>
                  <li>All ability images were yoinked from the RS3 wiki.</li>
                </ul>
              </b-card-text>
            </b-card-body>
          </b-collapse>

          <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text>
                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V2.00.0 - 9-8-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Restyled everything</li>
                  <li>If a stall happens because all abilities were on cooldown, you will now be stalled for 3 consecutive ticks before attempting to fire an ability again</li>
                  <li>Added Greater Concentrated Blast</li>
                  <li>Improved code: check to determine hits that do damage in current tick is only performed once per tick</li>
                  <li><a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a>:
                    Removed useless "delay" column and set values in BleedToMove column to 0 for channeled abilities</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.06.1 - 3-7-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Greater Ricochet effect now works properly</li>
                  <li>Bleeds now work properly when using Berserker/Maniacal/Reckless aura</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.06.0 - 27-6-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added the following options:
                    <ul>
                      <li>Channeler's ring</li>
                      <li>Champion's ring</li>
                      <li>Reaver's ring</li>
                      <li>Stalker's ring</li>
                    </ul>
                  </li>
                  <li>Wild Magic is no longer a channeling ability</li>
                  <li>Asphyxiate now stuns</li>
                  <li>Fixed several stun and/or bind durations in line with the updated ability tooltips ingame</li>
                  <li>Added some more tooltips to the options</li>
                  <li>Sped up and simplified the cycle searching algorithm</li>
                  <li>Cleaned up other parts of the code making it faster and more readable</li>
                  <li>Changed the way critical hit chance increases are handled due to ability/items</li>
                  <li>Cleaned up the <a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a> and the way its loaded</li>
                  <li>Added SideTargetDam/SideTargetDamMin/SideTargetDamMax to spreadsheet instead of them being hardcoded</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.7 - 1-4-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Individual ability damage and redundant abilities are now tracked when setting a custom simulation time</li>
                  <li>DPT calculation when setting a custom simulation time is now done properly</li>
                  <li>Phased out the use of ticks within the code such that it is more efficient</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.61 - 31-3-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Changed some "TrueEfficientWait" times in the spreadsheet to reflect the latest improvements to revolution</li>
                  <li>Damage boosting aura's can once again be used</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.6 - 4-3-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added the ability name to the tooltip of the ability images</li>
                  <li>Removed the options info section and instead added tooltips to the options</li>
                  <li>Moved the options section for a slightly better user experience</li>
                  <li>Fixed some formatting issues when clicking on the resulting output</li>
                  <li>Greater Dazing Shot stack timer is now more accurate</li>
                  <li>Salt the Wound can once again be used and now works properly when there is a boost active</li>
                </ul>

                <!-- ><p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.5 - 25-1-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Sunshine and Death Swiftness duration is no longer infinite when using Planted Feet</li>
                  <li>Changed some efficient wait times (used when using the 'efficient' option) </li>
                  <li>Greater Chain now works correctly with channeled abilities</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.4 - 22-1-2021</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Simulation counter now hopefully works properly</li>
                  <li>Ring of Vigour and Conservation of Energy now stack</li>
                  <li>Added the Ultimatums and Impatient perks</li>
                  <li>linking to wiki (CTRL+left click on image) now takes precedence over adding it to the bar</li>
                  <li>Block of information when clicking on AADPT number now stays open when running another simulation (click on AADPT number again to close it)</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.3 - 21-12-2020</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added a counter</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.2 - 14-12-2020</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added Greater Chain and Greater Ricochet</li>
                  <li>Fixed an issue with Wild Magic</li>
                  <li>Set Dragon Breath target cap to 4 and increased its adrenaline gain to 10 when it hits 2 or more targets</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.1 - 18-10-2020</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added the Devotion ability</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.0 - 11-8-2020</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Left clicking on abilities in their respective sections now puts them in the first
                    available slot on the bar</li>
                  <li>Left clicking + CTRL now links to the ability's wiki page</li>
                  <li>Added a new ability info table which can be seen when clicked on the resulting AADPT number</li>
                  <li>Added the Archaeology relics: Heightened Senses, Fury of the Small, Conservation of
                    Energy and Berserker's Fury</li>
                  <li>Added Perks: Shield Bashing</li>
                  <li>Fixed an issue where bleed abilities would be nulled when using the Planted Feet perk</li>
                  <li>Limited AoE abilities to be able to damage max 9 targets except for corruption shot&blast</li>
                  <li>Changed seconds to ticks within the code for clarity</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.04.0</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Added Caroming, Ruthless (as a flat damage bonus) and Reflexes perk</li>
                  <li>Increased maximum amount of targets to 10</li>
                  <li>Added Freedom and Anticipation abilities</li>
                  <li>Fixed an issue where planted feet wasn't working</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.03.1</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>Cleaned out/changed/created several directories</li>
                  <li>Added Hurricane + Destroy to the shared ability cooldown list</li>
                  <li>Fixed an issue where certain abilities would be on cooldown indefinitely</li>
                </ul>

                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.03.0</strong></p>
                <ul style="margin-top: 10px; margin-right: 15px;">
                  <li>All average ability damages are now calculated properly within the code instead of reading
                    values from an excel sheet</li>
                  <li>Added Precise, Equilibrium, Biting, Flanking and Lunging perks</li>
                  <li>Moved the options block and increased its size</li>
                  <li>Rewrote code so all player equipment related options are now assigned to the player object instead of them
                    being all over the place</li>
                  <li>Added Concentrated Blast, Fury and Greater Fury effects related to critical hits</li>
                  <li>Added a fourth condition for the cycle finder: Forced critical hit boost has to be equal too</li>
                  <li>Added Meteor Strike, Sunshine and Incendiary adrenaline boosting effect due to crits --- might be wonky</li>
                  <li>Added the aftershock perk and therefore also added the base damage back, and this time properly!</li>
                  <li>Added level 20 gear option and Erethdor's Grimoire</li>
                  <li>Added 2 defensive abilities: Debilitate and Bash</li>
                  <li>Base Ability Damage Boosts are now applied properly and in the right place</li>
                  <li>Added Equilibrium aura and made the average hit calculator more accurate</li>
                  <li>Widened certain blocks</li>
                  <li>Added Berserker, Maniacal and Reckless aura's</li>
                  <li>Added Damage boosts from level increasing boosts like the aura's above or potions</li>
                  <li>Added Prayer boosts</li>
                  <li>Added print more info button in options for python script</li>
                  <li>Rewrote code resulting in a slight decrease in python script runtime but increasing the readability of the
                    script</li>
                  <li>Made it so ability info is read from excel only once upon startup instead of every time the FIGHT! button is
                    pressed resulting in a significant decrease in execution time, especially for bars with
                    small cycle times</li>
                  <li>Moved host from DigitalOcean (paid) to Heroku (free)</li>
                  <li>Added Options Info section</li>
                </ul> -->
                <p style="margin-top: 10px; margin-left: 15px; margin-right: 15px;"><strong>V1.05.5 and earlier not available</strong></p>
              </b-card-text>
            </b-card-body>
          </b-collapse>
        </b-card>
      </b-card>
    </div>

    <b-button-group class="user-select-button-group">
      <b-button id="AttBtn" @click="collapse(0)" variant="secondary">Attack</b-button>
      <b-button id="StrBtn" @click="collapse(1)" variant="secondary">Strength</b-button>
      <b-button id="MagBtn" @click="collapse(2)" variant="secondary">Magic</b-button>
      <b-button id="RanBtn" @click="collapse(3)" variant="secondary">Ranged</b-button>
      <b-button id="ConBtn" @click="collapse(4)" variant="secondary">Constitution</b-button>
      <b-button id="DefBtn" @click="collapse(5)" variant="secondary">Defence</b-button>
      <b-button id="OptBtn" @click="collapse(6)" variant="secondary">Options</b-button>
    </b-button-group>

    <div id="attAbils" class="content AbilBlock" style="margin-top:20px;">
      <div class="attbox">
        <div class="AbilType">Basic</div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Slice.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Slice" alt="Slice" width="60" height="60" @click="abilClick($event)" title="Slice">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Backhand.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Backhand" alt="Backhand" width="60" height="60" @click="abilClick($event)" title="Backhand">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Havoc.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Havoc" alt="Havoc" width="60" height="60" @click="abilClick($event)" title="Havoc">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Smash.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Smash" alt="Smash" width="60" height="60" @click="abilClick($event)" title="Smash">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Barge.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Barge" alt="Barge" width="60" height="60" @click="abilClick($event)" title="Barge">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Greater_Barge.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Barge" alt="Greater_Barge" width="60" height="60" @click="abilClick($event)" title="Greater Barge">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Sever.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Sever" alt="Sever" width="60" height="60" @click="abilClick($event)" title="Sever">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Bladed_Dive.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Bladed_Dive" alt="Bladed_Dive" width="60" height="60" @click="abilClick($event)" title="Bladed Dive">
        </div>
      </div>

      <div class="attbox">
        <div class="AbilType">Threshold</div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Slaughter.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Slaughter" alt="Slaughter" width="60" height="60" @click="abilClick($event)" title="Slaughter">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Forceful_Backhand.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Forceful_Backhand" alt="Forceful_Backhand" width="60" height="60" @click="abilClick($event)" title="Forceful Backhand">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Flurry.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Flurry" alt="Flurry" width="60" height="60" @click="abilClick($event)" title="Flurry">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Greater_Flurry.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Flurry" alt="Greater_Flurry" width="60" height="60" @click="abilClick($event)" title="Greater Flurry">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Hurricane.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Hurricane" alt="Hurricane" width="60" height="60" @click="abilClick($event)" title="Hurricane">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Blood_Tendrils.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Blood_Tendrils" alt="Blood_Tendrils" width="60" height="60" @click="abilClick($event)" title="Blood Tendrils">
        </div>
      </div>

      <div class="attbox">
        <div class="AbilType">Ultimate</div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Overpower.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Overpower" alt="Overpower" width="60" height="60" @click="abilClick($event)" title="Overpower">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Massacre.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Massacre" alt="Massacre" width="60" height="60" @click="abilClick($event)" title="Massacre">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Meteor_Strike.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Meteor_Strike" alt="Meteor_Strike" width="60" height="60" @click="abilClick($event)" title="Meteor Strike">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Balanced_Strike.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Balanced_Strike" alt="Balanced_Strike" width="60" height="60" @click="abilClick($event)" title="Balanced Strike">
        </div>
      </div>

      <div class="attbox">
        <div class="AbilType">Lesser</div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Lesser_Havoc.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Havoc" alt="Lesser_Havoc" width="60" height="60" @click="abilClick($event)" title="Lesser Havoc">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Lesser_Smash.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Smash" alt="Lesser_Smash" width="60" height="60" @click="abilClick($event)" title="Lesser Smash">
        </div>
        <div class="att">
          <img :src="require('@/assets/AbilityImages/Lesser_Sever.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Sever" alt="Lesser_Sever" width="60" height="60" @click="abilClick($event)" title="Lesser Sever">
        </div>
      </div>
    </div>

    <div id="strAbils" class="content AbilBlock">
      <div class="strbox">
        <div class="AbilType" style="background-color: var(--strColor);">Basic</div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Kick.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Kick" alt="Kick" width="60" height="60" @click="abilClick($event)" title="Kick">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Punish.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Punish" alt="Punish" width="60" height="60" @click="abilClick($event)" title="Punish">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Dismember.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Dismember" alt="Dismember" width="60" height="60" @click="abilClick($event)" title="Dismember">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Fury.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Fury" alt="Fury" width="60" height="60" @click="abilClick($event)" title="Fury">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Greater_Fury.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Fury" alt="Greater_Fury" width="60" height="60" @click="abilClick($event)" title="Greater Fury">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Cleave.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Cleave" alt="Cleave" width="60" height="60" @click="abilClick($event)" title="Cleave">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Decimate.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Decimate" alt="Decimate" width="60" height="60" @click="abilClick($event)" title="Decimate">
        </div>
      </div>

      <div class="strbox">
        <div class="AbilType" style="background-color: var(--strColor);">Threshold</div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Stomp.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Stomp" alt="Stomp" width="60" height="60" @click="abilClick($event)" title="Stomp">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Destroy.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Destroy" alt="Destroy" width="60" height="60" @click="abilClick($event)" title="Destroy">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Quake.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Quake" alt="Quake" width="60" height="60" @click="abilClick($event)" title="Quake">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Assault.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Assault" alt="Assault" width="60" height="60" @click="abilClick($event)" title="Assault">
        </div>
      </div>

      <div class="strbox">
        <div class="AbilType" style="background-color: var(--strColor);">Ultimate</div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Berserk.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Berserk" alt="Berserk" width="60" height="60" @click="abilClick($event)" title="Berserk">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Pulverise.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Pulverise" alt="Pulverise" width="60" height="60" @click="abilClick($event)" title="Pulverise">
        </div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Frenzy.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Frenzy" alt="Frenzy" width="60" height="60" @click="abilClick($event)" title="Frenzy">
        </div>
      </div>

      <div class="strbox">
        <div class="AbilType" style="background-color: var(--strColor);">Lesser</div>
        <div class="str">
          <img :src="require('@/assets/AbilityImages/Lesser_Dismember.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Dismember" alt="Lesser_Dismember" width="60" height="60" @click="abilClick($event)" title="Lesser Dismember">
        </div>
      </div>
    </div>

    <div id="magAbils" class="content AbilBlock">
      <div class="magbox">
        <div class="AbilType" style="background-color: var(--magColor); color: #FFFFFF">Basic</div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Wrack.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Wrack" alt="Wrack" width="60" height="60" @click="abilClick($event)" title="Wrack">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Impact.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Impact" alt="Impact" width="60" height="60" @click="abilClick($event)" title="Impact">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Dragon_Breath.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Dragon_Breath" alt="Dragon_Breath" width="60" height="60" @click="abilClick($event)" title="Dragon Breath">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Sonic_Wave.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Sonic_Wave" alt="Sonic_Wave" width="60" height="60" @click="abilClick($event)" title="Sonic Wave">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Shock.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Shock" alt="Shock" width="60" height="60" @click="abilClick($event)" title="Shock">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Concentrated_Blast.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Concentrated_Blast" alt="Concentrated_Blast" width="60" height="60" @click="abilClick($event)" title="Concentrated Blast">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Greater_Concentrated_Blast.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Concentrated_Blast" alt="Greater_Concentrated_Blast" width="60" height="60" @click="abilClick($event)" title="Greater Concentrated Blast">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Combust.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Combust" alt="Combust" width="60" height="60" @click="abilClick($event)" title="Combust">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Surge.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Surge" alt="Surge" width="60" height="60" @click="abilClick($event)" title="Surge">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Chain.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Chain" alt="Chain" width="60" height="60" @click="abilClick($event)" title="Chain">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Greater_Chain.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Chain" alt="Greater_Chain" width="60" height="60" @click="abilClick($event)" title="Greater Chain">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Corruption_Blast.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Corruption_Blast" alt="Corruption_Blast" width="60" height="60" @click="abilClick($event)" title="Corruption Blast">
        </div>
      </div>

      <div class="magbox">
        <div class="AbilType" style="background-color: var(--magColor); color: #FFFFFF">Threshold</div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Asphyxiate.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Asphyxiate" alt="Asphyxiate" width="60" height="60" @click="abilClick($event)" title="Asphyxiate">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Deep_Impact.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Deep_Impact" alt="Deep_Impact" width="60" height="60" @click="abilClick($event)" title="Deep Impact">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Horror.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Horror" alt="Horror" width="60" height="60" @click="abilClick($event)" title="Horror">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Detonate.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Detonate" alt="Detonate" width="60" height="60" @click="abilClick($event)" title="Detonate">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Wild_Magic.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Wild_Magic" alt="Wild_Magic" width="60" height="60" @click="abilClick($event)" title="Wild Magic">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Smoke_Tendrils.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Smoke_Tendrils" alt="Smoke_Tendrils" width="60" height="60" @click="abilClick($event)" title="Smoke Tendrils">
        </div>
      </div>

      <div class="magbox">
        <div class="AbilType" style="background-color: var(--magColor); color: #FFFFFF">Ultimate</div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Omnipower.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Omnipower" alt="Omnipower" width="60" height="60" @click="abilClick($event)" title="Omnipower">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Metamorphosis.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Metamorphosis" alt="Metamorphosis" width="60" height="60" @click="abilClick($event)" title="Metamorphosis">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Tsunami.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Tsunami" alt="Tsunami" width="60" height="60" @click="abilClick($event)" title="Tsunami">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Sunshine.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Sunshine" alt="Sunshine" width="60" height="60" @click="abilClick($event)" title="Sunshine">
        </div>
      </div>

      <div class="magbox">
        <div class="AbilType" style="background-color: var(--magColor); color: #FFFFFF">Lesser</div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Lesser_Dragon_Breath.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Dragon_Breath" alt="Lesser_Dragon_Breath" width="60" height="60" @click="abilClick($event)" title="Lesser Dragon Breath">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Lesser_Sonic_Wave.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Sonic_Wave" alt="Lesser_Sonic_Wave" width="60" height="60" @click="abilClick($event)" title="Lesser Sonic Wave">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Lesser_Concentrated_Blast.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Concentrated_Blast" alt="Lesser_Concentrated_Blast" width="60" height="60" @click="abilClick($event)" title="Lesser Concentrated Blast">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Lesser_Combust.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Combust" alt="Lesser_Combust" width="60" height="60" @click="abilClick($event)" title="Lesser Combust">
        </div>
      </div>
    </div>

    <div id="ranAbils" class="content AbilBlock">
      <div class="ranbox">
        <div class="AbilType" style="background-color: var(--ranColor); color: #FFFFFF">Basic</div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Piercing_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Piercing_Shot" alt="Piercing_Shot" width="60" height="60" @click="abilClick($event)" title="Piercing Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Binding_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Binding_Shot" alt="Binding_Shot" width="60" height="60" @click="abilClick($event)" title="Binding Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Snipe.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Snipe" alt="Snipe" width="60" height="60" @click="abilClick($event)" title="Snipe">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Dazing_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Dazing_Shot" alt="Dazing_Shot" width="60" height="60" @click="abilClick($event)" title="Dazing Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Greater_Dazing_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Dazing_Shot" alt="Greater_Dazing_Shot" width="60" height="60" @click="abilClick($event)" title="Greater Dazing Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Demoralise.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Demoralise" alt="Demoralise" width="60" height="60" @click="abilClick($event)" title="Demoralise">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Needle_Strike.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Needle_Strike" alt="Needle_Strike" width="60" height="60" @click="abilClick($event)" title="Needle Strike">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Fragmentation_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Fragmentation_Shot" alt="Fragmentation_Shot" width="60" height="60" @click="abilClick($event)" title="Fragmentation Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Escape.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Escape" alt="Escape" width="60" height="60" @click="abilClick($event)" title="Escape">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Ricochet.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Ricochet" alt="Ricochet" width="60" height="60" @click="abilClick($event)" title="Ricochet">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Greater_Ricochet.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Ricochet" alt="Greater_Ricochet" width="60" height="60" @click="abilClick($event)" title="Greater Ricochet">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Corruption_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Corruption_Shot" alt="Corruption_Shot" width="60" height="60" @click="abilClick($event)" title="Corruption Shot">
        </div>
      </div>

      <div class="ranbox">
        <div class="AbilType" style="background-color: var(--ranColor); color: #FFFFFF">Threshold</div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Snap_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Snap_Shot" alt="Snap_Shot" width="60" height="60" @click="abilClick($event)" title="Snap Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Tight_Bindings.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Tight_Bindings" alt="Tight_Bindings" width="60" height="60" @click="abilClick($event)" title="Tight Bindings">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Rout.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Rout" alt="Rout" width="60" height="60" @click="abilClick($event)" title="Rout">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Rapid_Fire.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Rapid_Fire" alt="Rapid_Fire" width="60" height="60" @click="abilClick($event)" title="Rapid Fire">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Bombardment.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Bombardment" alt="Bombardment" width="60" height="60" @click="abilClick($event)" title="Bombardment">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Salt_the_Wound.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Salt_the_Wound" alt="Salt_the_Wound" width="60" height="60" @click="abilClick($event)" title="Salt the Wound">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Shadow_Tendrils.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Shadow_Tendrils" alt="Shadow_Tendrils" width="60" height="60" @click="abilClick($event)" title="Shadow Tendrils">
        </div>
      </div>

      <div class="ranbox">
        <div class="AbilType" style="background-color: var(--ranColor); color: #FFFFFF">Ultimate</div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Deadshot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Deadshot" alt="Deadshot" width="60" height="60" @click="abilClick($event)" title="Deadshot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Incendiary_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Incendiary_Shot" alt="Incendiary_Shot" width="60" height="60" @click="abilClick($event)" title="Incendiary Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Unload.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Unload" alt="Unload" width="60" height="60" @click="abilClick($event)" title="Unload">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Death\'s_Swiftness.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Death's_Swiftness" alt="Death's_Swiftness" width="60" height="60" @click="abilClick($event)" title="Death's Swiftness">
        </div>
      </div>

      <div class="ranbox">
        <div class="AbilType" style="background-color: var(--ranColor); color: #FFFFFF">Lesser</div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Lesser_Snipe.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Snipe" alt="Lesser_Snipe" width="60" height="60" @click="abilClick($event)" title="Lesser Snipe">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Lesser_Dazing_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Dazing_Shot" alt="Lesser_Dazing_Shot" width="60" height="60" @click="abilClick($event)" title="Lesser Dazing Shot">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Lesser_Needle_Strike.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Needle_Strike" alt="Lesser_Needle_Strike" width="60" height="60" @click="abilClick($event)" title="Lesser Needle Strike">
        </div>
        <div class="ran">
          <img :src="require('@/assets/AbilityImages/Lesser_Fragmentation_Shot.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Lesser_Fragmentation_Shot" alt="Lesser_Fragmentation_Shot" width="60" height="60" @click="abilClick($event)" title="Lesser Fragmentation Shot">
        </div>
      </div>
    </div>

    <div id="conAbils" class="content AbilBlock">
      <div class="conbox">
        <div class="AbilType" style="background-color: var(--conColor); color: #FFFFFF">Basic</div>
        <div class="con">
          <img :src="require('@/assets/AbilityImages/Sacrifice.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Sacrifice" alt="Sacrifice" width="60" height="60" @click="abilClick($event)" title="Sacrifice">

        </div>
        <div class="con">
          <img :src="require('@/assets/AbilityImages/Tuska\'s_Wrath.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Tuska's_Wrath" alt="Tuska's_Wrath" width="60" height="60" @click="abilClick($event)" title="Tuska's Wrath">
        </div>
      </div>

      <div class="conbox">
        <div class="AbilType" style="background-color: var(--conColor); color: #FFFFFF">Threshold</div>
      </div>

      <div class="conbox">
        <div class="AbilType" style="background-color: var(--conColor); color: #FFFFFF">Ultimate</div>
      </div>

      <div class="conbox">
        <div class="AbilType" style="background-color: var(--conColor); color: #FFFFFF">Lesser</div>
      </div>
    </div>

    <div id="defAbils" class="content AbilBlock">
      <div class="defbox">
        <div class="AbilType" style="background-color: var(--defColor); color: #FFFFFF">Basic</div>
        <div class="def">
          <img :src="require('@/assets/AbilityImages/Anticipation.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Anticipation" alt="Anticipation" width="60" height="60" @click="abilClick($event)" title="Anticipation">
        </div>
        <div class="def">
          <img :src="require('@/assets/AbilityImages/Bash.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Bash" alt="Bash" width="60" height="60" @click="abilClick($event)" title="Bash">
        </div>
        <div class="def">
          <img :src="require('@/assets/AbilityImages/Freedom.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Freedom" alt="Freedom" width="60" height="60" @click="abilClick($event)" title="Freedom">
        </div>
      </div>

      <div class="defbox">
        <div class="AbilType" style="background-color: var(--defColor); color: #FFFFFF">Threshold</div>
        <div class="def">
          <img :src="require('@/assets/AbilityImages/Devotion.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Devotion" alt="Devotion" width="60" height="60" @click="abilClick($event)" title="Devotion">
        </div>
        <div class="def">
          <img :src="require('@/assets/AbilityImages/Debilitate.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Debilitate" alt="Debilitate" width="60" height="60" @click="abilClick($event)" title="Debilitate">
        </div>
      </div>

      <div class="defbox">
        <div class="AbilType" style="background-color: var(--defColor); color: #FFFFFF">Ultimate</div>
      </div>

      <div class="defbox">
        <div class="AbilType" style="background-color: var(--defColor); color: #FFFFFF">Lesser</div>
      </div>
    </div>

    <div id="optBlock" class="content OptionBlock" style="margin-bottom: 20px;">
      <form id="optmenu" name="optmenu" method="get">
        <div class="optsect" style="width: 20px;"></div>

        <div id="AbilityOptions1" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Strength Boost</p>
          <b-form-input size="sm" class="mt-1" id="StrengthBoost" placeholder="Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'The amount of boosted levels (above your base level) due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
          <b-form-select class="mt-1" id="StrengthPrayer" v-model="StrengthPrayer" :options="optStrengthPrayer" size="sm"></b-form-select>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Magic Boost</p>
          <b-form-input size="sm" class="mt-1" id="MagicBoost" placeholder="Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'The amount of boosted levels (above your base level) due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
          <b-form-select class="mt-1" id="MagicPrayer" v-model="MagicPrayer" :options="optMagicPrayer" size="sm"></b-form-select>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Ranged Boost</p>
          <b-form-input size="sm" class="mt-1" id="RangedBoost" placeholder="Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'The amount of boosted levels (above your base level) due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
          <b-form-select class="mt-1" id="RangedPrayer" v-model="RangedPrayer" :options="optRangedPrayer" size="sm"></b-form-select>
        </div>

        <div class="optsect" style="width: 10px;"></div>

        <div id="AbilityOptions2" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Invention Perks</p>

          <b-form-checkbox class="switch mt-1" id="Level20Gear" v-model="Level20Gear" switch v-b-tooltip.hover.right="'Assumes the equipment levels of all augmented items are equal to level 20'">Level 20 Gear</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="PlantedFeet" v-model="PlantedFeet" switch v-b-tooltip.hover.right="'Duration of Sunshine and Death\'s Swiftness are increased by 25%, but lose their damage-over-time effect'">Planted Feet</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="Reflexes" v-model="Reflexes" switch v-b-tooltip.hover.right="'Anticipation\'s duration and cooldown are halved'">Reflexes</b-form-checkbox>

          <b-form-select class="mt-1" id="Precise" v-model="Precise" :options="optPrecise" size="sm" v-b-tooltip.hover.right="'Increases your minimum damage by 1.5% per rank of your maximum damage'"></b-form-select>
          <b-form-select class="mt-1" id="Equilibrium" v-model="Equilibrium" :options="optEquilibrium" size="sm" v-b-tooltip.hover.right="'Increases minimum hit by 3% per rank, and decreases maximum hit by 1% per rank'"></b-form-select>
          <b-form-select class="mt-1" id="Biting" v-model="Biting" :options="optBiting" size="sm" v-b-tooltip.hover.right="'+2% chance per rank to critically hit opponents'"></b-form-select>
          <b-form-select class="mt-1" id="Flanking" v-model="Flanking" :options="optFlanking" size="sm" v-b-tooltip.hover.right="'Certain abilities lose their stunning ability in exchange for dealing increased damage to a target that does not face the player'"></b-form-select>
          <b-form-select class="mt-1" id="Lunging" v-model="Lunging" :options="optLunging" size="sm" v-b-tooltip.hover.right="'The maximum damage of Combust, Dismember and Fragmentation shot is increased by 20% weapon damage per rank, but enemies that move will only take 1.5X increased damage'"></b-form-select>
          <b-form-select class="mt-1" id="Caroming" v-model="Caroming" :options="optCaroming" size="sm" v-b-tooltip.hover.right="'Chain and Ricochet hit 1 extra target per rank'"></b-form-select>
          <b-form-select class="mt-1" id="Ruthless" v-model="Ruthless" :options="optRuthless" size="sm" v-b-tooltip.hover.right="'Whenever you defeat an enemy you gain a 0.5% damage boost per rank for 20 seconds (code assumes a continuous max stack of 2.5%)'"></b-form-select>
          <b-form-select class="mt-1" id="Aftershock" v-model="Aftershock" :options="optAftershock" size="sm" v-b-tooltip.hover.right="'After dealing 50,000 damage, create an explosion centered on your current target, dealing up to 40% per rank weapon damage to nearby enemies'"></b-form-select>
          <b-form-select class="mt-1" id="ShieldBashing" v-model="ShieldBashing" :options="optShieldBashing" size="sm" v-b-tooltip.hover.right="'Debilitate\'s damage is increased by 15% per rank'"></b-form-select>
          <b-form-select class="mt-1" id="Ultimatums" v-model="Ultimatums" :options="optUltimatums" size="sm" v-b-tooltip.hover.right="'Reduces the adrenaline cost of Overpower, Frenzy, Unload and Omnipower by 5% per rank'"></b-form-select>
          <b-form-select class="mt-1" id="Impatient" v-model="Impatient" :options="optImpatient" size="sm" v-b-tooltip.hover.right="'9% chance per rank for basic abilities to generate 3% extra adrenaline'"></b-form-select>
        </div>

        <div class="optsect" style="width: 10px;"></div>

        <div id="PlayerOptions" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Equipment</p>
          <b-form-checkbox class="switch mt-1" id="StrengthCape" v-model="StrengthCape" switch v-b-tooltip.hover.right="'The Strength cape\'s perk causes Dismember\'s damage over time to last an extra 3.6 seconds (an extra 3 hits for a total of 8)'">Strength Cape</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="MSoA" v-model="MSoA" switch v-b-tooltip.hover.right="'Melee damage over time abilities (bleeds) have their duration extended by 50%, rounded down to the nearest whole number'">Masterwork Spear of Annihilation</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="Grimoire" v-model="Grimoire" switch v-b-tooltip.hover.right="'Every non-bleed hit has a 12% chance to be forced to become a critical hit and the player\'s damage cap for critical hits is increased to 15,000, up from 12,000'">Erethdor's Grimoire</b-form-checkbox>
<!--          <b-form-checkbox class="switch mt-1" id="KerapacWristWraps" v-model="KerapacWristWraps" switch v-b-tooltip.hover.right="'For six seconds after using the Dragon Breath ability, the Combust ability will deal 25% more damage - and deal it instantly'">Kerapac's wrist wraps</b-form-checkbox>-->

          <b-form-select class="mt-1" id="Ring" v-model="Ring" size="sm">
            <b-form-select-option v-for="ring in optRing" :key="ring.value" :id="ring.value" :value="ring.value" v-b-tooltip.hover.right :title="ring.title">{{ ring.text }}</b-form-select-option>
          </b-form-select>


          <b-form-select class="mt-1" id="Aura" v-model="Aura" size="sm">
            <b-form-select-option v-for="aura in optAura" :key="aura.value" :id="aura.value" :value="aura.value" v-b-tooltip.hover.right :title="aura.title">{{ aura.text }}</b-form-select-option>
          </b-form-select>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Bash Ability</p>
          <b-form-input size="sm" class="mt-1" id="DefenceLevel" placeholder="Defence Level" type="number" min="0" max="200" v-b-tooltip.hover></b-form-input>
          <b-form-input size="sm" class="mt-1" id="ShieldArmourValue" placeholder="Shield Armour Value" type="number" min="0" max="1000" v-b-tooltip.hover></b-form-input>
        </div>

        <div class="optsect" style="width: 10px;"></div>

        <div id="DummyOptions" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Player</p>
          <b-form-checkbox class="switch mt-1" id="afkStatus" v-model="afkStatus" switch v-b-tooltip.hover.right="'Assumes the player breaks channeling abilities such that they still do all their damage (except for Concentrated Blast which cuts off after 2 hits) but the next ability is activated earlier'">Efficient</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="switchStatus" v-model="switchStatus" switch v-b-tooltip.hover.right="'Assumes the player switches between 2h/dual/shield whenever required for the next available ability'">Switcher</b-form-checkbox>

          <b-form-input size="sm" class="mt-1" id="baseDamage" placeholder="Ability Damage" type="number" min="1" max="10000" v-b-tooltip.hover.right="'The ability damage as calculated in the \'Calculating ability damage\' section on the RS3 wiki (Min:1, Max:10000)'"></b-form-input>

          <p style="margin-top: 15px; text-align: center; font-weight: bold;">Dummy</p>
          <b-form-checkbox class="switch mt-1" id="movementStatus" v-model="movementStatus" switch v-b-tooltip.hover.right="'Assumes the dummy is stuck in place, meaning bleed damage won\'t be multiplied. When not ticked, bleed damage is multiplied for all hits (unless the dummy is stunned and/or bound).'">Stationary</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="stunbindStatus" v-model="stunbindStatus" switch v-b-tooltip.hover.right="'Assumes the dummy is immune to stuns and binds from abilities'">Stun&Bind Immune</b-form-checkbox>

          <b-form-input size="sm" class="mt-1" id="nTargets" placeholder="Number of Dummies" type="number" min="1" max="10" v-b-tooltip.hover.right="'Number of dummies affected by AoE abilities'"></b-form-input>
        </div>

        <div class="optsect" style="width: 10px;"></div>

        <div id="Relics&PythonScriptOptions" class="optsect">
          <p style="margin-top: 15px; text-align: center; font-weight: bold;">Archaeology Relics</p>

          <b-form-checkbox class="switch mt-1" id="HeightenedSenses" v-model="HeightenedSenses" switch v-b-tooltip.hover.right="'Increases maximum adrenaline by 10%'">Heightened Senses</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="FotS" v-model="FotS" switch v-b-tooltip.hover.right="'All adrenaline generating basic abilities generate +1% adrenaline'">Fury of the Small</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="CoE" v-model="CoE" switch v-b-tooltip.hover.right="'After using an ultimate ability, you will regain 10% adrenaline'">Conservation of Energy</b-form-checkbox>

          <b-form-input size="sm" class="mt-1" id="BerserkersFury" placeholder="Berserker's Fury" type="number" step="0.1" min="0" max="5.5" v-b-tooltip.hover.right="'Deal up to +5.5% damage (all styles) the lower your current life points are below max'"></b-form-input>

          <p style="margin-top: 15px; text-align: center; font-weight: bold;">Python Script</p>

          <div v-b-tooltip.hover.right="'When a value has been set for both the Simulation Time (in seconds, min:1, max:3600) and the Starting Adrenaline (min:0, max:100), the Python script won\'t detect cycles but instead runs for the given simulation time and determines the Damage Per Tick (DPT) in that time.'">
            <b-form-input size="sm" class="mt-1" id="simulationTime" placeholder="Simulation Time (s)" type="number" min="0" max="3600"></b-form-input>
            <b-form-input size="sm" class="mt-1" id="Adrenaline" placeholder="Start Adrenaline" type="number" min="0" max="100"></b-form-input>
          </div>

          <b-form-checkbox class="switch mt-1" id="Debug" v-model="Debug" switch v-b-tooltip.hover.right="'When ticked, up to the first 5 minutes of the simulation time can be verified upon clicking the resulting AADPT number (mostly used for debugging purposes)'">Print more info</b-form-checkbox>
        </div>

        <div class="optsect" style="width: 20px;"></div>
      </form>
    </div>

    <div id="RevolutionBar">
      <div id="revo1" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)" style="border-left: 0; width: 61px;"></div>
      <div id="revo2" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo3" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo4" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo5" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo6" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo7" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo8" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo9" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo10" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo11" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo12" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo13" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      <div id="revo14" class="RevoBar" @drop="drop($event)" @dragover="allowDrop($event)" style="border-right: 0; width: 61px"></div>
    </div>

    <div id="clear-button">
      <b-button size="sm" @click="clearBar()" variant="secondary">clear bar</b-button>
    </div>

    <div id="calc-button">
      <b-button @click="calcDPT($event)" variant="secondary">FIGHT!</b-button>
    </div>

    <div>
      <b-card hidden @click="showExtra" id="result-card-warning" bg-variant="warning" text-variant="white" header="Warning" class="text-center output-card" v-b-tooltip.hover.right="'Click here for more in depth information!'">
        <b-card-text id="result-text-warning"></b-card-text>
      </b-card>

      <b-card hidden @click="showExtra" id="result-card-danger" bg-variant="danger" text-variant="white" header="Error" class="text-center output-card">
        <b-card-text id="result-text-danger"></b-card-text>
      </b-card>

      <b-card hidden @click="showExtra" id="result-card" header="Result" bg-variant="dark" text-variant="white" class="text-center output-card" v-b-tooltip.hover.right="'Click here for more in depth information!'">
        <b-card-text id="result-text"></b-card-text>
      </b-card>
    </div>

    <b-card hidden id="result-card-extra" header="Result" bg-variant="dark" text-variant="white" class="text-left output-card-extra">
      <b-card-text id="result-text-extra"></b-card-text>
    </b-card>

    <p id="counter"></p>
  </div>
</template>

<script>
let LastIdx = null;
let BarAbilities = [];
let RevolutionBar = document.getElementsByClassName("RevoBar");
let PreviousBarInfo;

let origin
if (window.origin === 'http://localhost:8080') {
  origin = 'http://localhost:5000';
} else {
  origin = window.origin;
}
// let AlreadyRan = false;

export default {
  created: async function(){
    await fetch(`${origin}/api/return_counter`, {
        method: "GET",
        // credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
      }) // after receiving the response do:
      .then(function (response) {

        // if something went wrong, print error
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return;
        }

        response.json().then(function (data) {
          document.getElementById("counter").innerHTML = `Simulated fights: ${data['counter']}`;
        })
      })
  },
  data: function() {
    return {
      centerStyle: {
        alignItems: 'center',
        textAlign: 'center'
      },
      StrengthPrayer: null,
      optStrengthPrayer: [
        { value: null, text: 'Strength Prayer', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1.02, text: 'Burst of Strength'},
        { value: 1.04, text: 'Superhuman Strength'},
        { value: 1.06, text: 'Ultimate Strength'},
        { value: 1.08, text: 'Piety'},
        { value: 1.10, text: 'Turmoil'},
        { value: 1.12, text: 'Malevolence'}
      ],
      MagicPrayer: null,
      optMagicPrayer: [
        { value: null, text: 'Magic Prayer', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1.02, text: 'Charge'},
        { value: 1.04, text: 'Super Charge'},
        { value: 1.06, text: 'Overcharge'},
        { value: 1.08, text: 'Augury'},
        { value: 1.10, text: 'Torment'},
        { value: 1.12, text: 'Affliction'}
      ],
      RangedPrayer: null,
      optRangedPrayer: [
        { value: null, text: 'Ranged Prayer', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1.02, text: 'Unstoppable Force'},
        { value: 1.04, text: 'Unrelenting Force'},
        { value: 1.06, text: 'Overpowering Force'},
        { value: 1.08, text: 'Rigour'},
        { value: 1.10, text: 'Anguish'},
        { value: 1.12, text: 'Desolation'}
      ],
      Level20Gear: { value: 'Level20Gear', text: 'Level 20 Gear' },
      PlantedFeet: { value: 'PlantedFeet', text: 'Planted Feet' },
      Reflexes: { value: 'Reflexes', text: 'Reflexes' },
      Precise: null,
      optPrecise: [
        { value: null, text: 'Precise Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Precise 1'},
        { value: 2, text: 'Precise 2'},
        { value: 3, text: 'Precise 3'},
        { value: 4, text: 'Precise 4'},
        { value: 5, text: 'Precise 5'},
        { value: 6, text: 'Precise 6'}
      ],
      Equilibrium: null,
      optEquilibrium: [
        { value: null, text: 'Equilibrium Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Equilibrium 1'},
        { value: 2, text: 'Equilibrium 2'},
        { value: 3, text: 'Equilibrium 3'},
        { value: 4, text: 'Equilibrium 4'}
      ],
      Biting: null,
      optBiting: [
        { value: null, text: 'Biting Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Biting 1'},
        { value: 2, text: 'Biting 2'},
        { value: 3, text: 'Biting 3'},
        { value: 4, text: 'Biting 4'}
      ],
      Flanking: null,
      optFlanking: [
        { value: null, text: 'Flanking Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Flanking 1'},
        { value: 2, text: 'Flanking 2'},
        { value: 3, text: 'Flanking 3'},
        { value: 4, text: 'Flanking 4'}
      ],
      Lunging: null,
      optLunging: [
        { value: null, text: 'Lunging Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Lunging 1'},
        { value: 2, text: 'Lunging 2'},
        { value: 3, text: 'Lunging 3'},
        { value: 4, text: 'Lunging 4'}
      ],
      Caroming: null,
      optCaroming: [
        { value: null, text: 'Caroming Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Caroming 1'},
        { value: 2, text: 'Caroming 2'},
        { value: 3, text: 'Caroming 3'},
        { value: 4, text: 'Caroming 4'}
      ],
      Ruthless: null,
      optRuthless: [
        { value: null, text: 'Ruthless Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Ruthless 1'},
        { value: 2, text: 'Ruthless 2'},
        { value: 3, text: 'Ruthless 3'}
      ],
      Aftershock: null,
      optAftershock: [
        { value: null, text: 'Aftershock Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Aftershock 1'},
        { value: 2, text: 'Aftershock 2'},
        { value: 3, text: 'Aftershock 3'},
        { value: 4, text: 'Aftershock 4'}
      ],
      ShieldBashing: null,
      optShieldBashing: [
        { value: null, text: 'Shield Bashing Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Shield Bashing 1'},
        { value: 2, text: 'Shield Bashing 2'},
        { value: 3, text: 'Shield Bashing 3'},
        { value: 4, text: 'Shield Bashing 4'}
      ],
      Ultimatums: null,
      optUltimatums: [
        { value: null, text: 'Ultimatums Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Ultimatums 1'},
        { value: 2, text: 'Ultimatums 2'},
        { value: 3, text: 'Ultimatums 3'},
        { value: 4, text: 'Ultimatums 4'}
      ],
      Impatient: null,
      optImpatient: [
        { value: null, text: 'Impatient Perk', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 1, text: 'Impatient 1'},
        { value: 2, text: 'Impatient 2'},
        { value: 3, text: 'Impatient 3'},
        { value: 4, text: 'Impatient 4'}
      ],
      StrengthCape: { value: 'StrengthCape', text: 'Strength Cape' },
      MSoA: { value: 'MSoA', text: 'Masterwork Spear of Annihilation' },
      Grimoire: { value: 'Grimoire', text: 'Erethdor\'s Grimoire' },
      // KerapacWristWraps: { value: 'KerapacWristWraps', text: 'Kerapac\'s wrist wraps' },
      Ring: null,
      optRing: [
        { value: null, text: 'Ring', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 'RoV', text: 'Ring of Vigour', title: 'When an ultimate ability is used, adrenaline will be reduced by 90% instead of 100%' },
        { value: 'ReaversRing', text: 'Reaver\'s Ring', title: 'Increases critical strike chance by 5%' },
        { value: 'ChampionsRing', text: 'Champion\'s Ring', title: 'Increases critical strike chance against bleeding targets by 3%' },
        { value: 'ChannelersRing', text: 'Channeler\'s Ring', title: 'Increases critical strike chance while using channelled abilities by 4% per hit of the channelled ability' },
        { value: 'StalkersRing', text: 'Stalker\'s Ring', title: 'Increases critical strike chance when using a bow by 3% (cannot be used in conjunction with the Switcher option)' }
      ],
      Aura: null,
      optAura: [
        { value: null, text: 'Aura', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 'Equilibrium', text: 'Equilibrium', title: 'Decreases maximum hit by 25%, but increases minimum hit by the same amount' },
        { value: 'Berserker', text: 'Berserker', title: 'Boosts Attack and Strength by 10%' },
        { value: 'Maniacal', text: 'Maniacal', title: 'Boosts Magic by 10%' },
        { value: 'Reckless', text: 'Reckless', title: 'Boosts Range by 10%' }
      ],
      afkStatus: { value: 'afkStatus', text: 'Efficient' },
      switchStatus: { value: 'switchStatus', text: 'Switcher' },
      movementStatus: { value: 'movementStatus', text: 'Stationary' },
      stunbindStatus: { value: 'stunbindStatus', text: 'Stun&Bind Immune' },
      HeightenedSenses: { value: 'HeightenedSenses', text: 'Heightened Senses' },
      FotS: { value: 'FotS', text: 'Fury of the Small' },
      CoE: { value: 'CoE', text: 'Conservation of Energy' },
      Debug: { value: 'Debug', text: 'Print more info' }
    }
  },
  methods: {
    collapse: function (id) {
      let ScrollIdx = id;

      let attContent = document.getElementById("attAbils");
      let strContent = document.getElementById("strAbils");
      let magContent = document.getElementById("magAbils");
      let ranContent = document.getElementById("ranAbils");
      let conContent = document.getElementById("conAbils");
      let defContent = document.getElementById("defAbils");
      let optContent = document.getElementById("optBlock");

      let cbContent = [attContent,
        strContent,
        magContent,
        ranContent,
        conContent,
        defContent,
        optContent];

      let ScrollOut;

      // if the content is already showing
      if (cbContent[ScrollIdx].style.maxHeight) {
        cbContent[ScrollIdx].style.maxHeight = null;
        ScrollOut = false;
      } else { // else ScrollOut the content
        cbContent[ScrollIdx].style.maxHeight = cbContent[ScrollIdx].scrollHeight + "px";
        ScrollOut = true;
      }

      // depending on the action in the previous if-else statement:
      // if this is not the first button being clicked on and its not the same
      // button as last time
      if (LastIdx !== null && LastIdx !== ScrollIdx) {
        // basically do the opposite for the previous content compared to the new content
        if (ScrollOut) {
          cbContent[LastIdx].style.maxHeight = null;
        } else {
          cbContent[LastIdx].style.maxHeight = cbContent[LastIdx].scrollHeight + "px";
        }
      }

      // update the button which has previously been clicked on
      LastIdx = ScrollIdx;
    },
    // Prevent from weird shenanigans happening when dragging the element
    drag: function (event) {
      event.dataTransfer.setData("abilityName", event.target.id);
    },
    // Prevent from weird shenanigans happening when dropping the element
    allowDrop: function (event) {
      event.preventDefault();
    },
    // Function for dropping abilities into the rev bar slot
    drop: function (event) {
      // Prevent default action from happening
      event.preventDefault();

      // Ability (element) which is about to be dropped
      let srcId = event.dataTransfer.getData("abilityName");
      // Id of ability which is about to be dropped (which is its name)
      let srcAbil = document.getElementById(srcId);

      // If the user put anything else onto the bar besides an ability, return
      if (srcAbil == null || !srcAbil.classList.contains('Ability')) {
        return;
      }

      // Revo bar spot where the ability came from
      let srcRevo = srcAbil.parentNode;
      // Ability which is in the target spot
      let tgtAbil = event.currentTarget.firstElementChild;
      // Revo bar spot which is the target spot
      let tgtRevo = event.currentTarget;

      // If the ability has a field name, meaning its already on the bar
      if (srcAbil.hasAttribute('name')) {

        // If there is already an ability in the new spot
        if (tgtAbil !== null && tgtAbil !== srcAbil) {
          // Assign a new id to the elements to be swapped
          srcAbil.id = tgtRevo.id + "_" + srcAbil.name;
          tgtAbil.id = srcRevo.id + "_" + tgtAbil.name;

          // Replace the old ability with the new ability
          event.currentTarget.replaceChild(srcAbil, tgtAbil);
          // Put the old ability on the old spot
          srcRevo.appendChild(tgtAbil);

        } else { // If there is no ability in the new spot
          // Assign a new id to the elements to be swapped
          srcAbil.id = event.target.id + "_" + srcAbil.name;
          // Place the ability on the bar
          event.currentTarget.appendChild(srcAbil);
        }

      } else { // Else its a new input ability, check if its already on the bar

        // If the revolution bar already includes the ability do nothing
        if (!BarAbilities.includes(srcId)) { // put it on the bar
          // Copy of the ability which is about to be dropped
          let nodeCopy = document.getElementById(srcId).cloneNode(true);
          // Assign a new id to the copied ability revo(i) + _name
          nodeCopy.id = event.target.id + "_" + srcId;
          // Assign a name to the copied ability (which is the name of the ability)
          nodeCopy.name = srcId
          // Add event listener
          nodeCopy.addEventListener('click', this.abilClick);
          nodeCopy.addEventListener('dragstart', this.drag);

          // If there is already an ability in the new spot
          if (tgtAbil !== null) {
            // Delete the name from the array
            BarAbilities.splice(BarAbilities.indexOf(tgtAbil.name), 1);
            // Put the name of the new ability in the array
            BarAbilities.push(srcId);
            // Replace the old ability with the new ability
            event.currentTarget.replaceChild(nodeCopy, tgtAbil);

          } else { // else put it on the bar
            // put the name in an array
            BarAbilities.push(srcId);
            // put the ability on the new spot
            event.target.appendChild(nodeCopy);
          }
        }
      }
    },

    abilClick: function (event) {
      let element = event.target;
      let url;

      if (window.event.ctrlKey && element.nodeName === 'IMG' && element.parentNode.classList.value !== 'RevoBar') {
        url = "http://runescape.wiki/w/" + element.id;
        // open rs wiki page for the ability
        window.open(url, "_blank");
      } else if (element.nodeName === 'IMG' && element.parentNode.classList.value !== 'RevoBar' && !BarAbilities.includes(element.id)) {
        // if element is of type img and its not on the RevoBar
        let currentBar = document.getElementById('RevolutionBar')

        BarAbilities.push(element.id)

        for (let l = 0; l < 14; l++) {
          if (currentBar.childNodes[l].firstChild == null) {
            let nodeCopy = element.cloneNode(true);
            // Assign a new id to the copied ability revo(i) + _name
            nodeCopy.id = currentBar.childNodes[l].id + "_" + element.id;
            // Assign a name to the copied ability (which is the name of the ability)
            nodeCopy.name = element.id;
            // Add event listener
            nodeCopy.addEventListener('click', this.abilClick);
            nodeCopy.addEventListener('dragstart', this.drag);
            // put the ability on the new spot
            currentBar.childNodes[l].appendChild(nodeCopy);
            break;
          }
        }
      } else if (element.nodeName === 'IMG' && element.parentNode.classList.value === 'RevoBar') {
        // if element is of type img, meaning an ability is in that slot, delete it
        // first delete the ability from the array
        BarAbilities.splice(BarAbilities.indexOf(element.name), 1);

        // then remove the ability from the bar
        element.remove(element);
      }
    },

    clearBar: function () {
      for (let k = 0; k < RevolutionBar.length; k++) {
        // if the slot has a child element which is the ability image, delete it
        if (RevolutionBar[k].firstChild !== null) {
          RevolutionBar[k].removeChild(RevolutionBar[k].firstChild)
        }

        // delete all abilities in the array
        BarAbilities.splice(0, BarAbilities.length)
      }

      let resultCard = document.getElementById('result-card');
      let resultCardWarning = document.getElementById('result-card-warning');
      let resultCardDanger = document.getElementById('result-card-danger');
      let resultCardExtra = document.getElementById('result-card-extra');

      // Close result box if its open
      if (!resultCard.hidden) {
          resultCard.hidden = !resultCard.hidden
      } else if (!resultCardWarning.hidden) {
        resultCardWarning.hidden = !resultCardWarning.hidden
      } else if (!resultCardDanger.hidden) {
        resultCardDanger.hidden = !resultCardDanger.hidden
      }

      if (!resultCardExtra.hidden) {
        resultCardExtra.hidden = !resultCardExtra.hidden
      }
    },

    calcDPT: async function () {
      // get the run button element
      // var calcDPT = document.getElementById("calcbutton");
      // var LoopText;
      // var CycleText;
      // var AbilityTable;
      // var DPTNoteOut = false;
      let resultCard = document.getElementById('result-card');
      let resultCardWarning = document.getElementById('result-card-warning');
      let resultCardDanger = document.getElementById('result-card-danger');

      // get an array with the bar abilities in correct order
      let InputAbilities = [];

      for (let k = 0; k < RevolutionBar.length; k++) {
        if (RevolutionBar[k].firstChild !== null) {
          InputAbilities.push(RevolutionBar[k].firstChild.name)
        }
      }

      let optionElements = document.forms["optmenu"].elements

      let barInfo = {};
      let optionValue;

      for (let l = 0; l < optionElements.length; l++) {
        if (optionElements[l].type === 'checkbox') {
          optionValue = optionElements[l].checked;
        } else {
          optionValue = optionElements[l].value;
        }
        barInfo[optionElements[l].id] = optionValue;
      }

      // create dict with user options and the bar abilities
      barInfo['Abilities'] = InputAbilities;

      // Make sure the user put in a new rotation to prevent spam
      if (JSON.stringify(PreviousBarInfo) === JSON.stringify(barInfo)) {
        return;
      } else {
        PreviousBarInfo = barInfo;
      }

      // send bar info to the calc page where the DPT is calculated

      // await fetch(`${window.origin}/calc`, {
      await fetch(`${origin}/api/calc`, {
          method: "POST",
          body: JSON.stringify(barInfo),
          cache: "no-cache",
          headers: new Headers({
              "content-type": "application/json"
          })
      }) // after receiving the response do:
      .then(function (response) {

          // if something went wrong, print error
          if (response.status !== 200) {
              console.log(`Response status was not 200: ${response.status}`);
              return;
          }

          response.json().then(function (data) {
            let message;

            // if an error occured during calculating the DPT, print error
            if (data['error']) {
              message = data['error_message']
              resultCard.hidden = true;
              resultCardWarning.hidden = true;
              resultCardDanger.hidden = false;

              document.getElementById('result-text-danger').innerHTML = message;
              return;
            }

            // create a link using the DPT number, links to test page
            let linkStr = `<span style="color: #4CAF50;"><strong>${data['AADPT']} (${data['AADPTPercentage']}%)</strong></span>`;

            // CREATE A MESSAGE TO SHOW THE (AA)DPT
            if (data['CycleRotation'].length !== 0) {
                message = "The AADPT of the bar above is: " + linkStr;
            } else {
                message = "The DPT of the bar above is: " + linkStr;
            }

            // print the message in the right place
            document.getElementById('counter').innerHTML = `Simulated fights: ${data['counter']}`;

            // CREATE STRING CONTAINING THE CYCLE ROTATION
            let RotationString = '<br><br><span style="color: yellow;">START</span> --> ';

            // for every ability or stall in the rotation
            for (let m = 0; m < data['CycleRotation'].length; m++) {
                RotationString += data['CycleRotation'][m] + ' --> ';

                // break a line each time 4 elements have been printed
                if (m === 2 || (m > 3 && (m + 2) % 4 === 0)) {
                    RotationString += '<br>';
                }
            }

            // at the end, print BACK TO START
            RotationString += '<span style="color: yellow;">BACK TO START</span>';

            // STRING CONTAINING ALL REDUNDANT ABILITIES ON THE BAR
            let RedundantAbilities = data['CycleRedundant'].toString();

            let Type;
            // FORMAT SOME NICE OUTPUT TEXT WITH CYCLE INFORMATION
            if (data['CycleRotation'].length !== 0) {
              Type = 'Cycle';
            } else {
              Type = '';
            }

            let CycleText = '';
            CycleText += '<span style="color: #FF3333;">' + Type + ' Time: </span> ' + parseFloat((data['CycleTime'] * .6)).toFixed(1) + "s --> " + data['CycleTime'] + " ticks";
            CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Convergence Time: </span> ' + parseFloat((data['CycleConvergenceTime'] * .6)).toFixed(1) + "s --> " + data['CycleConvergenceTime'] + " ticks";
            CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Damage: </span> ' + data['CycleDamage'] + ' <span style="color: #707070;">Base Damage: ' + data['BaseDamage'] + '</span>';
            CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Rotation: </span> ' + RotationString + '<br><br>';

            if (data['CycleRedundant'].length > 0) {
                CycleText += '<span style="color: #FF3333;">Redundant abilities: </span> ' + RedundantAbilities.replace(/,/g, ', ') + "<br><br>";
            }

            function tableCreate() {
              let tt = '<table style="">';
              let headText = ['Source', 'activations', 'damage', '% of total damage'];
              let key;

              for(let i = 0; i < Object.keys(data['AbilityInfo']).length + 1; i++){
                  tt += '<tr>';
                  if (i !== 0) {
                      key = Object.keys(data['AbilityInfo'])[i-1];
                  }
                  for(let j = 0; j < 4; j++){
                      if (i === 0) {
                          tt += '<th style="border: 1px solid #999999;">' + headText[j] + '</th>';
                      } else {
                          if (j === 0) {
                              tt += '<td style="border: 1px solid #999999;">' + key + '</td>';
                          } else if (j === 1) {
                              tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + data['AbilityInfo'][key]['activations'] + '</span>' + '</td>';
                          } else if (j === 2) {
                              tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + parseFloat(data['AbilityInfo'][key]['damage']).toFixed(2) + '</span>' + '</td>';
                          } else if (j === 3) {
                              tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + parseFloat(data['AbilityInfo'][key]['shared%']).toFixed(2) + '</span>' + '</td>';
                          }
                      }
                  }
                  tt += '</tr>';
              }
              tt += '</table>';
              return tt;
            }

            let AbilityTable = tableCreate();

            CycleText += '<span style="color: #FF3333;">' + Type + ' Ability Information: </span> <br><br>';

            CycleText += AbilityTable + '<br><br>';

            CycleText += '<span style="color: #FF3333; font-size: small;">Python Script Execution Time: </span><span style="font-size:small;">' + data['ExecutionTime'] + "s</span><br>";
            CycleText += '<span style="color: #FF3333; font-size: small;">Simulation Time: </span><span style="font-size:small;">' + (parseFloat(data['SimulationTime']) * 0.6).toFixed(1) + "s --> " + data['SimulationTime'] + ' ticks</span><br>';

            // if theres a warning, extend the message
            if (data['warning'].length !== 0) {
                resultCard.hidden = true;
                resultCardWarning.hidden = false;
                resultCardDanger.hidden = true;

                // for every warning
                for (let i = 0; i < data['warning'].length; i++) {
                    message += "<br>" + data['warning'][i];
                }

                message += '</span>';

                // print the message in the right place
                document.getElementById('result-text-warning').innerHTML = message;
            } else {
                resultCard.hidden = false;
                resultCardWarning.hidden = true;
                resultCardDanger.hidden = true;

                // print the message in the right place
                document.getElementById('result-text').innerHTML = message;
            }


            // the loop text which shows what happens for each tick
            let LoopText = data['LoggerText'];

            document.getElementById('result-card-extra').innerHTML = CycleText + LoopText;

            // if (DPTNote.style.maxHeight && DPTNoteOut == true){
            //     DPTNote.style.maxHeight = DPTNote.scrollHeight + "px";
            // }
          })
      })
      //       // if its the second time the user clicked on the calc button (or more) , do nothing
      //       if (AlreadyRan) {
      //           return;
      //       } else { // else roll-out the results box
      //           outputNote.style.maxHeight = outputNote.scrollHeight + "px";
      //           AlreadyRan = true;
      //       }
      //   });
      // }
    },

    showExtra: function () {
      let resultCardExtra = document.getElementById('result-card-extra');
      resultCardExtra.hidden = !resultCardExtra.hidden;
    }
  }
}
</script>

<style scoped>
  /* Attack */
  .attbox {
      display: flex;
      flex-direction: row;
      background-color: var(--attColor);
      height: 75px;
      width: 1045px;
      border: 2.5px solid var(--attColor);
  }
  .att {
      width: 70px;
      height: 70px;
      border: 5px solid var(--attColor);
  }
  /* Strength */
  .strbox {
      display: flex;
      flex-direction: row;
      background-color: var(--strColor);
      height: 75px;
      width: 1045px;
      border: 2.5px solid var(--strColor);
  }
  .str {
      width: 70px;
      height: 70px;
      border: 5px solid var(--strColor);
  }
  /* Magic */
  .magbox {
      display: flex;
      flex-direction: row;
      background-color: var(--magColor);
      height: 75px;
      width: 1045px;
      border: 2.5px solid var(--magColor);
  }
  .mag {
      width: 70px;
      height: 70px;
      border: 5px solid var(--magColor);
  }
  /* Ranged */
  .ranbox {
      display: flex;
      flex-direction: row;
      background-color: var(--ranColor);
      height: 75px;
      width: 1045px;
      border: 2.5px solid var(--ranColor);
  }
  .ran {
      width: 70px;
      height: 70px;
      border: 5px solid var(--ranColor);
  }
  .conbox {
    display: flex;
    flex-direction: row;
    background-color: var(--conColor);
    height: 75px;
    width: 1045px;
    border: 2.5px solid var(--conColor);
  }
  .con {
    width: 70px;
    height: 70px;
    border: 5px solid var(--conColor);
  }
  .defbox {
    display: flex;
    flex-direction: row;
    background-color: var(--defColor);
    height: 75px;
    width: 1045px;
    border: 2.5px solid var(--defColor);
  }
  .def {
      width: 70px;
      height: 70px;
      border: 5px solid var(--defColor);
  }
  .AbilBlock {
    margin: auto;
    width: 1045px; /* 989 */
    height: 300px; /* 314 */
  }
  .AbilType {
    color: #000000;
    display: flex;
    width: 200px;
    height: 70px;
    justify-content: center;
    align-items: center;
    font-size: 15px;
    font-family: "Lucida Console", Courier, monospace;
  }
  .Ability {
    transition: 0.05s;
  }
  .Ability:hover{
    border: 0 solid #FFFFFF;
    box-shadow: 0 0 5px 5px #FFFFFF, 0 0 5px 5px #000000;
    transform: scale(1.1);
    cursor: grab;
  }
  .Ability:active{
    transform: scale(1);
  }
  .content {
    display: block;
    overflow: hidden;
    max-height: 0;
    transition: max-height 0.3s ease-out;
  }
  .OptionBlock {
    margin: auto;
    width: 1100px;
    height: 560px;
  }
  /* Options */
  .optsect {
      display: flex;
      flex-direction: column;
      background-color: #343A40;
      float: left;
      margin: auto;
      width: 200px;
      height: 560px;
      color: white;  /*var(--textColor2);*/
  }
  .optsect .switch {
    text-align: left;
    margin-left: 15px;
  }
  /* Hide the browser's default checkbox */
  .SingleOpt input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
      height: 0;
      width: 0;
  }
  .OptSelect select {
      text-align: center;
      border: 1px solid black;
      background-color: #eee;
  }
  .OptText input {
      display: inline-block;
      width: 60px;
      height: 24px;
      text-align: center;
      border: 1px solid black;
      background-color: #eee;
  }
  /* Revolution Bar */
  #RevolutionBar {
    background-color: #6C757D;
    width: 876px;
    height: 70px;
    max-width: 1200px;
    margin: auto;
    border: 5px solid var(--bar-border-color);
  }
  .RevoBar {
    display: inline-block;
    float: left;
    width: 62px;
    height: 60px;
    border-left: 1px solid #373737;
    border-right: 1px solid #373737;
  }
  .accordion {
    display: inline-block;
    width: 750px;
  }
  .output-card {
    margin-top: 20px;
    display: inline-block;
    width: 500px;
    height: 150px;
    cursor: pointer;
  }
  .output-card-extra {
    margin-top: 20px;
    padding: 15px;
    text-align: left;
    display: inline-block;
    width: 800px;
  }
  #result-text-extra {
    width: inherit;
    display: inline-block;
  }
  .accordion-button {
    height: 30px;
    width: 220px;
    display: flex;
    justify-content: center; /* align horizontal */
    align-items: center; /* align vertical */
  }
  .accordion-button-group {
    display: flex;
    width: 100%;
  }
  #card-header {
    margin-top: 20px;
  }
  .user-select-button-group {
    display: block;
    margin-top: 20px;
  }
  #clear-button {
    display: block;
    margin-top: 10px;
  }
  #calc-button {
    display: block;
    margin-top: 20px;
  }
  #counter {
    margin-top: 20px;
    color: white;
    font-size: 11px;
  }
</style>