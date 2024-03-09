<template>
  <div :style="centerStyle">
    <b-card no-body class="mb-1" id="card-header" bg-variant="dark" text-variant="white" style="text-align: left;">
      <h2 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Item IDs (tradeable)</h2>
      <p style="text-align: center;">
          Last updated: 7-5-2022
      </p>
      <p style="text-align: center; margin-left: 15px; margin-right: 15px; color: pink;">If this list needs an update, contact me on discord:
        <a style="color: #4CAF50" href="https://discordapp.com/users/713459040386023579"><strong>Micky#5858</strong></a>.
      </p>
    </b-card>

    <div id="download-button">
      <b-button :href="url" variant="secondary">Download .json</b-button>
    </div>

    <div>
      <b-card @click="showIDs" no-body class="mb-1" id="card-item-id-json" bg-variant="dark" text-variant="white">
        <b-card-text id="card-item-id-json-text">click to show json</b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
let getItemIDs = true;

let origin
if (window.origin === 'http://localhost:8080') {
  origin = 'http://localhost:5000';
} else {
  origin = window.origin;
}

export default {
  name: "ItemIds",
  data: function () {
    return {
      centerStyle: {
        alignItems: 'center',
        textAlign: 'center'
      },
      url: `${origin}/api/downloadJSON`
    }
  },
  methods: {
    showIDs: async function () {
      if (getItemIDs) {
        await fetch(`${origin}/api/itemIDs`, {
          method: "GET",
          'cache-control': "no-cache",
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
            // console.log(data)
            let textCard = document.getElementById('card-item-id-json');
            textCard.innerHTML = `<pre style="color: white; text-align: left;">${JSON.stringify(data, null, 2)}</pre>`;
            textCard.style.cursor = 'auto';
            getItemIDs = false;
          })
        })
      }
    }
  }
}
</script>

<style scoped>
  #card-header {
    margin-top: 20px;
    width: 750px;
    display: inline-block;
  }
  #card-item-id-json {
    cursor: pointer;
    margin-top: 20px;
    width: 500px;
    padding: 15px;
    display: inline-block;
  }
  #download-button {
    margin-top: 20px;
  }
</style>