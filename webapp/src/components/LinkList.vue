<template>
<div id="vue-instance">
  <b-button-group class="edit-buttons">
    <b-button v-if="edit" @click="showCreateModal = true" variant="secondary">create</b-button>
    <b-button v-if="edit" @click="saveItem()" variant="success">save</b-button>
    <b-button v-if="edit" @click="undoItem()" variant="primary">undo</b-button>
    <b-button v-if="edit" @click="redoItem()" variant="warning">redo</b-button>
    <b-button @click="edit = !edit" variant="danger">edit</b-button>
  </b-button-group>

  <b-form-input v-on:keyup.enter="getList()" v-model="listTitle" size="sm" class="mt-1" id="search-list" placeholder="Name of the list..."></b-form-input>

  <b-card id="search-options" :title="this.ListData.title" bg-variant="dark" text-variant="white" class="text-center">
<!--    <p v-if="edit">-->
<!--      {{ 'C' + this.ListData.nCategories }}-->
<!--      {{ 'L' + this.ListData.nLinks }}-->
<!--      {{ 'sC' + this.ListData.nSubCategories }}-->
<!--      {{ 'sL' + this.ListData.nSubLinks }}-->
<!--    </p>-->
    <b-card-text>
      <b-form-input @keyup="searchResults(message)" v-model="message" size="sm" class="mt-1" id="input-search" placeholder="Search the list..."></b-form-input>
      <b-button-group>
        <b-button type="submit" id="button-expand" @click="changeState(false)" variant="secondary">expand all</b-button>
        <b-button type="submit" id="button-collapse" @click="changeState(true)" variant="secondary">collapse all</b-button>
      </b-button-group>
    </b-card-text>
  </b-card>

  <div class="card-list">
    <b-card no-body v-for="(category, iCat) in ListData.categories"
            :item="category.name"
            :key="'A' + category.id"
            :id="'cat' + iCat"
            class="text-center categories"
            bg-variant="dark"
            text-variant="white"
            :draggable="edit"
            @dragstart="startDrag($event, 'category', iCat)"
            @drop="onDrop($event, 'category', iCat)"
            @dragover.prevent
            @dragenter.prevent>
      <b-card-header v-b-toggle="'T' + category.id" header-tag="header" class="p-2 category-header" role="tab">
        <b-badge v-if="edit" variant="danger" @click="deleteItem($event, 'category', iCat)" style="position: absolute; right: 10px; top: 10px;">&times;</b-badge>
        {{ category.name }}
      </b-card-header>

      <b-collapse :id="'T' + category.id" ref="collapsible" class="mt-2">
        <b-list-group>
          <b-list-group-item v-for="(link, iLink) in category.links"
                             :item="link.name"
                             :key="'A' + link.id"
                             :id="'link' + iLink"
                             class="links drop-zone" :class="'cat' + iCat + 'link'"
                             @click="openLink(link.url)"
                             variant="secondary"
                             :draggable="edit"
                             @dragstart="startDrag($event, 'link', iCat, iLink)"
                             @drop="onDrop($event, 'link', iCat, iLink)"
                             @dragover.prevent
                             @dragenter.prevent>
            <b-badge v-if="edit" variant="danger" @click="deleteItem($event, 'link', iCat, iLink)" style="position: absolute; right: 10px; top: 10px;">&times;</b-badge>
            {{ link.name }}
          </b-list-group-item>
          <b-list-group-item v-if="edit" variant="secondary" @click="addItem('link', iCat)">
            +++
          </b-list-group-item>

          <div v-for="(subCategory, iSubCat) in category.subCategories"
               :item="subCategory.name"
               :key="'C' + subCategory.id"
               :id="'subCat' + iSubCat"
               class="sub-categories" :class="'cat' + iCat + 'subCat'"
               :draggable="edit"
               @dragstart="startDrag($event, 'sub-category', iCat, null, iSubCat)"
               @drop="onDrop($event, 'sub-category', iCat, null, iSubCat)"
               @dragover.prevent
               @dragenter.prevent>
            <b-list-group-item v-b-toggle="'Ts' + subCategory.id" no-body variant="success" text-variant="white">
              <b-badge v-if="edit" variant="danger" @click="deleteItem($event, 'sub-category', iCat, null, iSubCat)" style="position: absolute; right: 10px; top: 10px;">&times;</b-badge>
              {{ subCategory.name }}
            </b-list-group-item>

            <b-collapse :id="'Ts' + subCategory.id" ref="collapsible">
              <b-list-group flush>
                <b-list-group-item v-for="(subLink, iSubLink) in subCategory.links"
                                   :item="subLink.name"
                                   :key="'D' + subLink.id"
                                   :id="'subLink' + iSubLink"
                                   class="sub-links" :class="['cat' + iCat + 'subLink', 'subCat' + iSubCat + 'subLink']"
                                   @click="openLink(subLink.url)"
                                   variant="secondary"
                                   :draggable="edit"
                                   @dragstart="startDrag($event, 'sub-link', iCat, null, iSubCat, iSubLink)"
                                   @drop="onDrop($event, 'sub-link', iCat, null, iSubCat, iSubLink)"
                                   @dragover.prevent
                                   @dragenter.prevent>
                  <b-badge v-if="edit" variant="danger" @click="deleteItem($event, 'sub-link', iCat, null, iSubCat, iSubLink)" style="position: absolute; right: 10px; top: 10px;">&times;</b-badge>
                  {{ subLink.name }}
                </b-list-group-item>
              </b-list-group>
              <b-list-group-item v-if="edit" variant="secondary" @click="addItem('sub-link', iCat, iSubCat)">
                +++
              </b-list-group-item>
            </b-collapse>
          </div>
          <b-card v-if="edit" no-body bg-variant="primary">
            <b-card-header @click="addItem('sub-category', iCat)">
              +++
            </b-card-header>
          </b-card>
        </b-list-group>
      </b-collapse>

    </b-card>

    <b-card v-if="edit" no-body bg-variant="dark" class="text-center categories-edit" text-variant="white" item="+++">
      <b-card-header @click="addItem('category')">
        +++
      </b-card-header>
    </b-card>
  </div>

  <!-- The Modal -->
  <div v-if="showCreateModal" id="create-modal" class="modal">

    <!-- Modal content -->
    <div class="modal-content">

      <span class="close" @click="closeModal()">&times;</span>
      <b-form-input v-model="listTitle" size="sm" class="mt-1" placeholder="name..."></b-form-input>
      <b-button type="submit" @click="createList()" variant="secondary">add</b-button>
    </div>

  </div>

  <!-- The Modal -->
  <div v-if="showModal" id="add-modal" class="modal">

    <!-- Modal content -->
    <div class="modal-content">

      <span class="close" @click="closeModal()">&times;</span>
      <b-form-input v-if="showName" v-model="itemName" size="sm" class="mt-1 addSubLink" placeholder="name..."></b-form-input>
      <b-form-input v-if="showURL" v-model="itemURL" size="sm" class="mt-1 addSubLink" placeholder="url..."></b-form-input>
      <b-button type="submit" @click="setItemAdd()" variant="secondary">add</b-button>
    </div>

  </div>

