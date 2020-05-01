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
      let request = new XMLHttpRequest();
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
      let request = new XMLHttpRequest();
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




let h = $(window).height()*.3;

let elem = document.getElementById('drawing');
let two = new Two({ width: $(document).width(), height: h}).appendTo(elem);
let hexagons = two.makeGroup();


function updateHexDiagram(hex_ind, color){
	console.log(hex_ind);
	console.log(hexagons.children);
	hexagons.children[hex_ind].fill = "rgb(" + color[0] + "," + color[1] + "," + color[2] + ")";
	two.update();
}


function makePickr(id, endpoint){
	let orig_endpoint = endpoint;

	const pickr = Pickr.create({
		el: '#' + id,
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
		strings: {
			save: "Save",
			cancel: "Exit",
		}
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
		
		new_color.pop();
		for(let i = 0; i < 3; i++){
			new_color[i] = new_color[i].toFixed(0);
		}

		  if(orig_endpoint == "set_hex_color"){
			  console.log("jaunted");
			  updateHexDiagram(parseInt(id.substring(4)) - 2, new_color);
		  }
		  else if(endpoint == "set_color"){
			  for(let a = 0; a < hexagons.children.length; a++){
				  updateHexDiagram(a, new_color);
			  }
		  }

		  if(endpoint == "set_hex_color"){
			  endpoint = endpoint + "/" + (parseInt(id.substring(4))-2).toString();
		  }

		  let request = new XMLHttpRequest();
		  request.onload = function() {
			  // We could do more interesting things with the response
			  // or, we could ignore it entirely
			  //alert(request.responseText);
			  console.log(request.responseText);
		  };
		  
		  // We point the request at the appropriate command
		  request.open("GET", "http://192.168.200.18:5000/" + endpoint + "/" + new_color[0] + "." + new_color[1] + "." + new_color[2], true);
		  // and then we send it off
		  request.send();
		
	});
	pickr.on('cancel', () => {
		pickr.hide();
	});

}

makePickr("set_color", "set_color");


function makeHex(x, y, r){
	let hex = two.makePolygon(x, h-y, r, 6);	
	hex.fill = 'white';
	hex.stroke = 'black';
	hexagons.add(hex);
}

let path = [3, 2, 4, 2, 2, 4, 4]



function resizeStructure(){
	two.height = $(window).height()*.3;
	two.width = $(window).width();
	hexagons.translation.set(0,0);
	hexagons.scale = 1;
	hexagons.center();
	hexagons.translation.set(two.width / 2, two.height / 2);
	
	let bounds = hexagons.getBoundingClientRect();
	let bound_h = bounds['height'];
	let bound_w = bounds['width'];

	//This adjusts the hexagons to fit into the canvas no matter what
	hexagons.scale = Math.min(two.height/bound_h, two.width/bound_w);
	two.update();

}

function attachHexagonClickEvents(){
	for(let i = 0; i < hexagons.children.length; i++){

		let hex_id = hexagons.children[i].id;
		
		makePickr(hex_id, "set_hex_color");

		//which hex num it is, starting w 0
		//let hex_num = parseInt(hex_id.substring(4));
		//attaches a function to each of the hexagons
		//$('#' + hex_id).click(function (){
		//	console.log("Clicked on " + hex_id);
		//});

	}
}

function drawStructure(){
	let x = 250;
	let y = 250;
	let r = 60
	
	makeHex(x, y, r);

	let theta = 0;
	let connection;
	for (let i = 0; i < path.length; i++){
		connection = path[i];
		//console.log(connection);
		theta = Math.PI/180*((210-60*connection)%360);
		x = x + Math.sqrt(3)*r*Math.cos(theta);
		y = y + Math.sqrt(3)*r*Math.sin(theta);
		//console.log(theta);
		//console.log(x);
		//console.log(y);
		//console.log("___");
		makeHex(x, y, r);
	}
	resizeStructure();
	attachHexagonClickEvents();
    updateHexColors();


}

function updateHexColors(){

	  let request = new XMLHttpRequest();
	  request.onload = function() {
		  // We could do more interesting things with the response
		  // or, we could ignore it entirely
		  //alert(request.responseText);
		  console.log(request.responseText);
	  };
	 

      request.onreadystatechange = function() {
	      if (this.readyState == 4 && this.status == 200) {
              let parsed = JSON.parse(this.responseText)['data'];
              console.log(parsed);
              for(let i = 0; i < hexagons.children.length; i++){
                  updateHexDiagram(i, parsed[i]);
              }
	      }
	  }; 


	  // We point the request at the appropriate command
	  request.open("GET", "http://192.168.200.18:5000/get_hex_colors",  true);
	  // and then we send it off
	  request.send();
	

}


drawStructure();

window.addEventListener('resize', resizeStructure, true);

