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
            current_thread[0] = None
        return foo(*args, **kwargs)
    return wrapper 

def run_thread(thread):
    current_thread[0] = thread
    current_thread[0].start()

@app.route("/")
def index():
    print("wassup")
    return "hello"

@app.route("/clear")
@end_current_thread
def clear():
    display.clear()
    return "Display cleared"

@app.route("/cycle_through_rainbow")
@end_current_thread
def cycle_through_rainbow():
    #display.cycle_through_rainbow() 
    run_thread(Thread(target=display.cycle_through_rainbow, kwargs=REPEAT_KWARG))
    return "Mode set to Cycle through Rainbow"

@app.route("/rainbow_wheel")
@end_current_thread
def rainbow_wheel():
    #display.cycle_through_rainbow() 
    run_thread(Thread(target=display.rainbow_cycle, args=[0.01],  kwargs=REPEAT_KWARG))
    response = jsonify({"data": "Mode set to Rainbow Cycle"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/play_song")
@end_current_thread
def play_song():
    #display.set_color(PINK)
    #data = jsonify(request.json)
    visualizer.should_run_visualizer = True
    run_thread(Thread(target=visualizer.visualize))
    response = jsonify({"data": "Visualizing song"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/set_color/<string:rgb>")
@end_current_thread
def set_color(rgb):
    color = tuple(int(x) for x in rgb.split("."))
    display.set_color(color)
    response = jsonify({"data": "Color set to %s" % str(color)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/set_hex_color/<int:hex_num>/<string:rgb>")
@end_current_thread
def set_hex_color(hex_num, rgb):
    color = tuple(int(x) for x in rgb.split("."))
    display.hexagons[hex_num].set_color(color)
    response = jsonify({"data": "Color set to %s" % str(color)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 


@app.route("/flash_around")
@end_current_thread
def flash_around():

    run_thread(Thread(target=display.flash_around, args=[3], kwargs=REPEAT_KWARG))

    response = jsonify({"data": "Flashing around"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/set_brightness/<float:b>")
@app.route("/set_brightness/<int:b>")
def set_brightness(b):
    display.set_brightness(b)
    response = jsonify({"data": "Brightness set to %f" %b})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/get_brightness")
def get_brightness():
    response = jsonify({"data": {"brightness": display.brightness}})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

@app.route("/get_hex_colors")
def get_hex_colors():
    colors = {}
    for i in range(len(display.hexagons)):
        colors[i] = display.hexagons[i].color

    response = jsonify({"data": colors})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 


def main():
    print(app.url_map)
    #print(app.request.host_url)
    context = ('cert.pem', 'key.pem')
    app.secret_key = CREDENTIALS['FLASK_SECRET_KEY']
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
