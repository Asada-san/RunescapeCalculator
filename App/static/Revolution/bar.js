// Variables which are used in multiple functions
var outputNote = document.getElementById("DPTbox")
var DPTNote = document.getElementById("VerifyBox")

var AlreadyRan = false; // boolean used to roll-out/in outputNote properly

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// ABILITY/OPTION BLOCK CONTENT SHOWING DEPENDING ON WHAT BUTTON IS BEING CLICKED ON
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// Get all collapsible buttons in an array
var coll = document.getElementsByClassName("collapsible");

// Get all the content corresponding to the collapsible buttons in an array
var cbContent = [
    attContent = document.getElementById("attAbils"),
    strContent = document.getElementById("strAbils"),
    magContent = document.getElementById("magAbils"),
    ranContent = document.getElementById("ranAbils"),
    conContent = document.getElementById("conAbils"),
    defContent = document.getElementById("defAbils"),
    optContent = document.getElementById("optBlock")
];

var LastIdx = null; // The previous button the user clicked on

for (var i = 0; i < coll.length; i++) { // for every collapsible button
    // If the button is clicked on
    coll[i].addEventListener("click", function(ev) {
//        this.classList.toggle("active"); // toggle this class active
        // get button element which has been clicked on
        var srcId = document.getElementById(ev.srcElement.id)

        // depending on which button has been clicked on set index
        if (srcId.id == "AttBtn") {
            var ScrollIdx = 0;
        } else if (srcId.id == "StrBtn") {
            var ScrollIdx = 1;
        } else if (srcId.id == "MagBtn") {
            var ScrollIdx = 2;
        } else if (srcId.id == "RanBtn") {
            var ScrollIdx = 3;
        } else if (srcId.id == "ConBtn") {
            var ScrollIdx = 4;
        } else if (srcId.id == "DefBtn") {
            var ScrollIdx = 5;
        } else if (srcId.id == "OptBtn") {
            var ScrollIdx = 6;
        }

        // if the content is already showing
        if (cbContent[ScrollIdx].style.maxHeight){
            cbContent[ScrollIdx].style.maxHeight = null;
            ScrollOut = false;
        } else { // else ScrollOut the content
            cbContent[ScrollIdx].style.maxHeight = cbContent[ScrollIdx].scrollHeight + "px";
            ScrollOut = true;
        }

        // depending on the action in the previous if-else statement:
        // if this is not the first button being clicked on and its not the same
        // button as last time
        if (LastIdx !== null && LastIdx !== ScrollIdx) {
            // basically do the opposite for the previous content compared to the new content
            if (ScrollOut) {
                cbContent[LastIdx].style.maxHeight = null;
            } else {
                cbContent[LastIdx].style.maxHeight = cbContent[LastIdx].scrollHeight + "px";
            }
        }

        // update the button which has previously been clicked on
        LastIdx = ScrollIdx;
    });
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// OPTIONS CONTENT ROLL OUT/IN /////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

//// Get all collapsible buttons in an array
//var optBtns = document.getElementsByClassName("Options");
//
//// Get all the content corresponding to the collapsible buttons in an array
//var optContent = [
//    Options = document.getElementById("optBlock"),
//    OptionsInfo = document.getElementById("optInfoBlock")
//];
//
//var LastBtnIdx = null; // The previous button the user clicked on
//
//for (var i = 0; i < optBtns.length; i++) { // for every collapsible button
//    // If the button is clicked on
//    optBtns[i].addEventListener("click", function(ev) {
////        this.classList.toggle("active"); // toggle this class active
//        // get button element which has been clicked on
//        var srcId = document.getElementById(ev.srcElement.id)
//
//        // depending on which button has been clicked on set index
//        if (srcId.id == "OptBtn") {
//            var ScrollBtnIdx = 0;
//        } else if (srcId.id == "OptInfoBtn") {
//            var ScrollBtnIdx = 1;
//        }
//
//        // if the content is already showing
//        if (optContent[ScrollBtnIdx].style.maxHeight){
//            optContent[ScrollBtnIdx].style.maxHeight = null;
//            ScrollOut = false;
//        } else { // else ScrollOut the content
//            optContent[ScrollBtnIdx].style.maxHeight = optContent[ScrollBtnIdx].scrollHeight + "px";
//            ScrollOut = true;
//        }
//
//        // depending on the action in the previous if-else statement:
//        // if this is not the first button being clicked on and its not the same
//        // button as last time
//        if (LastBtnIdx !== null && LastBtnIdx !== ScrollBtnIdx) {
//            // basically do the opposite for the previous content compared to the new content
//            if (ScrollOut) {
//                optContent[LastBtnIdx].style.maxHeight = null;
//            } else {
//                optContent[LastBtnIdx].style.maxHeight = optContent[LastBtnIdx].scrollHeight + "px";
//            }
//        }
//
//        // update the button which has previously been clicked on
//        LastBtnIdx = ScrollBtnIdx;
//    });
//}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// REVOLUTION BAR DRAGGING AND DROPPING ABILITIES //////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// Prevent from weird shenanigans happening when dropping the element
function allowDrop(ev) {
    ev.preventDefault();
}

// Prevent from weird shenanigans happening when dragging the element
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

var BarAbilities = []; // array containing abilities which are on the bar
// Function for dropping abilities into the rev bar slot
function drop(ev) {
    // Prevent default action from happening
    ev.preventDefault();

    // Id of ability which is about to be dropped (which is its name)
    var srcId = ev.dataTransfer.getData("text");
    // Ability (element) which is about to be dropped
    var srcAbil = document.getElementById(srcId);

    // If the user put anything else onto the bar besides an ability, return
    if (srcAbil == null || !srcAbil.classList.contains('Ability'))  {
     return;
    }

    // Revo bar spot where the ability came from
    var srcRevo = srcAbil.parentNode;
    // Ability which is in the target spot
    var tgtAbil = ev.currentTarget.firstElementChild;
    // Revo bar spot which is the target spot
    var tgtRevo = ev.currentTarget;

    // If the ability has a field name, meaning its already on the bar
    if (srcAbil.hasAttribute('name')) {

        // If there is already an ability in the new spot
        if (tgtAbil !== null && tgtAbil !== srcAbil) {
            // Assign a new id to the elements to be swapped
            srcAbil.id = tgtRevo.id + "_" + srcAbil.name;
            tgtAbil.id = srcRevo.id + "_" + tgtAbil.name;

            // Replace the old ability with the new ability
            ev.currentTarget.replaceChild(srcAbil, tgtAbil);
            // Put the old ability on the old spot
            srcRevo.appendChild(tgtAbil);

        } else { // If there is no ability in the new spot
            // Assign a new id to the elements to be swapped
            srcAbil.id = ev.target.id + "_" + srcAbil.name;
            // Place the ability on the bar
            ev.currentTarget.appendChild(srcAbil);
        }

    } else { // Else its a new input ability, check if its already on the bar

        // If the revolution bar already includes the ability do nothing
        if (BarAbilities.includes(srcId)) {
            return;

        } else { // else put it on the bar
            // Copy of the ability which is about to be dropped
            var nodeCopy = document.getElementById(srcId).cloneNode(true);
            // Assign a new id to the copied ability revo(i) + _name
            nodeCopy.id = ev.target.id + "_" + srcId;
            // Assign a name to the copied ability (which is the name of the ability)
            nodeCopy.name = srcId

            // If there is already an ability in the new spot
            if (tgtAbil !== null) {
                // Delete the name from the array
                BarAbilities.splice(BarAbilities.indexOf(tgtAbil.name), 1);
                // Put the name of the new ability in the array
                BarAbilities.push(srcId);
                // Replace the old ability with the new ability
                ev.currentTarget.replaceChild(nodeCopy, tgtAbil);

            } else { // else put it on the bar
                // put the name in an array
                BarAbilities.push(srcId);
                // put the ability on the new spot
                ev.target.appendChild(nodeCopy);
            }
        }
    }
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// DELETE ABILITIES IF THEY ARE BEING CLICKED ON ///////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// array containing every element (revolution bar slot)
var RevolutionBar = document.getElementsByClassName("RevoBar")

// for every slot on the revolution bar
for (var k=0; k<RevolutionBar.length; k++) {
    // if the user clicks on a slot
    RevolutionBar[k].addEventListener("click", function(ev) {
        // get the element which has been clicked on
        var element = document.getElementById(ev.target.id);

        // if element is of type img, meaning an ability is in that slot, delete it
        if (element.nodeName == 'IMG') {
            // first delete the ability from the array
            BarAbilities.splice(BarAbilities.indexOf(element.name), 1);

            // then remove the ability from the bar
            element.remove(element);
        } else { // else do nothing
            return;
        }
    })
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// PUT ABILITY ON BAR WITH LEFT CLICK AND LINK TO RS WIKI WHEN HOLDING CTRL ////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// array containing every element (revolution bar slot)
var AbilityColl = document.getElementsByClassName("Ability")

// for every slot on the revolution bar
for (var k=0; k<AbilityColl.length; k++) {
    // if the user clicks on a slot
    AbilityColl[k].addEventListener("click", function(ev) {
        // get the element which has been clicked on
        var element = document.getElementById(ev.target.id);

        if (window.event.ctrlKey && element.nodeName == 'IMG' && element.parentNode.classList.value !== 'RevoBar') {
            url = "http://runescape.wiki/w/" + element.id;
            // open rs wiki page for the ability
            window.open(url, "_blank");
        } else if (element.nodeName == 'IMG' && element.parentNode.classList.value !== 'RevoBar' && !BarAbilities.includes(element.id) ) {
            // if element is of type img and its not on the RevoBar
            var currentBar = document.getElementById('RevolutionBar')

            BarAbilities.push(element.id)

            for (var l=0; l<14; l++) {
                if (currentBar.childNodes[l * 2 + 1].firstChild == null) {
                    var nodeCopy = document.getElementById(element.id).cloneNode(true);
                    // Assign a new id to the copied ability revo(i) + _name
                    nodeCopy.id = currentBar.childNodes[l * 2 + 1].id + "_" + element.id;
                    // Assign a name to the copied ability (which is the name of the ability)
                    nodeCopy.name = element.id
                    // put the ability on the new spot
                    currentBar.childNodes[l * 2 + 1].appendChild(nodeCopy);
                    break;
                }
            }
        }
    })
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// DELETE ALL ABILITIES ON THE BAR /////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// get the clear button element
var DeleteBar = document.getElementById("clearbutton");

// if the user clicked on the clear button
DeleteBar.addEventListener("click", function() {
    // for every ability bar slot
    for (var k = 0; k < RevolutionBar.length; k++) {
        // if the slot has a child element which is the ability image, delete it
        if (RevolutionBar[k].firstChild !== null) {
            RevolutionBar[k].removeChild(RevolutionBar[k].firstChild)
        }

        // delete all abilities in the array
        BarAbilities.splice(0,BarAbilities.length)
    }

    // Close result box if its open
    if (AlreadyRan == true) {
        outputNote.style.maxHeight = null;
        AlreadyRan = false;
    }

    if (DPTNote.style.maxHeight) {
        DPTNote.style.maxHeight = null;
        document.getElementById('DPTprint').innerHTML = "";
    }
});

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// CALCULATE THE DPT ///////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// get the run button element
var calcDPT = document.getElementById("calcbutton");
var LoopText;
var CycleText;
var AbilityTable;
var DPTNoteOut = false;
var PreviousBarInfo;

// check if the calc button is being clicked on
calcDPT.addEventListener("click", async function(ev) {

    // get an array with the bar abilities in correct order
    var InputAbilities = [];

    for (var k=0; k<RevolutionBar.length; k++) {
        if (RevolutionBar[k].firstChild !== null) {
            InputAbilities.push(RevolutionBar[k].firstChild.name)
        }
    }

    optionElements = document.forms["optmenu"].elements

    var barInfo = {};

    for (var l=0; l<optionElements.length; l++) {

        if (optionElements[l].type == 'checkbox') {
            var optionValue = optionElements[l].checked;
        } else {
            var optionValue = optionElements[l].value;
        }

        barInfo[optionElements[l].id] = optionValue;
    }

    // create dict with user options and the bar abilities
    barInfo['Abilities'] = InputAbilities;

    // Make sure the user put in a new rotation to prevent spam
    if (JSON.stringify(PreviousBarInfo) == JSON.stringify(barInfo)) {
        return;
    } else {
        PreviousBarInfo = barInfo;
    }

    // send bar info to the calc page where the DPT is calculated
    await fetch(`${window.origin}/calc`, {
        method: "POST",
        credentials: "include",
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

            // if an error occured during calculating the DPT, print error
            if (data['error']) {
                message = data['error_message']
                document.getElementById('DPT').innerHTML = '<span style="color: #FF3333;"> ERROR<br><br>' + message + '</span>';
                return;
            }

            // create a link using the DPT number, links to test page
            var linkStr = `<span class="DPTprintButton" onclick="DPTprint()" style="color: #4CAF50;"><strong>${data['AADPT']} (${data['AADPTPercentage']}%)</strong></span>`;

            // CREATE A MESSAGE TO SHOW THE (AA)DPT
            if (data['CycleRotation'].length !== 0) {
                var message = "The AADPT of the bar above is: " + linkStr;
            } else {
                var message = "The DPT of the bar above is: " + linkStr;
            }

            // if theres a warning, extend the message
            if (data['warning'].length !== 0) {
                message += "<br><br>" +  '<span style="color: orange;">WARNING!';

                // for every warning
                for (var i = 0; i < data['warning'].length; i++) {
                    message += "<br>" + data['warning'][i];
                }

                message += '</span>';
            }

            // print the message in the right place
            document.getElementById('DPT').innerHTML = message;

            counterMessage = `<span style="color:#4CAF50; font-size:11px"> Simulated fights: ${data['counter']}`;

            // print the message in the right place
            document.getElementById('counter').innerHTML = counterMessage;

            // CREATE STRING CONTAINING THE CYCLE ROTATION
            RotationString = '<br><br><span style="color: yellow;">START</span> --> ';

            // for every ability or stall in the rotation
            for (m = 0; m < data['CycleRotation'].length; m++) {
                RotationString += data['CycleRotation'][m] + ' --> ';

                // break a line each time 4 elements have been printed
                if (m == 2 || (m > 3 && (m + 2) % 4 == 0)) {
                    RotationString += '<br>';
                }
            }
            // at the end, print BACK TO START
            RotationString += '<span style="color: yellow;">BACK TO START</span>';

            // STRING CONTAINING ALL REDUNDANT ABILITIES ON THE BAR
            var RedundantAbilities = data['CycleRedundant'].toString();

            CycleText = ''

            // FORMAT SOME NICE OUTPUT TEXT WITH CYCLE INFORMATION
            if (data['CycleRotation'].length !== 0) {
                Type = 'Cycle';
            } else {
                Type = '';
            }
                CycleText += '<span style="color: #FF3333;">' + Type + ' Time: </span> ' + parseFloat((data['CycleTime'] * .6)).toFixed(1) + "s --> " + data['CycleTime'] + " ticks";
                CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Convergence Time: </span> ' + parseFloat((data['CycleConvergenceTime'] * .6)).toFixed(1) + "s --> " + data['CycleConvergenceTime'] + " ticks";
                CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Damage: </span> ' + data['CycleDamage'] + ' <span style="color: #707070;">Base Damage: ' + data['BaseDamage'] + '</span>';
                CycleText += '<br><br><span style="color: #FF3333;">' + Type + ' Rotation: </span> ' + RotationString + '<br><br>';

                if (data['CycleRedundant'].length > 0) {
                    CycleText += '<span style="color: #FF3333;">Redundant abilities: </span> ' + RedundantAbilities.replace(/,/g, ', ') + "<br><br>";
                }

                function tableCreate() {
                    tt = '<table style="">';
                    headText = ['Source', 'activations', 'damage', '% of total damage'];
                    for(var i = 0; i < Object.keys(data['AbilityInfo']).length + 1; i++){
                        tt += '<tr>';
                        if (i !== 0) {
                            key = Object.keys(data['AbilityInfo'])[i-1];
                        }
                        for(var j = 0; j < 4; j++){
                            if (i == 0) {
                                tt += '<th style="border: 1px solid #999999;">' + headText[j] + '</th>';
                            } else {
                                if (j == 0) {
                                    tt += '<td style="border: 1px solid #999999;">' + key + '</td>';
                                } else if (j == 1) {
                                    tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + data['AbilityInfo'][key]['activations'] + '</span>' + '</td>';
                                } else if (j == 2) {
                                    tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + parseFloat(data['AbilityInfo'][key]['damage']).toFixed(2) + '</span>' + '</td>';
                                } else if (j == 3) {
                                    tt += '<td style="border: 1px solid #999999;">' + '<span style="float: right;">' + parseFloat(data['AbilityInfo'][key]['shared%']).toFixed(2) + '</span>' + '</td>';
                                }
                            }
                        }
                        tt += '</tr>';
                    }
                    tt += '</table>';
                    return tt;
                }
                AbilityTable = tableCreate();

                CycleText += '<span style="color: #FF3333;">' + Type + ' Ability Information: </span> <br><br>';

                CycleText += AbilityTable + '<br><br>';
//            }

            CycleText += '<span style="color: #FF3333; font-size: small;">Python Script Execution Time: </span><span style="font-size:small;">' + data['ExecutionTime'] + "s</span><br>";
            CycleText += '<span style="color: #FF3333; font-size: small;">Simulation Time: </span><span style="font-size:small;">' + (parseFloat(data['SimulationTime']) * 0.6).toFixed(1) + "s --> " + data['SimulationTime'] + ' ticks</span><br>';

            // the loop text which shows what happens for each tick
            LoopText = data['LoggerText'];

            document.getElementById('DPTprint').innerHTML = CycleText + LoopText;

            if (DPTNote.style.maxHeight && DPTNoteOut == true){
                DPTNote.style.maxHeight = DPTNote.scrollHeight + "px";
            }
        })
    })

    // if its the second time the user clicked on the calc button (or more) , do nothing
    if (AlreadyRan) {
        return;
    } else { // else roll-out the results box
        outputNote.style.maxHeight = outputNote.scrollHeight + "px";
        AlreadyRan = true;
    }
});

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// ROLL-OUT/IN NOTE CONTENT ////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// buttons used within a note block
var button = document.getElementsByClassName("note-button");

// the content of all the buttons which have to be shown upon a click
var noteContent = [
    guide = document.getElementById("Bar-guide"),
    notes = document.getElementById("Bar-notes"),
    options = document.getElementById("Changelog-notes"),
];

for (var i = 0; i < button.length; i++) { // for every note button
    button[i].addEventListener("click", function(ev) {
        this.classList.toggle("active");
        // get the id of the button
        var srcId = document.getElementById(ev.srcElement.id)

        // depending on which button has been clicked on set index
        if (srcId.id == "guide-button") {
            var ScrollIdx = 0;
        } else if (srcId.id == "notes-button") {
            var ScrollIdx = 1;
        } else if (srcId.id == "changelog-button") {
            var ScrollIdx = 2;
        }

        // if the content is already showing
        if (noteContent[ScrollIdx].style.maxHeight){
            noteContent[ScrollIdx].style.maxHeight = null;
        } else { // else ScrollOut the content
            noteContent[ScrollIdx].style.maxHeight = noteContent[ScrollIdx].scrollHeight + "px";
        }
    });
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// ROLL-OUT/IN DPT INFORMATION /////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// Function for showing cycle/rotation text when clicking on the DPT
function DPTprint() {
    document.getElementById('DPTprint').innerHTML = CycleText + LoopText;

    // if the content is already showing
    if (DPTNote.style.maxHeight) {
        DPTNote.style.maxHeight = null;
        document.getElementById('DPTprint').innerHTML = null;
        DPTNoteOut = false;
    } else { // else ScrollOut the content
        DPTNote.style.maxHeight = DPTNote.scrollHeight + "px";
        DPTNoteOut = true;
    }
}





