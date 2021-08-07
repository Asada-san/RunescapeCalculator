<template>
  <div :style="centerStyle">
    <b-card no-body class="mb-1" id="card-header" bg-variant="dark" text-variant="white" style="text-align: left;">
      <h2 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Item IDs (tradeable)</h2>
      <p style="text-align: center;">
          Last updated: 27-6-2021
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

export default {
  data: function () {
    return {
      centerStyle: {
        alignItems: 'center',
        textAlign: 'center'
      },
      url: 'http://localhost:5000/api/downloadJSON'
    }
  },
  methods: {
    showIDs: async function () {
      if (getItemIDs) {
        await fetch("http://localhost:5000/api/itemIDs", {
          method: "GET",
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
            // console.log(data)
            let textCard = document.getElementById('card-item-id-json');
            textCard.innerHTML = `<pre style="color: white; text-align: left;">${JSON.stringify(data, null, 2)}</pre>`;
            textCard.style.cursor = 'auto';
            getItemIDs = false;
          })
        })
      }
    }
  },
  name: "itemids"
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