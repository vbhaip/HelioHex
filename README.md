# HelioHex

This repository contains my work for a dynamic LED lighting display project.

## Demo


[![Youtube Demo](https://img.youtube.com/vi/GV5ejh_CZBM/0.jpg)](https://youtu.be/GV5ejh_CZBM)

^ Click on the image to watch the Youtube video and see it in action!

## Features

* Different lighting 'modes' - examples include:
	* Set the color of the whole display
	* Set the color of individual hexagons
	* Generate a random aesthetically-pleasing color palette
	* Sync the color of the display to the time of the day
* Spotify integration
	* Matches up the colors of each hexagon to the features of the song playing
	* Changes depending on the emotions of the song e.g. sadder songs are more blue
* Adaptable web controller - use any device on the network to control the device
	* Control all the different modes and brightness of the display
	* Shows a virtual visualization of the display
* Flexible design
	* Arrange the hexagons in whatever pattern you like - change the settings in one file and everything automatically updates
	* Each hexagon acts as its own unit - if you build more hexagons, you can easily expand the structure

## Under the Hood

<img src="images/structure-no-cover.jpg" width="275" height="200">
This is how the structure display looks without the light diffusing sheets on top. Each hexagon has a JST connector so that it can connect to any hexagon in whatever way you want to plug them in. 


<img src="images/individual-hexagon.jpg" width="200" height="200">
This is a closer look at each individual hexagon. Each hexagon consists of wood pieces I cut out and glued together. A piece of an individual addressable LED strip is attached to the inner perimeter of each hexagon. At the end of these LED strips are the connectors to link to other hexagons. The wood planks have notches at the bottom of each side for connecting the wires of each hexagon. The small blue and red wires at the top right connect the ground and 5V wires of the ends of the LED strip together to ensure that there is sufficient power that can pass to the entire display. Each hexagon is independent from the others in the way that I can make another hexagon and easily attach it to the display without changing the other hexagons.

<br/><br/>

Acrylic sheets diffuse the light from the LED strips. For now, I used parchment paper since I don't have access to a laser cutter to cut out the acrylic sheet (acrylic is very brittle and cracked each time I cut it).


## Materials and Costs 

| Material | Where to find it | Cost |
| -- | -- | -- |
| LED Strip | https://www.amazon.com/CHINLY-Individually-Addressable-Waterproof-waterproof/dp/B06XNJSKXN/ref=sr_1_5 | $29.90 |
| JST Connectors | https://www.amazon.com/ALITOVE-Female-Connector-WS2812B-SK6812-RGBW/dp/B071H5XCN5/ref=sr_1_5 | $10.99 |
| Remote Controller | https://www.amazon.com/dp/B075SXMD9Z/ref=sspa_dk_detail_3 | $8.99 |
| Plywood | https://www.homedepot.com/p/Utility-Panel-Common-1-8-in-x-4-ft-x-8-ft-Actual-0-106-in-x-48-in-x-96-in-833096/100543684 (might not be the exact one I used, need to double check) | $11.42 |
| Acrylic Light Panel | https://www.homedepot.com/p/OPTIX-23-75-in-x-47-75-in-White-Acrylic-Light-Panel-1A20084A/100564898 | $12.48 |
| Raspberry Pi 4 | https://www.microcenter.com/product/608436/raspberry-pi-4-model-b---2gb-ddr4 | $35.00 |
| 40 Amp Power Supply | https://www.amazon.com/CHINLY-Universal-Regulated-Switching-Transformer/dp/B01LZRIWZD/ref=sr_1_4 | $20.99 |
| Hot glue, super glue, push pins, clamps, etc. | - | $30.00 |
| **Total** | - | **$159.77** |


## How does it work? 

<img src="images/diagram.png" width="800" height="600">

This is a simplified diagram, but should give you an idea for how it works.


## Code

| File | Description |
| -- | -- |
| [main_controller.py](main_controller.py) | Runs a local Flask server that is on the Raspberry Pi. Endpoints control lighting modes of the display and return information on current display state. |
| [light_controller.py](light_controller.py) | Holds the Hexagon class and Structure class for the low level controlling of lighting modes. |
| [structure_settings.py](structure_settings.py) | Configurations file for the display. [light_controller.py](light_controller.py) reads from this file to determine the pattern of the display. |
| [spotify_visualizer.py](spotify_visualizer.py) | Contains the SpotifyVisualizer class that syncs the display to pitch and loudness information on the song currently playing on Spotify. The visualization uses functions to interpolate pitch and loudness over time and samples from it. |
| [spotify_visualizer_v2.py](spotify_visualizer_v2.py) | Updated version of [spotify_visualizer.py](spotify_visualizer.py). Uses a probabilistic sampling from pitch and loudness data and includes improvements to reflect emotions in the song. |
| [Spotify Analysis Testing.xlsx](<Spotify Analysis Testing.xlsx>) | Analysis of data from Spotify, containing graphs I created to better understand the data. |
| [Project Diagram.afdesign](<Project Diagram.afdesign>) | Diagram for how everything works on a high-level (shown in the README)|
| [clear.py](clear.py) | Short script to turn off all the lights - used when testing. |
| [images/](images/) | Contains images used in the README. |
| [heroku-app/](heroku-app/) | Contains Flask server that acts as a web controller for the display. Hosted on a Heroku server to be accessible from any device at http://heliohex.herokuapp.com. (You can access this website, but it will only work when you are on the network.) |
| [heroku-app/app.py](heroku-app/app.py) | Serves Flask server for the webpage. |
| [heroku-app/Controller Mockup.afdesign](<heroku-app/Controller Mockup.afdesign>) | Mockup of web controller in Affinity Designer. |
| [heroku-app/templates/index.html](heroku-app/templates/index.html) | Webpage for web controller. |
| [heroku-app/static](heroku-app/static) | Javascript and CSS for web controller. |
