# HelioHex

This repository contains my work for a dynamic LED lighting display project.

### Demo


[![Youtube Demo](https://img.youtube.com/vi/GV5ejh_CZBM/0.jpg)](https://youtu.be/GV5ejh_CZBM)


### Features

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

### Under the Hood

![](images/structure-no-cover.jpg =200x200)
This is how the structure display looks without the light diffusing sheets on top. Each hexagon has a JST connector so that it can connect to any hexagon in whatever way you want to plug them in. 


![](images/individual-hexagon.jpg =200x200)
This is a closer look of each individual hexagon. Each hexagon consists of wood pieces I cut out and glued together. A piece of an individual addressable LED strip is attached to the inner perimeter of each hexagon. At the end of these LED strips are the soldered connections. The wood planks have notches at the bottom of each side for connecting pieces of wire to pass through. The small blue and red wires at the top right connect the ground and 5V wires of the ends of the LED strip together to ensure thatthere is sufficient power that can pass to the entire display.
