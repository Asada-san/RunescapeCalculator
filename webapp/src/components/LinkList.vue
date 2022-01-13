<template>
<div id="vue-instance">
  <div id="search-options">
    <b-form-input @keyup="searchResults(message)" v-model="message" size="sm" class="mt-1" id="input-search" placeholder="edit me"></b-form-input>
    <b-form-checkbox @change="clearSearch(true)" class="switch mt-1" id="input-search-switch" v-model="searchHeader" switch v-b-tooltip.hover.top="'When checked, search through headers, otherwise search through all the links'"></b-form-checkbox>
  </div>

  <div class="card-list">
    <b-card no-body v-for="(item, index) in ListData"
            v-b-toggle="item.name.replace(/\s+/g, '-').toLowerCase()"
            :item="item.name"
            :key="index"
            :header="item.name"
            bg-variant="dark"
            text-variant="white"
            class="text-center card-item">
      <b-collapse :id="item.name.replace(/\s+/g, '-').toLowerCase()" class="mt-2">
        <b-list-group flush>
          <b-list-group-item v-for="(link, idx) in item.links"
                             :key="item.name + idx"
                             @click=openLink(link.url)
                             variant="secondary"
                             class="subtopic-items">{{ link.name }}</b-list-group-item>
        </b-list-group>
      </b-collapse>
    </b-card>
  </div>
</div>
</template>

<script>
export default {
  name: "LinkList",
  data: function() {
    return {
      message: '',
      searchHeader: false,
      ListData: [
        {name: 'Twitter mods',
          links: [{
            name: 'Luna',
            url: 'https://twitter.com'
          }, {
            name: 'Nick',
            url: 'https://twitter.com'
          }, {
            name: 'Jack',
            url: 'https://twitter.com'
          }]},
        {name: 'Youtube creators',
          links: [{
            name: 'Luna',
            url: 'https://Youtube.com'
          }, {
            name: 'Nick',
            url: 'https://Youtube.com'
          }, {
            name: 'Jack',
            url: 'https://Youtube.com'
          }, {
            name: 'Jack2',
            url: 'https://Youtube.com'
          }]},
        {name: 'Spreadsheets',
          links: [{
            name: 'Luna',
            url: 'https://nu.nl'
          }, {
            name: 'Nick',
            url: 'https://nu.nl'
          }, {
            name: 'Jack',
            url: 'https://nu.nl'
          }, {
            name: 'Nick2',
            url: 'https://nu.nl'
          }, {
            name: 'Jack2',
            url: 'https://nu.nl'
          }]},
        {name: 'Official',
          links: [{
            name: 'Luna',
            url: 'https://runescape.com'
          }, {
            name: 'Nick',
            url: 'https://runescape.com'
          }, {
            name: 'Jack',
            url: 'https://runescape.com'
          }, {
            name: 'Rick',
            url: 'https://runescape.com'
          }]}
      ]
    }
  },
  methods: {
    openLink: function (link) {
      // Opens link in a new tab.
      window.open(link, '_blank');
    },
    searchResults: function (input) {
      let SubLinks = document.getElementsByClassName("subtopic-items");
      let SubItems = document.getElementsByClassName("card-item");

      if (input.length > 2) {
        if (!this.searchHeader) {
          for (let i = 0; i < SubLinks.length; i++) {
            SubLinks[i].hidden = !SubLinks[i].innerHTML.includes(input);
          }

          for (let i = 0; i < SubItems.length; i++) {
            let isHidden = true;

            for (let j = 0; j < SubItems[i].children[1].children[0].children.length; j++) {
              if (!SubItems[i].children[1].children[0].children[j].hidden) {
                isHidden = false;
              }
            }

            SubItems[i].hidden = isHidden;
          }
        } else {
          for (let i = 0; i < SubItems.length; i++) {
            SubItems[i].hidden = !SubItems[i].children[0].innerHTML.includes(input);
          }
        }
      } else {
        this.clearSearch(false);
      }
    },
    clearSearch: function (clear) {
      let SubLinks = document.getElementsByClassName("subtopic-items");
      let SubItems = document.getElementsByClassName("card-item");

      if (clear) {
        this.message = '';
      }

      if (!this.searchHeader) {
        for (let i = 0; i < SubLinks.length; i++) {
          SubLinks[i].hidden = false;
        }
      }

      for (let i = 0; i < SubItems.length; i++) {
        SubItems[i].hidden = false;
      }
    }
  }
}
</script>

<style scoped>

#vue-instance {
  display: block;
  margin: 10px auto;
  text-align: center;
}

#search-options {
  display: inline-block;
}

#input-search {
  display: inline-block;
  width: 200px;
}

#input-search-switch {
  display: inline-block;
}

.card-list {
  display: block;
  width: 400px;
  margin: 10px auto;
}

.card-item {
  padding: 2px;
}

</style>