</div>
</template>

<script>
let origin
if (window.origin === 'http://localhost:8080') {
  origin = 'http://localhost:5000';
} else {
  origin = window.origin;
}

export default {
  name: "LinkList",
  // mounted:   this.$watch('list', function (value, mutation) {
  //   if (mutation) {
  //       mutation.method // e.g. 'push'
  //       mutation.args // raw arguments to the mutation method
  //       mutation.result // return value
  //       mutation.inserted // new, inserted elements
  //       mutation.removed // removed elements
  //   }
  // }),
  mounted: function () {
    document.onkeydown = this.keydownHandler;
  },
  data: function() {
    return {
      edit: false,
      undoItems: [],
      redoItems: [],
      object2add: {},
      object2delete: {},
      object2swap: {},
      showModal: false,
      showCreateModal: false,
      itemName: 'Big Business',
      itemURL: 'https://www.google.nl/',
      showName: false,
      showURL:  false,
      listTitle: '',
      message: '',
      categories: document.getElementsByClassName("categories"),
      links: document.getElementsByClassName("links"),
      subCategories: document.getElementsByClassName("sub-categories"),
      subLinks: document.getElementsByClassName("sub-links"),
      ListData: {}
    }
  },
  methods: {
    openLink: function (link) {
      // This function opens a link in a new tab.
      window.open(link, '_blank');
    },
    changeState: function (collapse) {
      // This function either collapses or expands all (sub-)categories depending on
      // whether the input collapse is true or false respectively.

      this.$refs.collapsible.map(c => {
        if (c.show === collapse) {
          c.toggle()
        }
      });
    },
    searchResults: function (input) {
      // This function checks if the user input compares to the name of any element and
      // takes action accordingly.
      //
      // The input is case insensitive.

      if (input.length > 0) {
        // Convert input to lower cases
        input = input.toLowerCase();

        // Check if a category needs to be hidden or not
        this.categories.forEach(category => {

          // Get corresponding links
          let links = document.getElementsByClassName(category.id + 'link');

          // Get corresponding sub categories
          let subCategories = document.getElementsByClassName(category.id + 'subCat');

          // Get corresponding sub categories
          let subLinks = document.getElementsByClassName(category.id + 'subLink');

          let hideCategory = true;

          // Check categories
          if (category.getAttribute('item').toLowerCase().includes(input)) {
            hideCategory = false;

            // Show all corresponding links
            links.forEach(link => {
              link.hidden = false;
            })

            // Show all corresponding sub categories
            subCategories.forEach(subCategory => {
              subCategory.hidden = false;
            })

            // Show all corresponding links
            subLinks.forEach(subLink => {
              subLink.hidden = false;
            })

          } else {
            // Check sub-categories
            subCategories.forEach(subCategory => {

              // Get corresponding sub-links
              let subLinks = document.getElementsByClassName(category.id + 'subLink' + ' ' + subCategory.id + 'subLink');

              let hideSubCategory = true; // Decision variable for hiding the sub-category

              // If sub-category name contains input, show all sub-links within
              if (subCategory.getAttribute('item').toLowerCase().includes(input)) {
                hideSubCategory = false;

                // Show all sub-links
                subLinks.forEach(subLink => {
                  subLink.hidden = false;
                })
              } else {
                // Check sub-links
                subLinks.forEach(subLink => {
                  // If sub-link name contains input, show sub-link
                  subLink.hidden = !subLink.getAttribute('item').toLowerCase().includes(input);

                  // If a sub-link is not hidden anymore, do not hide sub-category
                  if (!subLink.hidden) {
                    hideSubCategory = false;
                  }
                })
              }

              // Check if sub-category needs to be hidden
              subCategory.hidden = hideSubCategory;

              // If a sub-category is not hidden anymore, do not hide category
              if (!hideSubCategory) {
                hideCategory = false;
              }
            })

            // Check links
            links.forEach(link => {
              // If link name contains input, show link
              link.hidden = !link.getAttribute('item').toLowerCase().includes(input);

              // If a link is not hidden anymore, do not hide category
              if (!link.hidden) {
                hideCategory = false;
              }
            })
          }

          // Check if category needs to be hidden
          category.hidden = hideCategory;
        })
      } else {
        // Do not compare anything and show all categories/links
        this.clearSearch(false);
      }
    },
    clearSearch: function (clear) {
      // This function clears the user input field and shows all elements again, starting
      // with the deepest nested elements all the way to the categories.

      // Clear the current user input
      if (clear) {
        this.message = '';
      }

      // Show all sub-links
      this.subLinks.forEach(subLink => {
        subLink.hidden = false;
      })

      // Show all sub-categories
      this.subCategories.forEach(subCategory => {
        subCategory.hidden = false;
      })

      // Show all links
      this.links.forEach(link => {
        link.hidden = false;
      })

      // Show all categories
      this.categories.forEach(category => {
        category.hidden = false;
      })
    },
    addItem: function (type, iCat=null, iSubCat=null) {
      // This function makes the modal visible to the user and initialises the object to
      // be added

      if (type === 'link' || type === 'sub-link') {
        this.showName = true;
        this.showURL = true;
      } else if (type === 'category' || type === 'sub-category') {
        this.showName = true;
      } else {
        console.log('Type to add not recognized')
        return;
      }

      // Display the modal for user input
      this.showModal = true;

      // Create an object which contains information for the item to be added
      let object = this.getEmptyObject();

      object.type = type;
      object.action = 'add';
      object.iCat = iCat;
      object.iLink = null;
      object.iSubCat = iSubCat;
      object.iSubLink = null;

      this.object2add = object

      // When the user clicks anywhere outside of the modal, close it
      // window.onclick = function(event) {
      //   if (event.target === this.modal) {
      //     this.modal.style.display = "none";
      //   }
      // }
    },
    deleteItem: function (event, type, iCat=null, iLink=null, iSubCat=null, iSubLink=null) {
      // This function initialises the object to be deleted and calls the delete function

      // Stop the event from hitting child block function (such as collapse)
      event.stopPropagation();

      // Create an object which contains information for the item to be deleted
      let object = this.getEmptyObject();

      object.type = type;
      object.action = 'delete';
      object.iCat = iCat;
      object.iLink = iLink;
      object.iSubCat = iSubCat;
      object.iSubLink = iSubLink;

      this.object2delete = object;

      this.setItemDelete(); // The delete function
    },
    getEmptyObject: function () {
      // This function create a standard add/delete object

      return {
        'action': '',
        'type': '',
        'iCat': null,
        'iLink': null,
        'iSubCat': null,
        'iSubLink': null,
        'iCatOrigin': null,
        'iLinkOrigin': null,
        'iSubCatOrigin': null,
        'iSubLinkOrigin': null,
        'item': {}
      }
    },
    setItemAdd: function (undo=null) {

      // Get the object to be added
      let object = this.object2add;

      let newItem = Object.keys(object.item).length === 0

      if (object.type === 'category') {

        if (newItem) {
          object.item = {
            'name': this.itemName,
            'id': this.ListData.counter + 1,
            'subCategories': [],
            'links': []
          };

          object.iCat = this.ListData.categories.length;
        }

        this.ListData.categories.splice(object.iCat, 0, object.item);

      } else if (object.type === 'link') {

        if (newItem) {
          object.item = {
            'name': this.itemName,
            'id': this.ListData.counter + 1,
            'url': this.itemURL
          };

          object.iLink = this.ListData.categories[object.iCat].links.length;
        }

        this.ListData.categories[object.iCat].links.splice(object.iLink, 0, object.item);

      } else if (object.type === 'sub-category') {

        if (newItem) {
          object.item = {
            'name': this.itemName,
            'id': this.ListData.counter + 1,
            'links': [],
          };

          object.iSubCat = this.ListData.categories[object.iCat].subCategories.length;
        }

        this.ListData.categories[object.iCat].subCategories.splice(object.iSubCat, 0, object.item);

      } else if (object.type === 'sub-link') {

        if (newItem) {
          object.item = {
            'name': this.itemName,
            'id': this.ListData.counter + 1,
            'url': this.itemURL
          };

          object.iSubLink = this.ListData.categories[object.iCat].subCategories[object.iSubCat].links.length;
        }

        this.ListData.categories[object.iCat].subCategories[object.iSubCat].links.splice(object.iSubLink, 0, object.item);

      } else {
        console.log('Nothing was added')
      }

      if (undo === null) {
        this.undoItems.push(object);
        this.redoItems = [];
        this.ListData.counter++
      } else if (undo) {
        this.redoItems.push(object);
      } else if (!undo) {
        this.undoItems.push(object);
      } else {
        console.log('Unknown \'redo\' status...')
      }

      this.closeModal();
    },
    setItemDelete: function (undo) {

      let object = this.object2delete;

      if (object.type === 'category') {

        object.item = this.ListData.categories.splice(object.iCat, 1)[0];

      } else if (object.type === 'link') {

        object.item = this.ListData.categories[object.iCat].links.splice(object.iLink, 1)[0];

      } else if (object.type === 'sub-category') {

        object.item = this.ListData.categories[object.iCat].subCategories.splice(object.iSubCat, 1)[0];

      } else if (object.type === 'sub-link') {

        object.item = this.ListData.categories[object.iCat].subCategories[object.iSubCat].links.splice(object.iSubLink, 1)[0];

      } else {
        // Do nothing
        console.log('Nothing was deleted')
        return;
      }

      if (undo === null) {
        this.undoItems.push(object);
        this.redoItems = [];
      } else if (undo) {
        this.redoItems.push(object);
      } else if (!undo) {
        this.undoItems.push(object);
      } else {
        console.log('Unknown \'redo\' status...')
      }
    },
    undoItem: function () {
      if (this.undoItems.length !== 0) {
        let undo = this.undoItems.pop();

        if (undo.action === 'add') {
          this.object2delete = undo
          this.setItemDelete(true)
        } else if (undo.action === 'delete') {
          this.object2add = undo
          this.setItemAdd(true)
        } else if (undo.action === 'swap') {
          this.dataTransfer = undo.item
          this.swapItems(true)
        } else {
          console.log('Unknown undo type')
        }

      } else {
        console.log('Nothing to undo')
      }
    },
    redoItem: function () {
      if (this.redoItems.length !== 0) {
        let redo = this.redoItems.pop();

        if (redo.action === 'add') {
          this.object2add = redo
          this.setItemAdd(false)
        } else if (redo.action === 'delete') {
          this.object2delete = redo
          this.setItemDelete(false)
        } else if (redo.action === 'swap') {
          this.dataTransfer = redo.item
          this.swapItems(false)
        } else {
          console.log('Unknown undo type')
        }

      } else {
        console.log('Nothing to redo')
      }
    },
    keydownHandler: function (e) {
      // If not in editing mode, return immediately (default behavior)
      if (!this.edit) {
        return;
      }

      // If the focus is not on the input field
      if (e.target.id !== 'input-search') {

        // Detect CTRL + Z && V
        if (e.keyCode === 90 && e.ctrlKey) {
          this.undoItem();
        } else if (e.keyCode === 89 && e.ctrlKey) {
          this.redoItem();
        } else {
          console.log('Combination of keys not supported') // Kinda spammy
          return;
        }

        // Prevent other things from happening
        e.preventDefault();
      }
    },
    closeModal: function () {
      this.showModal = false;
      this.showCreateModal = false;

      this.showName = false;
      this.showURL = false;

      // When the user clicks anywhere outside of the modal, close it
      // window.onclick = function(event) {
      //   if (event.target === this.modal) {
      //     this.modal.style.display = "none";
      //   }
      // }
    },
    startDrag: function (evt, type, iCat=null, iLink=null, iSubCat=null, iSubLink=null) {
      evt.stopPropagation();

      this.dataTransfer = {
        'typeOrigin': type,
        'iCatOrigin': iCat,
        'iCatTarget': null,
        'iLinkOrigin': iLink,
        'iLinkTarget': null,
        'iSubCatOrigin': iSubCat,
        'iSubCatTarget': null,
        'iSubLinkOrigin': iSubLink,
        'iSubLinkTarget': null,
      }
    },
    onDrop: function (evt, type, iCat=null, iLink=null, iSubCat=null, iSubLink=null) {
      evt.stopPropagation();

      this.dataTransfer.typeTarget = type
      this.dataTransfer.iCatTarget = iCat
      this.dataTransfer.iLinkTarget = iLink
      this.dataTransfer.iSubCatTarget = iSubCat
      this.dataTransfer.iSubLinkTarget = iSubLink

      this.swapItems();
    },
    swapItems: function (undo=false) {
      let type = this.dataTransfer.typeTarget
      let iCat = this.dataTransfer.iCatTarget
      let iLink= this.dataTransfer.iLinkTarget
      let iSubCat = this.dataTransfer.iSubCatTarget
      let iSubLink = this.dataTransfer.iSubLinkTarget

      let typeOrigin = this.dataTransfer.typeOrigin
      let iCatOrigin = this.dataTransfer.iCatOrigin
      let iLinkOrigin = this.dataTransfer.iLinkOrigin
      let iSubCatOrigin = this.dataTransfer.iSubCatOrigin
      let iSubLinkOrigin = this.dataTransfer.iSubLinkOrigin

      if (undo) {
        // [type, typeOrigin] = [typeOrigin, type];
        [iCat, iCatOrigin] = [iCatOrigin, iCat];
        [iLink, iLinkOrigin] = [iLinkOrigin, iLink];
        [iSubCat, iSubCatOrigin] = [iSubCatOrigin, iSubCat];
        [iSubLink, iSubLinkOrigin] = [iSubLinkOrigin, iSubLink];
      }

      if (type === 'category' && typeOrigin === 'category') {

        let sorted = this.sortSwap([iCat, iCatOrigin]);

        [this.ListData.categories[sorted[0]], this.ListData.categories[sorted[1]]] = [this.ListData.categories[sorted[1]], this.ListData.categories[sorted[0]]];
        [this.ListData.categories[sorted[0]].id, this.ListData.categories[sorted[1]].id] = [this.ListData.categories[sorted[1]].id, this.ListData.categories[sorted[0]].id];

      } else if ((type === 'category' && typeOrigin === 'link') || (type === 'link' && typeOrigin === 'category' && undo)) {

        if (!undo) {
          this.ListData.categories[iCat].links.push(this.ListData.categories[iCatOrigin].links.splice(iLinkOrigin, 1)[0])
        } else {
          this.ListData.categories[iCat].links.splice(iLink, 0, this.ListData.categories[iCatOrigin].links.pop())
        }

      } else if (type === 'category' && typeOrigin === 'sub-category') {

        if (!undo) {
          this.ListData.categories[iCat].subCategories.push(this.ListData.categories[iCatOrigin].subCategories.splice(iSubCatOrigin, 1)[0])
        } else {
          this.ListData.categories[iCat].subCategories.splice(iSubCat, 0, this.ListData.categories[iCatOrigin].subCategories.pop())
        }

      } else if (type === 'category' && typeOrigin === 'sub-link') {

        if (!undo) {
          this.ListData.categories[iCat].links.push(this.ListData.categories[iCatOrigin].subCategories[iSubCatOrigin].links.splice(iSubLinkOrigin, 1)[0])
        } else {
          this.ListData.categories[iCat].subCategories[iSubCat].links.splice(iSubLink, 0, this.ListData.categories[iCatOrigin].links.pop())
        }

      } else if (type === 'link' && typeOrigin === 'link') {

        let sorted = this.sortSwap([iLink, iLinkOrigin]);

        [this.ListData.categories[iCat].links[sorted[0]], this.ListData.categories[iCat].links[sorted[1]]] = [this.ListData.categories[iCat].links[sorted[1]], this.ListData.categories[iCat].links[sorted[0]]];
        [this.ListData.categories[iCat].links[sorted[0]].id, this.ListData.categories[iCat].links[sorted[1]].id] = [this.ListData.categories[iCat].links[sorted[1]].id, this.ListData.categories[iCat].links[sorted[0]].id];

      } else if (type === 'sub-category' && typeOrigin === 'link') {

        if (!undo) {
          this.ListData.categories[iCat].subCategories[iSubCat].links.push(this.ListData.categories[iCatOrigin].links.splice(iLinkOrigin, 1)[0])
        } else {
          this.ListData.categories[iCat].links.splice(iLink, 0, this.ListData.categories[iCatOrigin].subCategories[iSubCatOrigin].links.pop())
        }

      } else if (type === 'sub-category' && typeOrigin === 'sub-category') {

        let sorted = this.sortSwap([iSubCat, iSubCatOrigin]);

        [this.ListData.categories[iCat].subCategories[sorted[0]], this.ListData.categories[iCat].subCategories[sorted[1]]] = [this.ListData.categories[iCat].subCategories[sorted[1]], this.ListData.categories[iCat].subCategories[sorted[0]]];
        [this.ListData.categories[iCat].subCategories[sorted[0]].id, this.ListData.categories[iCat].subCategories[sorted[1]].id] = [this.ListData.categories[iCat].subCategories[sorted[1]].id, this.ListData.categories[iCat].subCategories[sorted[0]].id];

      } else if (type === 'sub-category' && typeOrigin === 'sub-link') {

        if (!undo) {
          this.ListData.categories[iCat].subCategories[iSubCat].links.push(this.ListData.categories[iCatOrigin].subCategories[iSubCatOrigin].links.splice(iSubLinkOrigin, 1)[0])
        } else {
          this.ListData.categories[iCat].subCategories[iSubCat].links.splice(iSubLink, 0, this.ListData.categories[iCatOrigin].subCategories[iSubCatOrigin].links.pop())
        }

      } else if (type === 'sub-link' && typeOrigin === 'sub-link') {

        let sorted = this.sortSwap([iSubLink, iSubLinkOrigin]);

        [this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[0]], this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[1]]] = [this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[1]], this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[0]]];
        [this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[0]].id, this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[1]].id] = [this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[1]].id, this.ListData.categories[iCat].subCategories[iSubCat].links[sorted[0]].id];

      } else {
        console.log('Drop not allowed, undefined type pair', type, typeOrigin)
        return;
      }

      let swapObject = this.getEmptyObject();

      swapObject.action = 'swap';
      swapObject.item = this.dataTransfer;

      if (undo) {
        this.redoItems.push(swapObject);
      } else if (!undo) {
        this.undoItems.push(swapObject);
      } else {
        console.log('IDk')
      }
    },
    sortSwap: function (sorted) {
      sorted.sort(function (a, b) {
        return b - a;
      });

      return sorted
    },
    async getList () {
      let server_data = {'title': this.listTitle}

      let data = await this.request('get', server_data)

      if (data !== null) {
        this.ListData = await data.list;
      }
    },
    createList: async function () {
      this.showCreateModal = false;

      let server_data = {'title': this.listTitle}

      let data = await this.request('create', server_data)

      if (data !== null) {
        this.ListData = data.list;
      }
    },
    saveItem: async function () {
      let server_data = {'list': this.ListData}

      await this.request('save', server_data)
    },
    async request(type, server_data) {
      return await fetch(`${origin}/api/${type}`, {
        method: "POST",
        body: JSON.stringify(server_data),
        // credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
      }) // after receiving the response do:
      .then(response => {
        // if something went wrong, print error
        if (response.status !== 200) {
          console.log(`Response status was not 200: ${response.status}`);
          return;
        }

        return response.json().then(data => {
          if (data.error) {
            console.log(data.error_message)
            return null;
          } else {
            return data;
          }
        })

      })
      .catch((error) => {
        console.log(error);
        return null;
      });
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
  width: 500px;
}

