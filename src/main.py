from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue

_debug = False


# TODO: axis-mapping should be OOP and automatic!

try:
    from robot.servo import Servo
    base = Servo(Queue(), 7, verbose=False)
    base.start()

except Exception as e:
    print("Could not import robot")
    print(e)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return "Hello World"


@socketio.on_error_default
def default_error_handler(e):
    print("======================= ERROR")
    print(request.event["message"])
    print(request.event["args"])

@socketio.on('connect')
def test_connect():
    emit('teste', {'data': 'Connected'})

@socketio.on('ping')
def ping():
    emit('pong', {'data': 'pong'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        if _debug: print("[Server] Left: {},{}".format(x,y))
        #linear.q.put(("left",x,y))
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        if _debug: print("[Server] Right: {},{}".format(x,y))
        servo.q.put(("right",x,y))
        #servo2.q.put(("right",y,x))
    elif "A" in data.keys():
        if _debug: print("[Server] A")
        #binary.q.put(("A",1,0))
    elif "B" in data.keys():
        if _debug: print("[Server] B")
        #binary2.q.put(("B",1,0))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port="3005", debug=True, use_reloader=True)