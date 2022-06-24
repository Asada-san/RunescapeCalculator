<template>
  <div :style="centerStyle">
    <div class="accordion" role="tablist">
      <b-card no-body class="mb-1" id="card-header" bg-variant="dark" text-variant="white" style="text-align: left;">
        <h2 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Revolution Bar <span v-html="latestVersion" style="font-size:small;"></span></h2>
        <p style="text-align: center; margin-left: 15px; margin-right: 15px; color: pink;">Stuff may be broken, I'm working on it (slowly).
<!--          If something seems broken, do not hesitate to contact me on discord:-->
<!--          <a style="color: #4CAF50" href="https://discordapp.com/users/713459040386023579"><strong>Micky#5858</strong></a>.-->
        </p>

        <b-card no-body class="mb-0" bg-variant="dark" text-variant="white" >
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button-group class="accordion-button-group">
              <b-button v-b-toggle.accordion-1 class="accordion-button" variant="secondary">General Info</b-button>
              <b-button v-b-toggle.accordion-2 class="accordion-button" variant="secondary">Important Notes</b-button>
              <b-button class="accordion-button" variant="secondary" @click="changelogVisibility(false)">Changelog</b-button>
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
                  Discord: <a style="color: #4CAF50" href="https://discordapp.com/users/713459040386023579"><strong>Micky#5858</strong></a>,
                  Reddit: <a style="color: #4CAF50" href="https://www.reddit.com/user/ftwmickywtf"><strong>u/FTWmickyWTF</strong></a> or ingame:
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
                  <li>All ability information used to determine the AADPT is summarized on a <a href="https://github.com/Asada-san/RunescapeCalculator/blob/master/api/AbilityInfo.xlsx" target="_blank" style="color: #4CAF50"><strong>spreadsheet</strong></a>.</li>
                  <li>The code (including html, js, css and python files) have been uploaded to <a href="https://github.com/Asada-san/RunescapeCalculator" target="_blank" style="color: #4CAF50"><strong>Github</strong></a>. You're free to use it however you want.</li>
                  <li>All ability images were yoinked from the RS3 wiki.</li>
                </ul>
              </b-card-text>
            </b-card-body>
          </b-collapse>