#input-search {
  display: block;
  width: 200px;
  text-align: center;
  margin: 0 auto;
}

#search-list {
  display: block;
  width: 200px;
  text-align: center;
  margin: 0 auto;
}

.close {
  position: absolute;
  top: 0;
  right: 5px;
  cursor: pointer;
}

.card-list {
  display: block;
  width: 400px;
  margin: 10px auto;
}

.categories, .categories-edit{
  cursor: pointer;
  margin: 10px;
}

.edit-buttons {
  position: absolute;
  right: 10px;
  top: 10px;
}

/* The Modal (background) */
.modal {
  display: block; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 200px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
}

/*!* The Close Button *!*/
/*.delete {*/
/*  position: absolute;*/
/*  top: 10px;*/
/*  right: 10px;*/
/*  color: #aaaaaa;*/
/*  float: right;*/
/*  font-size: 28px;*/
/*  font-weight: bold;*/
/*}*/

/*.delete:hover,*/
/*.delete:focus {*/
/*  color: #ffffff;*/
/*  text-decoration: none;*/
/*  cursor: pointer;*/
/*}*/

/*!* The Right button container *!*/
/*.icon-right {*/
/*  position: absolute;*/
/*  top: 0;*/
/*  right: 5px;*/
/*  width: 40px;*/
/*  height: 40px;*/
/*  float: right;*/
/*}*/

