from evdev import InputDevice, ecodes
from sshkeyboard import listen_keyboard
from gpiozero import  Motor, PWMOutputDevice

import time
import sys
import os
import ledControl


motor1 = Motor(forward=17,backward=22)
pwm1 = PWMOutputDevice(27)
pwm1.value = 0

motor2 = Motor(forward=23,backward=24)
pwm2 = PWMOutputDevice(25)
pwm2.value = 0


"""
i2c = busio.I2C(SCL, SDA)
# Initialise the PCA9685 using the default address (0x40).
pca = PCA9685(i2c, address=0x40)
pca.frequency = 100
#pca.channels[0].duty_cycle = 0xFFFF
motor4 = motor.DCMotor(pca.channels[0], pca.channels[1])
motor4.decay_mode = motor.SLOW_DECAY
"""

def Start():
    try:
        print("MARCHE ON")
        ledControl.Led(ledControl.rouge,True)
        # listen_keyboard(on_press=on_key_press)
        file_path = '/dev/input/event5'
        while (os.path.exists(file_path) == False):
            print('manette non connectée')
            time.sleep(5)

        dev = InputDevice('/dev/input/event5')
        print('manette connectée : A => avancer / B => reculer / joystick gauche => direction')
        for event in dev.read_loop():
            if event.code == ecodes.ABS_Y: #joystick droit
                if(event.value > 30000 and event.value < 40000):
                    RightStop()
                else:
                    RightGo(event.value)
            
            elif event.code == ecodes.ABS_RZ:   #joystick gauche
                if(event.value > 30000 and event.value < 40000):
                    LeftStop()
                else:
                    LeftGo(event.value)

            elif event.code == ecodes.BTN_TR and event.value == 1: #bouton RB
                ledControl.SpeedIndicator(True)
                
            elif event.code == ecodes.BTN_TL and event.value == 1: #bouton LB
                ledControl.SpeedIndicator(False)

            elif event.code == ecodes.BTN_START and event.value == 1: #bouton start
                Close()
    
        ledControl.Led(ledControl.rouge,False)

    except KeyboardInterrupt:
        Close()
    finally:
        Close()


def LeftGo(value):
    pwm2.value = 0.7
    if(value > 30000):
        motor2.backward()
    else:
        motor2.forward()

def RightGo(value):
    pwm1.value = 1
    if(value > 30000):
        motor1.forward()
    else:
        motor1.backward()

def LeftStop():
    pwm2.value = 0
    motor2.stop()

def RightStop():
    pwm1.value = 0
    motor1.stop()

def Close():
        LeftStop()
        RightStop()
        ledControl.LedsOff()
        print("MARCHE OFF")

"""
def on_key_press(key):
    print(f"press : {key}")
    if(key == "z"):
        pwm2.value = 0.5
        pwm1.value = 0.5
        motor1.forward()
        motor2.backward()
    elif(key == "s"):
        pwm2.value = 0.2
        pwm1.value = 0.2
        motor1.forward()
        motor2.backward()
    elif(key == "d"):
        pwm2.value = 0
        pwm1.value = 0
    elif(key == "q"):
        pwm2.value = 0
        pwm1.value = 0
        motor1.stop()
        motor2.stop()
        motor1.close()
        motor2.close()
        sys.exit()

"""












"""

def Turn():
    angle = 90
    while(OnOff == True):
        while(angle < 180):
            time.sleep(0.01)
            #kit.servo[14].angle = angle  
            kit.servo[15].angle = angle    
            angle = angle + 1
            print(angle)
        while(angle > 00):
            time.sleep(0.01)
            #kit.servo[14].angle = angle
            kit.servo[15].angle = angle    
            angle = angle - 1
            print(angle)

def InitialiseAngle():
    angle = kit.servo[14].angle
    while(angle > 91 or angle < 89):
        while(angle < 90):
            time.sleep(0.01)
            kit.servo[14].angle = angle    
            angle = angle + 1
            print(angle)
        while(angle > 90):
            time.sleep(0.01)
            kit.servo[14].angle = angle    
            angle = angle - 1
            print(angle)

def UpDown():
    angle = 90
    while(True):
        while(angle < 90):
            time.sleep(0.01)
            kit.servo[8].angle = angle    
            angle = angle + 1
            print(angle)
        while(angle > 0):
            time.sleep(0.01)
            kit.servo[8].angle = angle    
            angle = angle - 1
            print(angle)

        
"""