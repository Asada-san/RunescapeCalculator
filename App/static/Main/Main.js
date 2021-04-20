//var searchButton = document.getElementById('ddgSearchButton');
//var searchInput = document.getElementById('ddgSearchInput');
//var searchEngineString;

// call duckduckgo whenever the user presses enter in the input field
//document.getElementById('ddgSearchInput').onkeypress = function(ev){
//    if (!ev) ev = window.event;
//    var keyCode = ev.keyCode || ev.which;
//    if (keyCode == '13'){
//        ddgSearch();
//    }
//}

// Call ddgSearch whenever the search button is pressed
//searchButton.addEventListener('click', ddgSearch);

// Function that open duckduckgo in a new tab searching for whatever the user put in
//function ddgSearch() {
//    searchEngineString = '';
//    searchEngineString += 'https://duckduckgo.com/?q=' + searchInput.value.replace(/ /g, '+')
//
//    window.open(searchEngineString, "_blank");
//}

var sidenavStatus = false;

document.getElementById("mySidenav").style.width = "0";
document.getElementById("main").style.marginLeft= "0";

//if (typeof(Storage) !== "undefined") {
//    // If we need to open the bar
//
//    if(localStorage.getItem("sidebar") == 'true'){
//        // Open the bar
//        document.getElementById("mySidenav").style.transition = "0s"
//        document.getElementById("mySidenav").style.width = "250px";
//        document.getElementById("main").style.transition = "0s"
//        document.getElementById("main").style.marginLeft = "250px";
//
//        sidenavStatus = true;
//    }
//}
//
//function sideNav() {
//    document.getElementById("mySidenav").style.transition = ".5s"
//    document.getElementById("main").style.transition = ".5s"
//
//    if (sidenavStatus == false) {
//        document.getElementById("mySidenav").style.width = "250px";
//        document.getElementById("main").style.marginLeft = "250px";
//
//        sidenavStatus = true;
//    } else if (sidenavStatus == true) {
//        document.getElementById("mySidenav").style.width = "0";
//        document.getElementById("main").style.marginLeft= "0";
//
//        sidenavStatus = false;
//    }
//
//    if (typeof(Storage) !== "undefined") {
//        // Save the state of the sidebar as "true" (becomes a string)
//        localStorage.setItem("sidebar", sidenavStatus);
//    }
//}

