from flask import Flask, render_template
import urllib.request
import os

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
	return render_template('index.html') 

@app.route("/ping_spotify")
def ping_spotify():
	urllib.request.urlopen(os.environ['RPI_BASE_URL'] + "play_song")
	return (''), 204

@app.route("/flash_around")
def flash_around():
	urllib.request.urlopen(os.environ['RPI_BASE_URL'] + "flash_around")
	return (''), 204

@app.route("/rainbow_wheel")
def rainbow_wheel():
	urllib.request.urlopen(os.environ['RPI_BASE_URL'] + "rainbow_cycle")
	return (''), 204

@app.route("/set_color")
def set_color():
	urllib.request.urlopen(os.environ['RPI_BASE_URL'] + "set_color/200.200.0")
	return (''), 204

app.jinja_env.globals.update(ping_spotify=ping_spotify, flash_around=flash_around, rainbow_wheel=rainbow_wheel, set_color=set_color)

def main():
	app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
	main()
