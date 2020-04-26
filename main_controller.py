from flask import Flask, request, jsonify
import light_controller as lc
import spotify_visualizer as sv
from threading import Thread
from functools import wraps
from credentials import CREDENTIALS

app = Flask(__name__)

visualizer = sv.SpotifyVisualizer()
display = visualizer.display

REPEAT_KWARG = {'repeat': True}

current_thread = [None]

def end_current_thread(foo):
    @wraps(foo)
    def wrapper(*args, **kwargs):
        if current_thread[0] is not None:
            display.continue_process = False
            visualizer.stop() 
            current_thread[0].join()
        return foo(*args, **kwargs)
    return wrapper 

def run_thread(thread):
    current_thread[0] = thread
    current_thread[0].start()

@app.route("/")
def index():
    return "hello"

@app.route("/clear")
@end_current_thread
def clear():
    display.clear()
    return "Display cleared"

@app.route("/rainbow_cycle")
@end_current_thread
def rainbow_cycle():
    #display.cycle_through_rainbow() 
    run_thread(Thread(target=display.cycle_through_rainbow, kwargs=REPEAT_KWARG))
    return "Mode set to Rainbow Cycle"

@app.route("/play_song")
@end_current_thread
def play_song():
    #display.set_color(PINK)
    #data = jsonify(request.json)
    visualizer.should_run_visualizer = True
    run_thread(Thread(target=visualizer.visualize))
    return "Visualizing song" 


def main():
    print(app.url_map)
    app.secret_key = CREDENTIALS['FLASK_SECRET_KEY']
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
