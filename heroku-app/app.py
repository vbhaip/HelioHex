from flask import Flask, render_template, redirect, url_for, request, session, make_response
import requests
import urllib.request
import os
import sys
import time
import json
import urllib

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ["FLASK_SECRET"]

@app.route("/")
def index():
        response = make_response(render_template('index.html'))
        response.set_cookie('token', session.get('spotify_token', "null"))
        return response

@app.route("/callback")
def callback():
        #make post request to exchange auth code for token
        code = request.args.get('code')

        body = {}
        body['grant_type'] = 'authorization_code'
        body['code'] = code
        body['redirect_uri'] = "http://heliohex.herokuapp.com/callback"
        body['client_id'] = os.environ['SPOTIFY_CLIENT_ID']
        body['client_secret'] = os.environ['SPOTIFY_CLIENT_SECRET']

        response = requests.post('https://accounts.spotify.com/api/token', data=body)
        print(response.text)
        sys.stdout.flush()

        tosend = response.json()

        #if authentication goes wrong, nothing will happen
        if "error" in tosend or "expires_in" not in tosend:
            return redirect(url_for('index'))

        tosend['expires_at'] = int(tosend['expires_in']) + time.time()
        #tosend = urllib.parse.urlencode(tosend)
        #tosend = json.dumps(tosend)
        tosend = str(tosend)

        #requests.post(os.environ['RPI_BASE_URL'] + "authenticate_spotify", data=tosend)
        session['spotify_token'] = tosend

        return redirect(url_for('index'))

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

app.jinja_env.globals.update(ping_spotify=ping_spotify, flash_around=flash_around, rainbow_wheel=rainbow_wheel, set_color=set_color, callback=callback)

def main():
	app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
	main()
