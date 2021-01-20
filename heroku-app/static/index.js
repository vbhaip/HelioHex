//https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page
// Only run what comes next *after* the page has loaded
addEventListener("DOMContentLoaded", function() {

	let token = document.cookie.slice(document.cookie.indexOf("=") + 1)
	//cookies dont allow commas, so replace that to work normally, and remove start and end quotes
	token = token.replace(/\\054/g, ',');
	token = token.slice(1, -1)
	if(token !== 'null'){
		$.ajax({
			method: 'POST',
			async: true,
			crossDomain: true,
			url: 'http://192.168.200.28:5000/authenticate_spotify',
			data: token
		});
	}
   
    getPlugState();
    
    let buttons = document.querySelectorAll(".basic_button");
    for (let i=0, l=buttons.length; i<l; i++) {
        let button = buttons[i];
        // For each button, listen for the "click" event
        button.addEventListener("click", function(e) {
          // When a click happens, stop the button
          // from submitting our form (if we have one)
            e.preventDefault();

            let clickedButton = e.target;
            let command = clickedButton.value;

            disableInteractions();

			if(button.id === 'spotify'){
				location.href =  "https://accounts.spotify.com/authorize?client_id=f1dd20ef40d74fcaa4d9384a057c7846&response_type=code&redirect_uri=http%3A%2F%2Fheliohex.herokuapp.com%2Fcallback&scope=user-library-read%20user-modify-playback-state%20user-read-currently-playing%20user-read-playback-state%20user-modify-playback-state&state=34fFs29kd09"
			}

			else{

				$.ajax({
					async: true,
					url: "http://192.168.200.28:5000/" + command,
					cache: false,
					crossDomain: true,
					success: function(result){
						enableInteractions();
						if(button.id != "flash_around" && button.id != "set_color_palette" && button.id != "day_time"){
							clearVisualization();
						}
						if(button.id == "set_color_palette" || button.id == "day_time"){
						   getHexColors(); 
						}

						if(button.id == "toggle_power"){
							if(result['data']['is_on'] == 1){
								button.textContent = "Turn Off";
								getHexColors();
							}
							else{
								button.textContent = "Turn On";
							}
						}

					}
				});
			}
        });
    }
}, true);


function getPlugState(){
            $.ajax({
                async: true,
                url: "http://192.168.200.28:5000/plug_state",
                cache: false,
				crossDomain: true,
                success: function(result){
                    //console.log(result);
                    if(result['data']['is_on'] == 1){
						getHexColors();
                        $('#toggle_power')[0].textContent = "Turn Off"; 
                    }
                    else{
                        clearVisualization();
                        $('#toggle_power')[0].textContent = "Turn On"; 
                    }
                }
            });

}


var slider = document.getElementById("slider");
slider.onchange = function(){
    
    disableInteractions();
    $.ajax({
        async: false,
        url: "http://192.168.200.28:5000/set_brightness/" + slider.value/100.0,
		crossDomain: true,
        cache: false,
        success: function(result){
            enableInteractions();
        }
    });
}

let h = $(window).height()*.3;

let elem = document.getElementById('drawing');
let two = new Two({ width: $(document).width(), height: h}).appendTo(elem);
let hexagons = two.makeGroup();

var disabled = false;


function updateHexDiagram(hex_ind, color){
	//console.log(hex_ind);
	//console.log(hexagons.children);
	hexagons.children[hex_ind].fill = "rgb(" + color[0] + "," + color[1] + "," + color[2] + ")";
	two.update();
}

function clearVisualization(){
    for(let i = 0; i < hexagons.children.length; i++){
        updateHexDiagram(i, [255,255,255]);
    }
}


