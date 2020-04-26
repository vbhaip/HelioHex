from flask import Flask, request, jsonify
import light_controller as lc
import spotify_visualizer as sv

app = Flask(__name__)

visualizer = sv.SpotifyVisualizer()
display = visualizer.display

@app.route("/")
def index():
    return "hello"

@app.route("/rainbow_cycle")
def rainbow_cycle():
    display.cycle_through_rainbow() 
    return

@app.route("/play_song", methods=["POST"])
def play_song():
    display.set_color(PINK)
    data = jsonify(request.json)
    return data


def main():
    print("made it here")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