<!--          <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">-->
<!--            <b-card-body>-->
<!--              <b-card-text id="changelog-card"></b-card-text>-->
<!--              <div style="text-align: center;">-->
<!--                <b-button @click="changelogVisibility(true)" variant="secondary">Show more</b-button>-->
<!--              </div>-->
<!--            </b-card-body>-->
<!--          </b-collapse>-->
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
      <b-dropdown text="Charts" variant="secondary">
        <b-dropdown-item v-on:click="displayChart(0)" switch v-b-tooltip.hover.right="'Displays the total damage over time'">Total damage</b-dropdown-item>
        <b-dropdown-item v-on:click="displayChart(1)" switch v-b-tooltip.hover.right="'Displays the total damage over time per ability'">Total damage per ability</b-dropdown-item>
        <b-dropdown-item v-on:click="displayChart(2)" switch v-b-tooltip.hover.right="'Displays the total damage per tick over time'">Total damage per tick</b-dropdown-item>
        <b-dropdown-item v-on:click="displayChart(3)" switch v-b-tooltip.hover.right="'Displays the total damage taken per dummy'">Total damage per dummy</b-dropdown-item>
      </b-dropdown>
    </b-button-group>

    <div id="attAbils" class="scrollContent AbilBlock" style="margin-top:20px;">
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
<!--        <div class="att">-->
<!--          <img :src="require('@/assets/AbilityImages/Bladed_Dive.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Bladed_Dive" alt="Bladed_Dive" width="60" height="60" @click="abilClick($event)" title="Bladed Dive">-->
<!--        </div>-->
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
<!--        <div class="att">-->
<!--          <img :src="require('@/assets/AbilityImages/Balanced_Strike.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Balanced_Strike" alt="Balanced_Strike" width="60" height="60" @click="abilClick($event)" title="Balanced Strike">-->
<!--        </div>-->
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

    <div id="strAbils" class="scrollContent AbilBlock">
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

    <div id="magAbils" class="scrollContent AbilBlock">
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
<!--        <div class="mag">-->
<!--          <img :src="require('@/assets/AbilityImages/Surge.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Surge" alt="Surge" width="60" height="60" @click="abilClick($event)" title="Surge">-->
<!--        </div>-->
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Chain.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Chain" alt="Chain" width="60" height="60" @click="abilClick($event)" title="Chain">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Greater_Chain.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Greater_Chain" alt="Greater_Chain" width="60" height="60" @click="abilClick($event)" title="Greater Chain">
        </div>
        <div class="mag">
          <img :src="require('@/assets/AbilityImages/Magma_Tempest.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Magma_Tempest" alt="Magma_Tempest" width="60" height="60" @click="abilClick($event)" title="Magma Tempest">
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

    <div id="ranAbils" class="scrollContent AbilBlock">
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
<!--        <div class="ran">-->
<!--          <img :src="require('@/assets/AbilityImages/Escape.png')" class="Ability" draggable="true" @dragstart="drag($event)" id="Escape" alt="Escape" width="60" height="60" @click="abilClick($event)" title="Escape">-->
<!--        </div>-->
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

    <div id="conAbils" class="scrollContent AbilBlock">
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

    <div id="defAbils" class="scrollContent AbilBlock">
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

    <div id="optBlock" class="scrollContent OptionBlock" style="margin-bottom: 20px;">
      <form id="optmenu" name="optmenu" method="get">
        <div class="optsect" style="width: 20px;"></div>

        <div id="AbilityOptions1" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Strength Boost</p>
          <b-form-input size="sm" class="mt-1" id="StrengthLevel" v-model="StrengthLevel" placeholder="Strength Level" type="number" min="1" max="99" v-b-tooltip.hover.right="'Base Strength level (min:1, max:99)'"></b-form-input>
          <b-form-input size="sm" class="mt-1" id="StrengthBoost" placeholder="Strength Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'Boosted Strength levels due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
          <b-form-select class="mt-1" id="StrengthPrayer" v-model="StrengthPrayer" :options="optStrengthPrayer" size="sm"></b-form-select>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Magic Boost</p>
          <b-form-input size="sm" class="mt-1" id="MagicLevel" v-model="MagicLevel" placeholder="Magic Level" type="number" min="1" max="99" v-b-tooltip.hover.right="'Base Magic level due to potions and/or aura\'s (min:1, max:99)'"></b-form-input>
          <b-form-input size="sm" class="mt-1" id="MagicBoost" placeholder="Magic Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'Boosted Magic levels due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
          <b-form-select class="mt-1" id="MagicPrayer" v-model="MagicPrayer" :options="optMagicPrayer" size="sm"></b-form-select>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Ranged Boost</p>
          <b-form-input size="sm" class="mt-1" id="RangedLevel" v-model="RangedLevel" placeholder="Ranged Level" type="number" min="1" max="99" v-b-tooltip.hover.right="'Base Ranged level due to potions and/or aura\'s (min:1, max:99)'"></b-form-input>
          <b-form-input size="sm" class="mt-1" id="RangedBoost" placeholder="Ranged Level Boost" type="number" min="0" max="60" v-b-tooltip.hover.right="'Boosted Ranged levels due to potions and/or aura\'s (min:0, max:60)'"></b-form-input>
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

          <b-form-input class="mt-1" size="sm" id="MainHand" type="text" v-model="MainHand" list="mainHands" placeholder="Main-hand"></b-form-input>
          <datalist id="mainHands">
            <option v-for="mainHand in mainHandList" :key="mainHand.value">{{mainHand}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="OffHand" type="text" v-model="OffHand" list="offHands" placeholder="Off-hand"></b-form-input>
          <datalist id="offHands">
            <option v-for="offHand in offHandList" :key="offHand.value">{{offHand}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Ring" type="text" v-model="Ring" list="rings" placeholder="Ring"></b-form-input>
          <datalist id="rings">
            <option v-for="ring in ringList" :key="ring.value">{{ring}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Aura" type="text" v-model="Aura" list="auras" placeholder="Aura"></b-form-input>
          <datalist id="auras">
            <option v-for="aura in auraList" :key="aura.value">{{aura}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Cape" type="text" v-model="Cape" list="capes" placeholder="Cape"></b-form-input>
          <datalist id="capes">
            <option v-for="cape in capeList" :key="cape.value">{{cape}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Pocket" type="text" v-model="Pocket" list="pockets" placeholder="Pocket"></b-form-input>
          <datalist id="pockets">
            <option v-for="pocket in pocketList" :key="pocket.value">{{pocket}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Ammo" type="text" v-model="Ammo" list="ammos" placeholder="Ammo"></b-form-input>
          <datalist id="ammos">
            <option v-for="ammo in ammoList" :key="ammo.value">{{ammo}}</option>
          </datalist>

          <b-form-input class="mt-1" size="sm" id="Gloves" type="text" v-model="Gloves" list="Glovess" placeholder="Gloves"></b-form-input>
          <datalist id="Glovess">
            <option v-for="gloves in glovesList" :key="gloves.value">{{gloves}}</option>
          </datalist>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Bash Ability</p>
          <b-form-input size="sm" class="mt-1" id="DefenceLevel" placeholder="Defence Level" type="number" min="0" max="200" v-b-tooltip.hover></b-form-input>
          <b-form-input size="sm" class="mt-1" id="ShieldArmourValue" placeholder="Shield Armour Value" type="number" min="0" max="1000" v-b-tooltip.hover></b-form-input>
        </div>

        <div class="optsect" style="width: 10px;"></div>

        <div id="DummyOptions" class="optsect">
          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Anachronia cape stand</p>
          <b-form-checkbox class="switch mt-1" id="AnachroniaCapeStand" v-model="AnachroniaCapeStand" switch v-b-tooltip.hover.right="'Dismember\'s damage over time lasts an extra 3.6 seconds (an extra 3 hits for a total of 8)'">Strength Cape</b-form-checkbox>

          <p style="margin-left: 15px; margin-top: 15px; text-align: center; font-weight: bold;">Player</p>
          <b-form-checkbox class="switch mt-1" id="afkStatus" v-model="afkStatus" switch v-b-tooltip.hover.right="'Assumes the player breaks channeling abilities such that they still do all their damage (except for Concentrated Blast which cuts off after 2 hits) but the next ability is activated earlier'">Efficient</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="switchStatus" v-model="switchStatus" switch v-b-tooltip.hover.right="'Assumes the player switches between 2h/dual/shield whenever required for the next available ability'">Switcher</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="ringOfVigourPassive" v-model="ringOfVigourPassive" switch v-b-tooltip.hover.right="'TBD'">RoV passive</b-form-checkbox>

          <b-form-input size="sm" class="mt-1" id="baseDamage" placeholder="Ability Damage" type="number" min="1" max="10000" v-b-tooltip.hover.right="'The ability damage as calculated in the \'Calculating ability damage\' section on the RS3 wiki (Min:1, Max:10000)'"></b-form-input>

          <p style="margin-top: 15px; text-align: center; font-weight: bold;">Dummy</p>
          <b-form-checkbox class="switch mt-1" id="movementStatus" v-model="movementStatus" switch v-b-tooltip.hover.right="'Assumes the dummy is stuck in place, meaning bleed damage won\'t be multiplied. When not ticked, bleed damage is multiplied for all hits (unless the dummy is stunned and/or bound).'">Stationary</b-form-checkbox>
          <b-form-checkbox class="switch mt-1" id="stunbindStatus" v-model="stunbindStatus" switch v-b-tooltip.hover.right="'Assumes the dummy is immune to stuns and binds from abilities'">Stun&Bind Immune</b-form-checkbox>

          <b-form-input size="sm" class="mt-1" id="nTargets" placeholder="Number of Dummies" type="number" min="1" max="30" v-b-tooltip.hover.right="'Number of dummies affected by AoE abilities'"></b-form-input>
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
      <b-card hidden id="result-card" :header="resultCardHeader" :bg-variant="resultCardBackgroundVariant" :text-variant="resultCardTextColorVariant" class="text-center output-card result">
        <b-card-text @click="showExtra" id="result-text" class="result-card-text" v-b-tooltip.hover.right="'Click here for more in depth information!'"></b-card-text>

        <div @click="downloadData()" id="data-download-button" v-b-tooltip.hover.top="'Download data corresponding to current result'">
          <img :src="require('@/assets/download.png')" id="download-image-1" alt="download-image">
        </div>
      </b-card>

      <b-button-group hidden id="chart-buttons" class="user-select-button-group result">

      </b-button-group>
    </div>

    <b-card hidden @mousedown="startDrag($event, 0)" bg-variant="dark" text-variant="white" class="text-left output-card-chart result">
      <span class="close" v-on:click="displayChart(0)">&times;</span>
      <div class="container-100wh">
        <line-chart :chart-data="dataLineChart1"></line-chart>
      </div>
    </b-card>

    <b-card hidden @mousedown="startDrag($event, 1)" bg-variant="dark" text-variant="white" class="text-left output-card-chart result">
      <span class="close" v-on:click="displayChart(1)">&times;</span>
      <div class="container-100wh">
        <line-chart :chart-data="dataLineChart2"></line-chart>
      </div>
    </b-card>

    <b-card hidden @mousedown="startDrag($event, 2)" bg-variant="dark" text-variant="white" class="text-left output-card-chart result">
      <span class="close" v-on:click="displayChart(2)">&times;</span>
      <div class="container-100wh">
        <bar-chart :chart-data="dataBarChart1"></bar-chart>
      </div>
    </b-card>

    <b-card hidden @mousedown="startDrag($event, 3)" bg-variant="dark" text-variant="white" class="text-left output-card-chart result">
      <span class="close" v-on:click="displayChart(3)">&times;</span>
      <div class="container-100wh">
        <line-chart :chart-data="dataLineChart3"></line-chart>
      </div>
    </b-card>

    <b-card hidden id="result-card-extra" header="Result" bg-variant="dark" text-variant="white" class="text-left output-card-extra result">
    </b-card>

    <p id="counter"></p>

    <div id="changelogModal" class="OptionBlock" v-on:click="closeModalOutside($event)">

      <div class="modal-content">


        <span class="close" v-on:click="closeModal()">&times;</span>
<!--        <div class="optsect" style="width: 20px;"></div>-->
        <div id="changelogItem" style="margin-bottom: 20px"></div>
<!--        <b-button v-if="setAllButton" id="optSubmitAll" @click="setOptions(true)" variant="secondary">Set All</b-button>-->
        <b-button @click="changelogVisibility(true)" variant="secondary" style="position: absolute; width: 200px; right: 10px; bottom: 10px;">Show older</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from './LineChart.vue';
import BarChart from './BarChart.vue';
import { updateInfo } from '@/assets/js/Updates';

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

export default {
  components: {
    LineChart,
    BarChart
  },
  data: function() {
    return {
      ringList: [],
      Ring: '',
      mainHandList: [],
      MainHand: '',
      offHandList: [],
      OffHand: '',
      capeList: [],
      Cape: '',
      glovesList: [],
      Gloves: '',
      auraList: [],
      Aura: '',
      pocketList: [],
      Pocket: '',
      ammoList: [],
      Ammo: '',
      latestVersion: updateInfo[0]['version'],
      changelogOpen: false,
      kLog: 0,
      chartElements: document.getElementsByClassName("output-card-chart"),
      dataLineChart1: null,
      dataBarChart1: null,
      dataLineChart2: null,
      dataLineChart3: null,
      fightData: {},
      resultCardBackgroundVariant: 'dark',
      resultCardTextColorVariant: 'white',
      resultCardHeader: 'Result',
      dragData: {},
      poppedUp: Array(this.chartElements).fill(0),
      resized: Array(this.chartElements).fill(0),
      zIndexCharts: 1000,
      initData: {
        labels: [],
        datasets: [
          {
            label: 'data',
            data: [],
            fill: false,
            borderColor: '#4CAF50',
            backgroundColor: '#4CAF50',
            borderWidth: 1
          }
        ]
      },
      centerStyle: {
        alignItems: 'center',
        textAlign: 'center'
      },
      StrengthLevel: 99,
      StrengthPrayer: 1,
      optStrengthPrayer: [
        { value: 1, text: 'Strength Prayer', disabled: true, selected: true, hidden: true},
        { value: 1, text: 'none'},
        { value: 1.02, text: 'Burst of Strength'},
        { value: 1.04, text: 'Superhuman Strength'},
        { value: 1.06, text: 'Ultimate Strength'},
        { value: 1.08, text: 'Piety'},
        { value: 1.10, text: 'Turmoil'},
        { value: 1.12, text: 'Malevolence'}
      ],
      MagicLevel: 99,
      MagicPrayer: 1,
      optMagicPrayer: [
        { value: 1, text: 'Magic Prayer', disabled: true, selected: true, hidden: true},
        { value: 1, text: 'none'},
        { value: 1.02, text: 'Charge'},
        { value: 1.04, text: 'Super Charge'},
        { value: 1.06, text: 'Overcharge'},
        { value: 1.08, text: 'Augury'},
        { value: 1.10, text: 'Torment'},
        { value: 1.12, text: 'Affliction'}
      ],
      RangedLevel: 99,
      RangedPrayer: 1,
      optRangedPrayer: [
        { value: 1, text: 'Ranged Prayer', disabled: true, selected: true, hidden: true},
        { value: 1, text: 'none'},
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
      AnachroniaCapeStand: { value: 'Strength Cape', text: 'Anachronia Strength Cape' },
      afkStatus: { value: 'afkStatus', text: 'Efficient' },
      switchStatus: { value: 'switchStatus', text: 'Switcher' },
      movementStatus: { value: 'movementStatus', text: 'Stationary' },
      ringOfVigourPassive: { value: 'ringOfVigourPassive', text: 'RoV Passive' },
      stunbindStatus: { value: 'stunbindStatus', text: 'Stun&Bind Immune' },
      HeightenedSenses: { value: 'HeightenedSenses', text: 'Heightened Senses' },
      FotS: { value: 'FotS', text: 'Fury of the Small' },
      CoE: { value: 'CoE', text: 'Conservation of Energy' },
      Debug: { value: 'Debug', text: 'Print more info' },
      ChartType: null,
      optChartType: [
        { value: null, text: 'Charts', disabled: true, selected: true, hidden: true},
        { value: null, text: 'none'},
        { value: 'Line', text: 'Line'},
        { value: 'Bar', text: 'Bar'}
      ]
    }
  },
  created: async function(){
    let vm = this; // Necessary so that "this" can still be used after server request

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

        vm.ringList = data['nameList']['Ring'];
        vm.mainHandList = data['nameList']['Main-hand'];
        vm.offHandList = data['nameList']['Off-hand'];
        vm.pocketList = data['nameList']['Pocket'];
        vm.glovesList = data['nameList']['Gloves'];
        vm.auraList = data['nameList']['Aura'];
        vm.capeList = data['nameList']['Cape'];
        vm.ammoList = data['nameList']['Ammo'];
      })
    })
    .catch((error) => {
      console.log(error);
      document.getElementById("counter").innerHTML = `Simulated fights: Unknown`;
    });
  },
  mounted () {
    // this.fillData()
  },
  methods: {
    closeModalOutside: function (event) {
      let modal = document.getElementById("changelogModal");

      if (event.target === modal) {
        this.closeModal();
      }
    },
    closeModal: function () {
      document.getElementById("changelogModal").style.display = "none";
      document.getElementById("changelogItem").innerHTML = '';
      this.kLog = 0;
    },
    fillData: function (option) {
      // option: Number of chart(s) that needs updating
      //  -1: All charts
      //   0: Line chart with total damage
      //   1: Line chart with total damage per ability
      //   2: Bar chart with total damage per tick
      //   3: Line chart with total damage per dummy

      let lineChartPointRadius = 3;

      // If no fights have been simulated yet
      if (Object.keys(this.fightData).length === 0) {
        if (!this.chartElements[0].hidden && [-1, 0].includes(option)) {
          this.dataLineChart1 = this.initData;
        }

        if (!this.chartElements[1].hidden && [-1, 1].includes(option)) {
          this.dataLineChart2 = this.initData;
        }

        if (!this.chartElements[2].hidden && [-1, 2].includes(option)) {
          this.dataBarChart1 = this.initData;
        }

        if (!this.chartElements[3].hidden && [-1, 3].includes(option)) {
          this.dataLineChart3 = this.initData;
        }

        return;
      }

      let nDataPoints = this.fightData['CycleTime'];

      if (nDataPoints > 100) {
        lineChartPointRadius = 0;
      }

      if (nDataPoints > 1000) {
        nDataPoints = 1000;
      }

      // Line chart with total damage
      if (!this.chartElements[0].hidden && [-1, 0].includes(option)) {
        this.dataLineChart1 = {
          labels: Array.from(Array(nDataPoints + 1).keys()),
          //labels: Array.from({length: }, (_, i) => i + 1),
          datasets: [
            {
              label: 'Total damage',
              data: this.fightData['CycleDamageIncrement'].slice(0, nDataPoints + 1),
              fill: false,
              borderColor: '#4CAF50',
              backgroundColor: '#4CAF50',
              borderWidth: 1,
              pointRadius: lineChartPointRadius
            }, {
              label: 'Trendline',
              data: Array.from({length: nDataPoints + 1}, (_, i) => i).map(x => x * this.fightData['AADPT']),
              fill: false,
              borderColor: '#900C3F',
              backgroundColor: '#900C3F',
              borderWidth: 1,
              pointRadius: 0
            }
          ]
        }
      }

      // Line chart with total damage per ability
      if (!this.chartElements[1].hidden && [-1, 1].includes(option)) {
        let lines = [];
        let colors = ['#FF9999', '#FFCC99', '#FFFF99', '#CCFF99', '#99FF99', '#99FFCC',
          '#99FFFF', '#99CCFF', '#9999FF', '#CC99FF', '#FF99FF', '#FF99CC', '#E0E0E0', '#FFFFFF'];
        let i = 0;

        // Create plot for every ability used in the rotation
        for (const key in this.fightData['AbilityInfoPerTick']) {
          lines.push({
            label: key,
            data: this.fightData['AbilityInfoPerTick'][key]['damage'].slice(0, nDataPoints + 1),
            fill: false,
            borderColor: colors[i],
            backgroundColor: colors[i],
            borderWidth: 1,
            pointRadius: lineChartPointRadius
          });

          i++;
        }

        this.dataLineChart2 = {
          labels: Array.from(Array(nDataPoints + 1).keys()),
          datasets: lines
        }
      }

      // Bar chart with total damage per tick
      if (!this.chartElements[2].hidden && [-1, 2].includes(option)) {
        this.dataBarChart1 = {
          labels: Array.from({length: nDataPoints}, (_, i) => i + 1),
          // labels: Array.from(Array(this.fightData['CycleDamagePerTick'].length).keys()),
          datasets: [
            {
              label: 'Damage',
              data: this.fightData['CycleDamagePerTick'].slice(0, nDataPoints),
              fill: false,
              borderColor: '#4CAF50',
              backgroundColor: '#4CAF50',
              borderWidth: 1
            }
          ]
        }
      }

      // Line chart with total damage per dummy
      if (!this.chartElements[3].hidden && [-1, 3].includes(option)) {
        let lines = [];
        let colors = ['#FF9999', '#FFCC99', '#FFFF99', '#CCFF99', '#99FF99', '#99FFCC',
                      '#99FFFF', '#99CCFF', '#9999FF', '#CC99FF', '#FF99FF', '#FF99CC',
                      '#E0E0E0', '#FFFFFF', '#FF9999', '#FFCC99', '#FFFF99', '#CCFF99',
                      '#99FF99', '#99FFCC', '#99FFFF', '#99CCFF', '#9999FF', '#CC99FF',
                      '#FF99FF', '#FF99CC', '#E0E0E0', '#FFFFFF', '#FF9999', '#FFCC99'];

        // Create plot for every ability used in the rotation
        let length = this.fightData['DamagePerDummy'].length
        for (let i = 0; i < length; i++) {
          if (this.fightData['DamagePerDummy'][i][this.fightData['DamagePerDummy'][i].length - 1] !== 0) {
            lines.push({
              label: 'Dummy ' + (i + 1),
              data: this.fightData['DamagePerDummy'][i].slice(0, nDataPoints + 1),
              fill: false,
              borderColor: colors[i],
              backgroundColor: colors[i],
              borderWidth: 1,
              pointRadius: lineChartPointRadius
            });
          }
        }

        this.dataLineChart3 = {
          labels: Array.from(Array(nDataPoints + 1).keys()),
          datasets: lines
        }
      }
    },
    collapse: function (id) {
      let ScrollIdx = id;

      let scrollContent = document.getElementsByClassName("scrollContent")

      let ScrollOut;

      // if the content is already showing
      if (scrollContent[ScrollIdx].style.maxHeight) {
        scrollContent[ScrollIdx].style.maxHeight = null;
        ScrollOut = false;
      } else { // else ScrollOut the content
        scrollContent[ScrollIdx].style.maxHeight = scrollContent[ScrollIdx].scrollHeight + "px";
        ScrollOut = true;
      }

      // depending on the action in the previous if-else statement:
      // if this is not the first button being clicked on and its not the same
      // button as last time
      if (LastIdx !== null && LastIdx !== ScrollIdx) {
        // basically do the opposite for the previous content compared to the new content
        if (ScrollOut) {
          scrollContent[LastIdx].style.maxHeight = null;
        } else {
          scrollContent[LastIdx].style.maxHeight = scrollContent[LastIdx].scrollHeight + "px";
        }
      }

      // update the button which has previously been clicked on
      LastIdx = ScrollIdx;
    },
    drag: function (event) {
      // Prevent weird shenanigans from happening when dragging the element
      event.dataTransfer.setData("abilityName", event.target.id);
    },
    allowDrop: function (event) {
      // Prevent weird shenanigans from happening when dropping the element
      event.preventDefault();
    },
    drop: function (event) {
      // Function for dropping abilities into the rev bar slot

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

      // Hide all the result elements
      let resultElements = document.getElementsByClassName("result");

      resultElements.forEach(element => {
        if (!element.hidden) {
          element.hidden = !element.hidden;
        }
      })
    },
    calcDPT: async function () {
      let resultCard = document.getElementById('result-card');
      let downloadButton = document.getElementById('data-download-button');

      let vm = this; // Necessary so that "this" can still be used after server request

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

            // Unhide result card
            resultCard.hidden = false;
            // if an error occured during calculating the DPT, print error
            if (data['error']) {
              downloadButton.hidden = true;

              vm.resultCardBackgroundVariant = 'danger';
              vm.resultCardTextColorVariant = 'white';
              vm.resultCardHeader = 'ERROR';

              message = data['error_message']

              document.getElementById('result-text').innerHTML = message;
              return;
            } else {
              downloadButton.hidden = false;
            }

            // Set current data as the global data since there is no error
            vm.fightData = data;

            // create a link using the DPT number, links to test page
            let linkStr = `<span style="color: #4CAF50;"><strong>${data['AADPT']} (${data['AADPTPercentage']}%)</strong></span>`;

            // CREATE A MESSAGE TO SHOW THE (AA)DPT
            if (data['CycleFound']) {
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
                vm.resultCardBackgroundVariant = 'warning';
                vm.resultCardTextColorVariant = 'black';
                vm.resultCardHeader = 'Result';

                // for every warning
                for (let i = 0; i < data['warning'].length; i++) {
                    message += "<br>" + data['warning'][i];
                }

                message += '</span>';
            } else {
                vm.resultCardBackgroundVariant = 'dark';
                vm.resultCardTextColorVariant = 'white';
                vm.resultCardHeader = 'Result';
            }

            // Print the message in the right place
            document.getElementById('result-text').innerHTML = message;


            // the loop text which shows what happens for each tick
            let LoopText = data['LoggerText'];

            document.getElementById('result-card-extra').innerHTML = CycleText + LoopText;

            vm.fillData(-1);

            let chartButtons = document.getElementById("chart-buttons");
            chartButtons.hidden = false;


            // if (DPTNote.style.maxHeight && DPTNoteOut == true){
            //     DPTNote.style.maxHeight = DPTNote.scrollHeight + "px";
            // }
          })
      })
      .catch((error) => {
        console.log(error);
        resultCard.hidden = false;

        // if an error occured during calculating the DPT, print error
        downloadButton.hidden = true;

        vm.resultCardBackgroundVariant = 'danger';
        vm.resultCardTextColorVariant = 'white';
        vm.resultCardHeader = 'ERROR';

        document.getElementById('result-text').innerHTML = 'Communication with server failed';
      });
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
    },
    changelogVisibility: function (showMore) {
      // showMore = true --> clicked on "show more" button within changelog card
      // showMore = false --> clicked on "Changelog"


      if (!showMore) {
        document.getElementById("changelogModal").style.display = "block";
      }

      // If everything is showing, return
      if (this.kLog === updateInfo.length) {
        return;
      }
      let updateToShow = updateInfo[this.kLog];

      let updateDiv = document.createElement("div");

      let title = document.createElement("p");
      title.innerHTML = updateToShow['version'] + ' - ' + updateToShow['date']

      title.style.marginTop = (10) + 'px';
      title.style.fontSize = (20) + 'px';
      title.style.fontWeight = 'bold';

      updateDiv.appendChild(title);

      let categories = updateToShow['items'];
      for (let i in categories) {
        let header = document.createElement("p");

        header.innerHTML = categories[i]['header'];

        header.style.marginTop = (10) + 'px';

        updateDiv.appendChild(header);

        let ul = document.createElement("ul");

        ul.style.marginTop = (10) + 'px';

        let subItems = categories[i]['subItems']
        for (let j in subItems) {
          let li = document.createElement("li");
          li.innerHTML = subItems[j];
          ul.appendChild(li);
        }

        updateDiv.appendChild(ul);
      }

      document.getElementById("changelogItem").appendChild(updateDiv);

      this.kLog++;
    },
    displayChart: function (option) {
      let chartCard = this.chartElements[option];

      if (!this.poppedUp[option]) {
        chartCard.style.left = ((window.innerWidth - 800)/2) + 'px';

        this.poppedUp[option] = 1;
      }

      chartCard.hidden = !chartCard.hidden;

      if (!chartCard.hidden) {
        chartCard.style.zIndex = ++this.zIndexCharts;
        this.fillData(option);
      }
    },
    downloadData: function () {
      //Convert JSON Array to string.
      let json = JSON.stringify(this.fightData);

      //Convert JSON string to BLOB.
      json = [json];
      let blob1 = new Blob(json, { type: "text/plain;charset=utf-8" });

      //Check the Browser.
      let isIE = !!document.documentMode;
      if (isIE) {
        window.navigator.msSaveBlob(blob1, "Data.json");
      } else {
        let url = window.URL || window.webkitURL;
        let link = url.createObjectURL(blob1);
        let a = document.createElement("a");
        a.download = "Data.json";
        a.href = link;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    },
    startDrag: function (e, option) {
      e.preventDefault();

      if (e.ctrlKey) {
        return;
      }

      this.dragData = {
        x: e.clientX,
        y: e.clientY,
        screenX: window.scrollX,
        screenY: window.scrollY,
        option: option,
        element: this.chartElements[option]
      };

      this.dragData['element'].style.zIndex = ++this.zIndexCharts;

      document.onmouseup = this.endDrag;
      document.onmousemove = this.onDrag;
    },
    onDrag: function(e) {
      e.preventDefault();

      let clientXdif = this.dragData['x'] - e.clientX;
      let clientYdif = this.dragData['y'] - e.clientY;
      let screenXdif = this.dragData['screenX'] - window.scrollX;
      let screenYdif = this.dragData['screenY'] - window.scrollY;

      let mousePosition = {
          x : clientXdif + screenXdif,
          y : clientYdif + screenYdif
      };

      this.dragData['x'] = e.clientX;
      this.dragData['y'] = e.clientY;
      this.dragData['screenX'] = window.scrollX;
      this.dragData['screenY'] = window.scrollY;

      this.dragData['element'].style.left = (this.dragData['element'].offsetLeft - mousePosition['x']) + 'px';
      this.dragData['element'].style.top = (this.dragData['element'].offsetTop - mousePosition['y']) + 'px';
    },
    endDrag: function () {
      document.onmouseup = null;
      document.onmousemove = null;
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
    width: 995px; /* 989 */
    height: 300px; /* 314 */
  }
  .AbilType {
    color: #000000;
    display: flex;
    width: 150px;
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
  .scrollContent {
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
  }
  .result-card-text {
    cursor: pointer;
  }
  .output-card-extra {
    margin-top: 20px;
    padding: 15px;
    text-align: left;
    display: inline-block;
    width: 800px;
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
  .container-100wh {
    width: 100%;
    height: 100%;
  }
  #data-download-button {
    position: absolute;
    width: 30px;
    height: 30px;
    cursor: pointer;
    top: 5px;
    right: 5px;
  }
  #download-image-1 {
    width: inherit;
    height: inherit;
  }
  .output-card-chart {
    z-index: 100;
    position: absolute;
    width: 800px;
    top: 25%;
    padding: 0;
    text-align: left;
    margin: auto;
    border: 1px solid #888;
    /*resize: both;*/
    /*overflow: auto;*/
  }

  #changelogModal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    background-color: #343A40; /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
  }


  /* Modal Content */
  .modal-content {
    background-color: #343A40;
    margin: auto;
    padding: 50px 20px;
    border: 1px solid #888;
    width: 900px;
  }

  #changelogItem {
    color: #fff;
    text-align: left;
    overflow: auto; /* Enable scroll if needed */
    max-height: 800px;
  }

  /* The Close Button */
  .close {
    position: absolute;
    top: 5px;
    right: 10px;
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .close:hover,
  .close:focus {
    color: #fff;
    text-decoration: none;
    cursor: pointer;
  }
</style>