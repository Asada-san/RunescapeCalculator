<template>
  <div id="app">
    <navbar />
<!--    <RevoCalc v-if="page === 'RevoCalc'"/>-->
<!--    <ItemIDs v-if="page === 'ItemIDs'"/>-->
<!--    <ItemIDs />-->
<!--    <p>{{ greeting }}</p>-->
<!--    <p>{{ flaskGreeting }}</p>-->
  </div>
</template>

<script>
import navbar from './components/navbar.vue'

export default {
    // components: {
    //     logo
    // },
    data: function(){
        return {
            // greeting: 'Hello, Vue!',
            // flaskGreeting: ''
        }
    },
    // created: async function(){
    //     const gResponse = await fetch("http://localhost:5000/greeting");
    //     const gObject = await gResponse.json();
    //     this.flaskGreeting = gObject.greeting;
    // },
    components: {
      navbar, // register component=
    }
}

document.title = 'Runescape';
document.body.style.backgroundColor = '#1D1F21';
</script>

<style>
:root {
  --main-bg-color: #383838;
  --note-bg-color: #484848;
  --note-border: 0 0 2px 5px #282828;
  --note-button-bg-color: #606060;
  --note-button-bg-color-hover: 	#505050;
  --button-bg-color: #4CAF50;
  --button-bg-color-hover: #15811A;
  --button-text-color: #FFFFFF;
  --border-color: #101010;
  --bar-slot-bg-color: #808080;
  --bar-border-color: #FFCB05;
  --attColor: #FFD700;
  --strColor: #FFA500;
  --magColor: #00008B;
  --ranColor: #006400;
  --conColor: #A80000;
  --defColor: #6C757D;
  --textColor1: #D0D0D0;
  --textColor2: #000000;
}
#app {

}
</style>
