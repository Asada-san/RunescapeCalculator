<template>
  <div>
    <b-button id="sidebar-button" v-b-toggle.sidebar-backdrop>☰</b-button>

    <b-sidebar id="sidebar-backdrop" no-header title="Page selection" bg-variant="dark" text-variant="white" backdrop-variant="secondary" backdrop shadow>
      <div class="px-3 py-2">
        <b-nav vertical>
          <h4 id="sidebar-no-header-title">Page selection</h4>
          <b-nav-item link-classes="text-light" @click="changeComponent('RevoCalc')">Revolution</b-nav-item>
<!--          <b-nav-item link-classes="text-light" @click="changeComponent('AbilRot')">Rotation</b-nav-item>-->
          <b-nav-item link-classes="text-light" @click="changeComponent('ItemIDs')">Item IDs</b-nav-item>
<!--          <b-nav-item link-classes="text-light" @click="changeComponent('LinkList')">Links</b-nav-item>-->
          <b-nav-form style="margin-top:50px;">
            <b-form-input id="search-input" size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button id="search-button" size="sm" class="my-2 my-sm-0" @click="searchDDG">Search</b-button>
          </b-nav-form>
        </b-nav>
      </div>

      <template #footer="{ hide }">
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <strong class="mr-auto"></strong>
          <b-button size="sm" @click="hide">Close</b-button>
        </div>
      </template>
    </b-sidebar>

    <component :change-component="changeComponent" :is="currentComponent"></component>
  </div>
</template>

<script>
import RevoCalc from './RevoCalc.vue'
import ItemIDs from './itemids.vue'
import LinkList from './LinkList.vue'

let lastComponent;

if (localStorage.component !== undefined) {
  lastComponent = localStorage.component;
} else {
  lastComponent = RevoCalc;
}

export default {
  name: "NavBar",
  data: function () {
    return {
      currentComponent: lastComponent,
    }
  },
  methods: {
    changeComponent: function (component) {
      if (this.currentComponent !== component) {
        this.currentComponent = component;
        localStorage.component = component;
      }
    },

    searchDDG: function () {
      let searchEngineString = 'https://duckduckgo.com/?q=' + document.getElementById('search-input').value.replace(/ /g, '+')

      window.open(searchEngineString, "_blank");
    }
  },
  components: {
    ItemIDs,
    RevoCalc,
    LinkList
  }
}
</script>

<style scoped>

#sidebar-button {
  position: absolute;
  left: 10px;
  top: 10px;
}

</style>