# --------------- imports --------------- #
#import gpiod # in venv, pip install gpiod
#from gpiod.line import Direction, Value
#from adafruit_servokit import ServoKit
#from evdev import InputDevice, ecodes
#import time
#import os



"""
def Start():
    print("RCCARE ON")
    kit.servo[0].angle = 90
    kit.servo[2].angle = 90

    file_path = '/dev/input/event5'
    while (os.path.exists(file_path) == False):
        print('manette non connectée')
        time.sleep(5)

    dev = InputDevice('/dev/input/event5')
    print('manette connectée : A => avancer / B => reculer / joystick gauche => direction')
    for event in dev.read_loop():
        if event.code == ecodes.ABS_RZ and event.value != 0:
            if event.value < 10000:
               kit.servo[2].angle = 0
            elif event.value > 50000:
                kit.servo[2].angle = 180
            else :
                kit.servo[2].angle = 90
        elif event.code == ecodes.ABS_Y and event.value != 0:  
            if event.value < 10000:
               kit.servo[0].angle = 0
            elif event.value > 50000:
                kit.servo[0].angle = 180
            else :
                kit.servo[0].angle = 90
                
                
        
        elif event.code == ecodes.ABS_Y and event.value != 0:    
            kit.servo[0].angle = 90
        
        
        
        if event.code == ecodes.BTN_A or event.code == ecodes.BTN_B:
            ServoPropulsion(event.code, event.value)
        

         elif event.code == ecodes.ABS_X and event.value != 0:
            if event.value < 10000:
                ServoDirection("g")
            elif event.value > 50000:
                ServoDirection("d")
            else :
                ServoDirection("m")

# --------------- PROPULSION --------------- #

def PROPULSION(value):
    if(value == 90 and kit.servo[1].angle > 90) :
        kit.servo[1].angle = 90
    else :
        kit.servo[1].angle = value

# gestion du servomoteur pour la direction des roues avant arrière
def ServoPropulsion(key,value):
    if(value == 1):
        if key == ecodes.BTN_A :
            PROPULSION(0)
        elif key == ecodes.BTN_B:
            PROPULSION(150)
    else :
        PROPULSION(90)

# --------------- DIRECTION --------------- #

def DIRECTION(value):
    kit.servo[0].angle = value
    kit.servo[2].angle = value 

# gestion du servomoteur pour la direction des roues gauche droite
def ServoDirection(key):
    if key == "g" :
        DIRECTION(180)
    elif key == "d" :
        DIRECTION(00)
    else :
        DIRECTION(90)

"""



"""

#from gpiozero import AngularServo
#from sshkeyboard import listen_keyboard
#import evdev
#import xbox

GPIO17 = 17
GPIO18 = 18

global RedOnOff # gyrophare on/off
RedOnOff = False
global ledRedReq
ledRedReq = gpiod.request_lines(
        "/dev/gpiochip4",
        consumer="led",
        config={GPIO17: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}
        ) # initialisation de GPIO 17 pour le gyrophare

global BlueOnOff # gyrophare on/off
BlueOnOff = False

            #print(f"Bouton A {event.value}")

# led Rouge on/off
def RedLed() :
     # on veux utiliser ces variables globals
    global RedOnOff
    global ledRedReq

    #inversion on/off
    RedOnOff = not RedOnOff

    if RedOnOff :
        ledRedReq.set_value(GPIO17, Value.ACTIVE) # allume led
    else :
        ledRedReq.set_value(GPIO17, Value.INACTIVE) # éteind led 

# led Bleu on/off
def BlueLed() :
     # on veux utiliser ces variables globals
    global BlueOnOff
    global GPIO18Req

    #inversion on/off
    BlueOnOff = not BlueOnOff

    if BlueOnOff :
        GPIO18Req.set_value(GPIO18, Value.ACTIVE) # allume led
    else :
        GPIO18Req.set_value(GPIO18, Value.INACTIVE) # éteind led 


# gyrophare
def Gyro() :
     # on veux utiliser ces variables globals
    global GYRO
    global ledRedReq

    #inversion on/off
    GYRO = not GYRO

    try:
        while GYRO == True:
            ledRedReq.set_value(GPIO17, Value.ACTIVE) # allume led
            time.sleep(1) # attend 1s
            ledRedReq.set_value(GPIO17, Value.INACTIVE) # éteind led
            time.sleep(1) # attend 1s
    except KeyboardInterrupt:
        ledRedReq.set_value(GPIO17, Value.INACTIVE)


# touche clavier enfoncée
def on_key_press(key):
    print(f"press : {key}")
    if(key == "d" or key == "q"):
        ServoDirection(key)
    if(key == "z" or key == "s"):
        ServoPropulsion(key)


# touche clavier relachée
def on_key_release(key):
    print(f"release : {key}")
    if(key == "d" or key == "q"):
        DIRECTION(90)
    if(key == "z" or key == "s"):
        PROPULSION(100)
"""       

"""



    #for ev in evdev.InputDevice("/dev/input/event0").

    
    kit.servo[2].angle =100
    kit.servo[3].angle = 90
    listen_keyboard(on_press=on_key_press,on_release=on_key_release)



    print(f"Release:  {key}")


                BROUILLON



from flask import Flask, Response
from picamera2 import Picamera2
import cv2

### You can donate at https://www.buymeacoffee.com/mmshilleh 

app = Flask(__name__)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

"""





"""
# touche clavier lachée
def on_key_release(key):
    print("Key released: ", key)
"""

    
"""

CAMERA STREAMING OK

import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

"""
"""

PAGE = """"""\"""" """
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""
"""
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    address = ('', 7123)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam2.stop_recording()

"""    