function makePickr(id, endpoint){
	let orig_endpoint = endpoint;

	const pickr = Pickr.create({
		el: '#' + id,
		theme: 'nano', // or 'monolith', or 'nano'

		swatches: [
			'rgba(244, 67, 54, 1)',
			'rgba(233, 30, 99, 1)',
			'rgba(156, 39, 176, 1)',
			'rgba(103, 58, 183, 1)',
			'rgba(63, 81, 181, 1)',
			'rgba(33, 150, 243, 1)',
			//'rgba(3, 169, 244, 1)',
			//'rgba(0, 188, 212, 1)',
			//'rgba(0, 150, 136, 1)',
			//'rgba(76, 175, 80, 1)',
			//'rgba(139, 195, 74, 1)',
			'rgba(205, 220, 57, 1)',
			'rgba(255, 235, 59, 1)',
            //'rgba(255, 193, 7, 1)'
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
		//console.log(color.toRGBA());
		new_color = color.toRGBA();
		
		new_color.pop();
		for(let i = 0; i < 3; i++){
			new_color[i] = new_color[i].toFixed(0);
		}

		  if(orig_endpoint == "set_hex_color"){
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
          disableInteractions();
          $.ajax({
              async: true,
              url: "http://192.168.200.28:5000/" + endpoint + "/" + new_color[0] + "." + new_color[1] + "." + new_color[2],
			  crossDomain: true,
              cache: false,
              success: function(result){
                  enableInteractions();
              }
          });
		
	});
	pickr.on('cancel', () => {
		pickr.hide();
	});
    pickr.on('show', () => {
        
        //doesn't show pickr if we want buttons disabled
        if(disabled){
            pickr.hide();
            return;
        }

    });

}

makePickr("set_color", "set_color");


function makeHex(x, y, r){
	let hex = two.makePolygon(x, h-y, r, 6);	
	hex.fill = 'white';
	hex.stroke = 'black';
	hexagons.add(hex);
}

//hardcoded path just to alleviate time if it doesnt load
let path = [3,3,1,3,3,2,4]

function updatePath(){
      
    $.ajax({
        async: false,
        url: "http://192.168.200.28:5000/get_path",
		crossDomain: true,
        cache: false,
        success: function(result){
            path = result['data']['path'];
        }
    });

	

}

function resizeStructure(){
	two.height = $(window).height()*.3;
    two.width = $('#drawing').width();
	hexagons.translation.set(0,0);
	hexagons.scale = 1;
	hexagons.center();
	hexagons.translation.set(two.width / 2, two.height / 2);
	
	let bounds = hexagons.getBoundingClientRect();
	let bound_h = bounds['height'];
	let bound_w = bounds['width'];

	//This adjusts the hexagons to fit into the canvas no matter what
	hexagons.scale = Math.min(two.height/bound_h, two.width/bound_w);
	//two.update();

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

    updatePath();

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
    getBrightnessSlider();
	resizeStructure();
	two.update();
	attachHexagonClickEvents();
	animateStructureShowing();


}

function getHexColors(){
    
    $.ajax({
        async: true,
        url: "http://192.168.200.28:5000/get_hex_colors",
		crossDomain: true,
        cache: false,
        success: function(result){
            for(let i = 0; i < hexagons.children.length; i++){
                updateHexDiagram(i, result['data'][i]);
            }
        }
    });
	

}

function getBrightnessSlider(){
    
    $.ajax({
        async: false,
        url: "http://192.168.200.28:5000/get_brightness",
		crossDomain: true,
        cache: false,
        success: function(result){
            slider.value = ((parseInt(result['data']['brightness']*100)).toFixed(0));
        }
    });

}

function disableVisualization(){
    hexagons.opacity = 0.5;
    disabled = true;
    two.update();

}

function enableVisualization(){
    hexagons.opacity = 1;
    disabled = false;
    two.update()

}

function disableInteractions(){
    disableVisualization();
    

    var buttons = document.querySelectorAll(".button");
    for (var i=0, l=buttons.length; i<l; i++) {
        buttons[i].disabled = true;
    }
    slider.disabled = true;


}

function enableInteractions(){
    enableVisualization();


    var buttons = document.querySelectorAll(".button");
    for (var i=0, l=buttons.length; i<l; i++) {
        buttons[i].disabled = false;
    }
    slider.disabled = false;
}

function animateStructureShowing(){
	let orig_scale = hexagons.scale;
	hexagons.scale = 0;	
	for(let i = 0; i < 60; i++){
		setTimeout(function(){
			for(let j = 0; j < hexagons.children.length; j++){
				let hexagon = hexagons.children[j];
				//console.log(hexagon);
				hexagon.rotation = hexagon.rotation +  2 * Math.PI / 60;
			}
			hexagons.scale += orig_scale / 60;
			//resizeStructure();
			two.update();
			//console.log(i);


		}, 40*i);

	}
}
setTimeout(function(){
	getHexColors();
	drawStructure();
	animateStructureShowing();
}, 300);

window.addEventListener('resize', () => {
	resizeStructure();
	two.update();
}, true);

