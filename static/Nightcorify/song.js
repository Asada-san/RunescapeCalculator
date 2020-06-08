var song;
var Loading = true;
var SelectedASong = false;

var songNameText = document.getElementById('songName');

var SongButton = document.getElementById('StartSongButton');
var StuffHider = document.getElementsByClassName('StuffHider');
var BarWaveBox = document.getElementById('BarWaveBox');

var sliderRate = document.getElementById('sliderRate');
var sliderTime = document.getElementById('sliderTime');

var UpdateSliderTime;

var sliderRateOutput = document.getElementById("sliderRateValue");
var sliderTimeOutput = document.getElementById("sliderTimeValue");

var NoteWidth = 800;
var NoteHeight = 800;

var mp3File = document.getElementById("MP3input");

var fft;
var nFrequency = 128;
var nLoop = 0;

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// P5 SETUP FUNCTION ///////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

function setup() {
    noLoop(); // Don't loop the draw function yet

    // create canvas
    var cnv = createCanvas(NoteWidth, NoteHeight);
    cnv.parent('BarWaveBox');

    // set standards
    colorMode(HSB);
    angleMode(DEGREES);

    // When the user puts in an mp3 file
    mp3File.oninput = function() {

        // display certain elements for the user to interact with
        for (var i = 0; i < StuffHider.length; i++) {
            StuffHider[i].style.display = 'none';
        }

        // If a song is playing or the user already uploaded a song before
        if (SelectedASong && song.isPlaying()) {
            song.stop();
            SongButton.innerHTML = 'Start';
        }

        noLoop(); // stop looping until song is fully loaded
        nLoop = 0; // reset nLoop

        // load in the mp3 file
        song = loadSound(URL.createObjectURL(this.files[0]), loaded);

        // show the name of the uploaded file
        songNameText.innerHTML = this.files[0]['name'];

        // the user selected a song!
        SelectedASong = true;
    };

    // set P5 FFT values (smoothing - number of frequency bands)
    fft = new p5.FFT(.6, nFrequency);

    // When the song button is pressed go to checkPlayStatus function
    SongButton.addEventListener("click", checkPlayStatus);

    // construct slider for setting the sample rate of the mp3 file
    sliderRate.min = 1;     // min value 1 <-- normal speed/pitch
    sliderRate.max = 1.5;   // max value 1.5 <-- higher speed/pitch than 1
    sliderRate.value = 1;   // start at value 1
    sliderRate.step = .01;  // increments of .01
    sliderRateOutput.innerHTML = sliderRate.value; // set initial value of the rate slider

    // update value of rate slider whenever the user changes it
    sliderRate.oninput = function() {
        sliderRateOutput.innerHTML = this.value;
    };
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// FUNCTION FOR WHENEVER AN MP3 IS LOADED IN ///////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

function loaded() {
    Loading = false; // loading has finished

    SongButton.innerHTML = 'Start'; // user can now start the song

    song.setVolume(1); // default loudness of the song

    // display certain elements for the user to interact with
    for (var i = 0; i < StuffHider.length; i++) {
        StuffHider[i].style.display = 'block';
    }

    var SongLength = song.duration();

    // construct slider for setting the timestamp of the mp3 file
    sliderTime.min = 0;             // min value 0
    sliderTime.max = SongLength;    // max value length of the song
    sliderTime.value = 0;           // start at t = 0
    sliderTime.step = .1;           // increments of .1 seconds
    sliderTimeOutput.innerHTML = sliderTime.value; // set initial value of the time slider

    // when the user is moving the slider
    sliderTime.oninput = function() {
        clearInterval(UpdateSliderTime); // stop checking the song time every 100 ms
        sliderTimeOutput.innerHTML = parseFloat(this.value).toFixed(1); // still display the current time corresponding to the knob position
    };

    // update value of rate slider whenever the user changes it (only when the user lets loose of the knob)
    sliderTime.onchange = function() {
        UpdateSliderTime = setInterval(checkSongTime, 100); // start checking the song time every 100 ms again

        // jump to the chosen time in the song
        if (song.isPlaying()) {
            song.jump(this.value);
        } else { // when the song is not playing, start it first before jumping
            checkPlayStatus();
            song.jump(this.value);
        }
    };
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// P5 DRAW FUNCTION ////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// this function runs at the fps of the user window
function draw() {
    if (!Loading) {
        background('#484848'); // set background color

        var spectrum = fft.analyze(); // get the spectrum at the current time

        translate(NoteWidth/2, NoteHeight/2);
        var Radius = 100;

        nLoop++; // increment nLoop by 1
        circleSpeed = nLoop / 5; // value determining the speed with which the visualizer circles around

        // for every frequency band calculate 4 points used for drawing a shape
        for (var i = 0; i < spectrum.length; i++) {
            var rad = (-90 + circleSpeed) % 360;

            var angle1 = map(i, 0, spectrum.length, rad, rad + 360);
            var angle2 = map(i + 1, 0, spectrum.length, rad, rad + 360);

            var amp = spectrum[i];
            var r = map(amp, 0, 255, Radius, Radius + 250);
            var x1 = Radius * cos(angle1);
            var y1 = Radius * sin(angle1);
            var x2 = Radius * cos(angle2);
            var y2 = Radius * sin(angle2);

            var x3 = r * cos(angle1);
            var y3 = r * sin(angle1);
            var x4 = r * cos(angle2);
            var y4 = r * sin(angle2);

            // stroke((255 / nFrequency) * i, 255, 255);
            fill((360 / nFrequency) * ((i + circleSpeed) % nFrequency), 255, 255);

            // draw a 'rectangle'
            beginShape();
            // arc(0, 0, 200, 200, angle1, angle2 - angle1);
            vertex(x1, y1);
            vertex(x3, y3);
            vertex(x4, y4);
            vertex(x2, y2);
            endShape(CLOSE);
        }

        // when the song is done loading, set the song sample rate depending on the rate slider value
        if (!Loading) {
            song.rate(sliderRate.value);
        }
    }
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// DO STUFF BASED ON WHETHER A SONG IS PLAYING OR NOT //////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// function for checking the current time in the song and updating the time slider accordingly
function checkSongTime() {
    sliderTime.value = song.currentTime();
    sliderTimeOutput.innerHTML = parseFloat(sliderTime.value).toFixed(1);

    // if the song has finished playing
    if (!song.isPlaying()) {
        SongButton.innerHTML = 'Start'; // change button text
        noLoop(); // stop looping the draw function
        nLoop = 0; // reset nLoop
        clearInterval(UpdateSliderTime); // stop running the checkSongTime function every 100ms
    }
}

// function for checking whether the song is paused or not and to do the opposite
function checkPlayStatus() {
    // if the song is not currently playing
    if (!song.isPlaying()) {
        loop(); // start looping the draw function again with a rate equal to the windows fps
        song.play(); // start the song

        UpdateSliderTime = setInterval(checkSongTime, 100); // start checking the song time every 100ms
        ChangePlayStatus = 'Pause'; // change button text
    } else { // else the song has been paused
        song.pause(); // pause the song
        noLoop(); // stop looping the draw function
        ChangePlayStatus = 'Resume'; // change button text
        clearInterval(UpdateSliderTime); // stop running the checkSongTime function every 100ms
    }

    // set button text depending on whether the song is playing or not
    SongButton.innerHTML = ChangePlayStatus;
}

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
// ROLL-OUT/IN NOTE CONTENT ////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

// buttons used within a note block
var button = document.getElementsByClassName("note-button");

// the content of all the buttons which have to be shown upon a click
var noteContent = [
    guide = document.getElementById("Song-guide")
];

for (var i = 0; i < button.length; i++) { // for every note button
    button[i].addEventListener("click", function(ev) {
        this.classList.toggle("active");
        // get the id of the button
        var srcId = document.getElementById(ev.srcElement.id)

        // depending on which button has been clicked on set index
        if (srcId.id == "general-button") {
            var ScrollIdx = 0;
        }

        // if the content is already showing
        if (noteContent[ScrollIdx].style.maxHeight){
            noteContent[ScrollIdx].style.maxHeight = null;
        } else { // else ScrollOut the content
            noteContent[ScrollIdx].style.maxHeight = noteContent[ScrollIdx].scrollHeight + "px";
        }
    });
}