/*.icon-right:hover,*/
/*.icon-right:focus {*/
/*  color: #ffffff;*/
/*  text-decoration: none;*/
/*  cursor: pointer;*/
/*}*/

/*.chevron-down {*/
/*  content: '';*/
/*  position: absolute;*/
/*  top: 25%;*/
/*  right: 25%;*/
/*  height: 30%;*/
/*  width: 30%;*/
/*  border-top: 3px solid;*/
/*  border-right: 3px solid;*/
/*  transform: rotate(135deg);*/
/*  color: darkgrey;*/
/*}*/

/*.chevron-right {*/
/*  content: '';*/
/*  position: absolute;*/
/*  top: 25%;*/
/*  right: 25%;*/
/*  height: 30%;*/
/*  width: 30%;*/
/*  border-top: 3px solid;*/
/*  border-right: 3px solid;*/
/*  transform: rotate(45deg);*/
/*  color: dimgrey;*/
/*}*/

/*.category-header:hover .icon-right{*/
/*  color: #fff;*/
/*}*/

/*@keyframes rotate180 {*/
/*  to {  }*/
/*}*/

/*.categories:active .icon-right{*/
/*  transform-origin: 80% 20%;*/
/*  animation-fill-mode: forwards;*/
/*  transform: rotate(180deg);*/
/*  transition: transform 0.4s ease;*/
/*}*/

