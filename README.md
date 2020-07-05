# HelioHex

This repository contains my work for a dynamic LED lighting display project.

## Demo


[![Youtube Demo](https://img.youtube.com/vi/8TQva79vo88/0.jpg)](https://youtu.be/8TQva79vo88)

^ Click on the image to watch the Youtube video and see it in action!

## Features

* Different lighting 'modes'
	* Set the color of the whole display
	* Set the color of individual hexagons
	* Generate a random aesthetically-pleasing color palette
	* Sync the color of the display to the time of the day
* Spotify integration
	* Matches up the colors of each hexagon to the features of the song playing
	* Changes depending on the emotions of the song e.g. sadder songs are more blue
* Adaptable web controller
	* Use any device on the network to control the device
	* Control all the different modes and brightness of the display
	* Shows a virtual visualization of the display
* Flexible design
	* Arrange the hexagons in whatever pattern you like - change the settings in one file and everything automatically updates
	* Expand the structure easily if you build more hexagons

Check out the full post-mortem here: https://vinaybhaip.com/blog/2020/07/05/heliohex.

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
