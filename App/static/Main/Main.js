var searchButton = document.getElementById('ddgSearchButton');
var searchInput = document.getElementById('ddgSearchInput');
var searchEngineString;

// call duckduckgo whenever the user presses enter in the input field
document.getElementById('ddgSearchInput').onkeypress = function(ev){
    if (!ev) ev = window.event;
    var keyCode = ev.keyCode || ev.which;
    if (keyCode == '13'){
        ddgSearch();
    }
}

// Call ddgSearch whenever the search button is pressed
searchButton.addEventListener('click', ddgSearch);

// Function that open duckduckgo in a new tab searching for whatever the user put in
function ddgSearch() {
    searchEngineString = '';
    searchEngineString += 'https://duckduckgo.com/?q=' + searchInput.value.replace(/ /g, '+')

    window.open(searchEngineString, "_blank");
}