</style>



<!--{-->
<!--  "title":"Runescape",-->
<!--  "id": 0,-->
<!--  "counter": 47,-->
<!--  "categories":[-->
<!--    {-->
<!--      "name":"Runescape Official links",-->
<!--      "id": 0,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"RS3 Homepage",-->
<!--          "id": 1,-->
<!--          "url":"https://www.runescape.com/community"-->
<!--        },-->
<!--        {-->
<!--          "name":"Twitter",-->
<!--          "id": 2,-->
<!--          "url":"https://twitter.com/runescape"-->
<!--        },-->
<!--        {-->
<!--          "name":"Youtube",-->
<!--          "id": 3,-->
<!--          "url":"https://www.youtube.com/user/runescape"-->
<!--        },-->
<!--        {-->
<!--          "name":"Instagram",-->
<!--          "id": 4,-->
<!--          "url":"https://www.instagram.com/runescape/"-->
<!--        },-->
<!--        {-->
<!--          "name":"Twitch",-->
<!--          "id": 5,-->
<!--          "url":"https://www.twitch.tv/directory/game/RuneScape"-->
<!--        },-->
<!--        {-->
<!--          "name":"Jagex Support on Twitter",-->
<!--          "id": 6,-->
<!--          "url":"https://twitter.com/JagexSupport"-->
<!--        },-->
<!--        {-->
<!--          "name":"Jagex",-->
<!--          "id": 7,-->
<!--          "url":"https://www.jagex.com/en-GB/"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Youtube content creators",-->
<!--      "id": 8,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Protoxx",-->
<!--          "id": 9,-->
<!--          "url":"https://www.youtube.com/c/ProtoxxGaming"-->
<!--        },-->
<!--        {-->
<!--          "name":"The RS Guy",-->
<!--          "id": 10,-->
<!--          "url":"https://www.youtube.com/c/TheRSGuyRunescapeContent"-->
<!--        },-->
<!--        {-->
<!--          "name":"Silenced",-->
<!--          "id": 11,-->
<!--          "url":"https://www.youtube.com/c/SilencedRS"-->
<!--        },-->
<!--        {-->
<!--          "name":"Maikeru RS",-->
<!--          "id": 12,-->
<!--          "url":"https://www.youtube.com/c/maikerurs"-->
<!--        },-->
<!--        {-->
<!--          "name":"Large Gats",-->
<!--          "id": 13,-->
<!--          "url":"https://www.youtube.com/c/LargeGats"-->
<!--        },-->
<!--        {-->
<!--          "name":"Grimm dutch",-->
<!--          "id": 14,-->
<!--          "url":"https://www.youtube.com/c/Grimmdutch"-->
<!--        },-->
<!--        {-->
<!--          "name":"Evil Lucario",-->
<!--          "id": 15,-->
<!--          "url":"https://www.youtube.com/c/EvilLucario"-->
<!--        },-->
<!--        {-->
<!--          "name":"rswillmissit",-->
<!--          "id": 16,-->
<!--          "url":"https://www.youtube.com/user/rswillmissit"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Twitch streamers",-->
<!--      "id": 17,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Luna",-->
<!--          "id": 18,-->
<!--          "url":"https://nu.nl"-->
<!--        },-->
<!--        {-->
<!--          "name":"Nick",-->
<!--          "id": 19,-->
<!--          "url":"https://nu.nl"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Jagex moderators",-->
<!--      "id": 20,-->
<!--      "subCategories":[-->
<!--        {-->
<!--          "name":"Reddit",-->
<!--          "id": 21,-->
<!--          "links":[-->
<!--            {-->
<!--              "name":"Osborne",-->
<!--              "id": 22,-->
<!--              "url":"https://www.reddit.com/user/JagexOsborne"-->
<!--            },-->
<!--            {-->
<!--              "name":"Hooli",-->
<!--              "id": 23,-->
<!--              "url":"https://www.reddit.com/user/JagexHooli"-->
<!--            },-->
<!--            {-->
<!--              "name":"Luma",-->
<!--              "id": 24,-->
<!--              "url":"https://www.reddit.com/user/JagexLuma"-->
<!--            }-->
<!--          ]-->
<!--        },-->
<!--        {-->
<!--          "name":"Twitter",-->
<!--          "id": 25,-->
<!--          "links":[-->
<!--            {-->
<!--              "name":"Pi",-->
<!--              "id": 26,-->
<!--              "url":"https://mobile.twitter.com/JagexPi"-->
<!--            },-->
<!--            {-->
<!--              "name":"Sponge",-->
<!--              "id": 27,-->
<!--              "url":"https://mobile.twitter.com/JagexSponge"-->
<!--            },-->
<!--            {-->
<!--              "name":"Luma",-->
<!--              "id": 28,-->
<!--              "url":"https://mobile.twitter.com/JagexLuma"-->
<!--            }-->
<!--          ]-->
<!--        }-->
<!--      ],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Luna",-->
<!--          "id": 29,-->
<!--          "url":"https://runescape.com"-->
<!--        },-->
<!--        {-->
<!--          "name":"Nick",-->
<!--          "id": 30,-->
<!--          "url":"https://runescape.com"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Discord servers",-->
<!--      "id": 31,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Luna",-->
<!--          "id": 32,-->
<!--          "url":"https://runescape.com"-->
<!--        },-->
<!--        {-->
<!--          "name":"Nick",-->
<!--          "id": 33,-->
<!--          "url":"https://runescape.com"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Spreadsheets",-->
<!--      "id": 34,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Max Efficiency Guide",-->
<!--          "id": 35,-->
<!--          "url":"https://docs.google.com/spreadsheets/d/17fUsCqH_8sMGHs3lKFBY6t0lsFgfCIeox6nCdBFl5QQ/edit#gid=0"-->
<!--        },-->
<!--        {-->
<!--          "name":"Nick",-->
<!--          "id": 36,-->
<!--          "url":"https://runescape.com"-->
<!--        },-->
<!--        {-->
<!--          "name":"Jack",-->
<!--          "id": 37,-->
<!--          "url":"https://runescape.com"-->
<!--        },-->
<!--        {-->
<!--          "name":"Rick",-->
<!--          "id": 38,-->
<!--          "url":"https://runescape.com"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Utilities",-->
<!--      "id": 39,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Runescape Wiki",-->
<!--          "id": 40,-->
<!--          "url":"https://runescape.wiki/"-->
<!--        },-->
<!--        {-->
<!--          "name":"Alt1 Toolkit",-->
<!--          "id": 41,-->
<!--          "url":"https://runeapps.org/alt1"-->
<!--        },-->
<!--        {-->
<!--          "name":"RuneClan",-->
<!--          "id": 42,-->
<!--          "url":"https://www.runeclan.com/"-->
<!--        },-->
<!--        {-->
<!--          "name":"Price check & trade",-->
<!--          "id": 43,-->
<!--          "url":"https://pct.wtf/"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"D&Ds",-->
<!--      "id": 44,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Penguin Hide and Seek",-->
<!--          "id": 45,-->
<!--          "url":"http://jq.world60pengs.com/"-->
<!--        }-->
<!--      ]-->
<!--    },-->
<!--    {-->
<!--      "name":"Minigames",-->
<!--      "id": 46,-->
<!--      "subCategories":[],-->
<!--      "links":[-->
<!--        {-->
<!--          "name":"Kags' POP Encyclopedia",-->
<!--          "id": 47,-->
<!--          "url":"https://secure.runescape.com/m=forum/sl=0/forums?75,76,639,66118461"-->
<!--        }-->
<!--      ]-->
<!--    }-->
<!--  ]-->
<!--}-->