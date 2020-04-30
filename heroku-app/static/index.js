//https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page
// Only run what comes next *after* the page has loaded
addEventListener("DOMContentLoaded", function() {

  var buttons = document.querySelectorAll(".basic_button");
  for (var i=0, l=buttons.length; i<l; i++) {
    var button = buttons[i];
    // For each button, listen for the "click" event
    button.addEventListener("click", function(e) {
      // When a click happens, stop the button
      // from submitting our form (if we have one)
      e.preventDefault();

      var clickedButton = e.target;
      var command = clickedButton.value;

      // Now we need to send the data to our server
      // without reloading the page - this is the domain of
      // AJAX (Asynchronous JavaScript And XML)
      // We will create a new request object
      // and set up a handler for the response
      var request = new XMLHttpRequest();
      request.onload = function() {
          // We could do more interesting things with the response
          // or, we could ignore it entirely
          //alert(request.responseText);
		  console.log(request.responseText);
      };

      // We point the request at the appropriate command
      request.open("GET", "http://192.168.200.18:5000/" + command, true);
      // and then we send it off
      request.send();
    });
  }
}, true);


var slider = document.getElementById("slider");
slider.onchange = function(){
      var request = new XMLHttpRequest();
      request.onload = function() {
          // We could do more interesting things with the response
          // or, we could ignore it entirely
          //alert(request.responseText);
		  console.log(request.responseText);
      };

      // We point the request at the appropriate command
      request.open("GET", "http://192.168.200.18:5000/set_brightness/" + slider.value/100.0, true);
      // and then we send it off
      request.send();
}


const pickr = Pickr.create({
    el: '#set_color',
    theme: 'nano', // or 'monolith', or 'nano'

    swatches: [
        'rgba(244, 67, 54, 1)',
        'rgba(233, 30, 99, 0.95)',
        'rgba(156, 39, 176, 0.9)',
        'rgba(103, 58, 183, 0.85)',
        'rgba(63, 81, 181, 0.8)',
        'rgba(33, 150, 243, 0.75)',
        'rgba(3, 169, 244, 0.7)',
        'rgba(0, 188, 212, 0.7)',
        'rgba(0, 150, 136, 0.75)',
        'rgba(76, 175, 80, 0.8)',
        'rgba(139, 195, 74, 0.85)',
        'rgba(205, 220, 57, 0.9)',
        'rgba(255, 235, 59, 0.95)',
        'rgba(255, 193, 7, 1)'
    ],

    components: {

        // Main components
        preview: true,
        opacity: false,
        hue: true,
		

        // Input / output Options
        interaction: {
            hex: false,
            rgba: false,
            hsla: false,
            hsva: false,
            cmyk: false,
            input: false,
			cancel: true,
            clear: false,
            save: true 
        }
    },
	useAsButton: true,
	lockOpacity: true,
});
pickr.on('init', instance => {

    // Grab actual input-element
    const {result} = instance.getRoot().interaction;

    // Listen to any key-events
    result.addEventListener('keydown', e => {

        // Detect whever the user pressed "Enter" on their keyboard
        if (e.key === 'Enter') {
            instance.applyColor(); // Save the currenly selected color
            instance.hide(); // Hide modal
        }
    }, {capture: true});
});

pickr.on('save', (color, instance) => {
	console.log(color.toRGBA());
	new_color = color.toRGBA();

      var request = new XMLHttpRequest();
      request.onload = function() {
          // We could do more interesting things with the response
          // or, we could ignore it entirely
          //alert(request.responseText);
		  console.log(request.responseText);
      };

      // We point the request at the appropriate command
      request.open("GET", "http://192.168.200.18:5000/set_color/" + new_color[0].toFixed(0) + "." + new_color[1].toFixed(0) + "." + new_color[2].toFixed(0), true);
      // and then we send it off
      request.send();
});

let h = $(window).height()*.4;

let elem = document.getElementById('drawing');
let two = new Two({ width: $(document).width(), height: h}).appendTo(elem);
let group = two.makeGroup();

function makeHex(x, y, r){
	let hex = two.makePolygon(x, h-y, r, 6);	
	hex.fill = '#FF8000';
	hex.stroke = 'orangered';
	group.add(hex);
	return hex;
}

let path = [3, 2, 4, 2, 2, 4, 4]

let connection;


let x = 250;
let y = 250;
let r = 30;

makeHex(x, y, r);

let theta = 0;
for (let i = 0; i < path.length; i++){
	connection = path[i];
	console.log(connection);
	theta = Math.PI/180*((210-60*connection)%360);
	x = x + Math.sqrt(3)*r*Math.cos(theta);
	y = y + Math.sqrt(3)*r*Math.sin(theta);
	console.log(theta);
	console.log(x);
	console.log(y);
	console.log("___");
	makeHex(x, y, r);
}


group.center();
group.translation.set(two.width / 2, two.height / 2);
two.update();
