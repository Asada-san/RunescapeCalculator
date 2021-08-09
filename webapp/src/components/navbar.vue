<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="#" v-b-tooltip.hover.right="'Doesn\'t work'">Home</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item @click="changeComponent('RevoCalc')">Revolution</b-nav-item>
          <b-nav-item @click="changeComponent('ItemIDs')">Item ID's</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input id="search-input" size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button id="search-button" size="sm" class="my-2 my-sm-0" @click="searchDDG" type="submit">Search</b-button>
          </b-nav-form>

<!--          <b-nav-item-dropdown text="Lang" right>-->
<!--            <b-dropdown-item href="#">EN</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">ES</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">RU</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">FA</b-dropdown-item>-->
<!--          </b-nav-item-dropdown>-->

<!--          <b-nav-item-dropdown right>-->
<!--            &lt;!&ndash; Using 'button-content' slot &ndash;&gt;-->
<!--            <template #button-content>-->
<!--              <em>User</em>-->
<!--            </template>-->
<!--            <b-dropdown-item href="#">Profile</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">Sign Out</b-dropdown-item>-->
<!--          </b-nav-item-dropdown>-->
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <component :change-component="changeComponent" :is="currentComponent"></component>
  </div>
</template>

<script>
import RevoCalc from './RevoCalc.vue'
import ItemIDs from './itemids.vue'

let lastComponent;

if (localStorage.component !== undefined) {
  lastComponent = localStorage.component;
} else {
  lastComponent = RevoCalc;
}
// lastComponent = localStorage.component;

export default {
  name: "navbar",
  data: function(){
    return {
      currentComponent: lastComponent
    }
  },
  methods: {
    changeComponent: function (component) {
      this.currentComponent = component;
      localStorage.component = component;
    },
    searchDDG: function () {
      let searchEngineString = 'https://duckduckgo.com/?q=' + document.getElementById('search-input').value.replace(/ /g, '+')

      window.open(searchEngineString, "_blank");
    }
  },
  components: {
      ItemIDs,
      RevoCalc
  }
}
</script>

<style scoped>

</style>