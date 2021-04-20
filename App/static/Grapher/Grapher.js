var width = window.innerWidth;
var height = window.innerHeight;

async function processEquation() {
    var equation = document.getElementById("equation").value;

    var graphInfo = {'equation': equation,
                     'windowHeight': height,
                     'windowWidth': width};

    // send bar info to the calc page where the DPT is calculated
    await fetch(`${window.origin}/graph`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(graphInfo),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function (response) {

        // if something went wrong, print error
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return;
        }

        response.json().then(function (data) {
            console.log(data)

            var canvas = document.getElementById("canvas");
            var context = canvas.getContext('2d');

            canvas.width = width;
            canvas.height = height;
            console.log(canvas)

//            var image_obj = new Image();
//            image_obj.onload = function(){
                var newImage = context.createImageData(canvas.width, canvas.height);
                var arr = context.getImageData(0, 0, canvas.width, canvas.height);
                var pixels = arr.data;

                for(var i = 0; i < pixels.length; i+=4){
                    var r = 255 - pixels[i];
                    var g = 255 - pixels[i + 1];
                    var b = 255 - pixels[i + 2];
                    var a = pixels[i + 3];

                    newImage.data[i] = r;
                    newImage.data[i + 1] = g;
                    newImage.data[i + 2] = b;
                    newImage.data[i + 3] = a;
                }

                context.clearRect(0, 0, canvas.width, canvas.height);
                context.putImageData(newImage, 0, 0);

                console.log(context, canvas)
//            }
        })
    })
}