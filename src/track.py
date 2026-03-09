from evdev import InputDevice, ecodes # manette xbox
#from sshkeyboard import listen_keyboard # clavier
from gpiozero import  Motor, PWMOutputDevice

import time
import sys
import os
import ledControl

pLeft ='left'
pRight = 'right'

pMotorL = Motor(forward=17,backward=22)
pPwmL = PWMOutputDevice(27)
pPwmL.value = 0

pMotorR = Motor(forward=23,backward=24)
pPwmR = PWMOutputDevice(25)
pPwmR.value = 0

pSPEED = 0 # valeur comprise entre 0 et 1

def Start():
        try:
            ledControl.TurnLed(ledControl.Rouge,True)
            #ledControl.Rouge.value = True
            print("MARCHE ON")
            #  listen_keyboard(on_press=on_key_press) # clavier
            Controller()
        except KeyboardInterrupt:
            Close()
        finally:
            Close()

def Controller():
            global pSPEED
            pSPEED = ledControl.MinimalSpeed()

            #connexion à la manette
            file_path = '/dev/input/event5'
            while (os.path.exists(file_path) == False):
                print('manette non connectée')
                time.sleep(5)
            dev = InputDevice('/dev/input/event5')
            print('manette connectée')
            #lecture des touches
            for event in dev.read_loop():
                
                #joystick droit
                if event.code == ecodes.ABS_RZ: 
                    #joystick au milieu
                    if(event.value > 30000 and event.value < 40000): 
                        Stop(leftRight=pRight)
                    #joystick actionné
                    else: 
                        GO(leftRight=pRight,value=event.value)
                
                #joystick gauche
                elif event.code == ecodes.ABS_Y:   
                    #joystick au milieu
                    if(event.value > 30000 and event.value < 40000): 
                        Stop(leftRight=pLeft)
                    #joystick actionné
                    else:  
                        GO(leftRight=pLeft,value=event.value)

                #bouton RB appuyé
                elif event.code == ecodes.BTN_TR and event.value == 1: 
                    pSPEED = ledControl.SpeedIndicator(True)
                    print(pSPEED)
                
                #bouton LB appuyé
                elif event.code == ecodes.BTN_TL and event.value == 1: 
                    pSPEED = ledControl.SpeedIndicator(False)
                    print(pSPEED)

                #bouton start appuyé
                elif event.code == ecodes.BTN_START and event.value == 1: 
                    Close(shutdown = True)

                #bouton select appuyé
                elif event.code == ecodes.BTN_SELECT and event.value == 1: 
                    Close()

def GO(leftRight, value):
    # moteur gauche ou droite
    if(leftRight == pLeft):
        pwm = pPwmL  
        motor = pMotorL
    else:
        pwm = pPwmR  
        motor = pMotorR
    # vitesse
    speed = 0
    while(speed < pSPEED):
        speed = speed+0.1
        if(speed > 1):
             speed = 1.0
        pwm.value = speed
        time.sleep(0.001)
        print(leftRight,' speed :',speed)
    # direction
    if(value > 30000):
        motor.backward()
    else:
        motor.forward()

def Stop(leftRight):
    # moteur gauche ou droite
    if(leftRight == pLeft):
        pPwmL.value = 0
        pMotorL.stop()
    else:
        pPwmR.value = 0
        pMotorR.stop()

def Close(shutdown = False):
        Stop(leftRight=pRight)
        Stop(leftRight=pLeft)
        ledControl.LedsOff()
        print("MARCHE OFF")
        if(shutdown == True):
            # éteindre raspi
            os.system('sudo shutdown now') 
        else:
            # quitter le programme
            sys.exit() 

if __name__ == "__main__":
    Start()



"""
i2c = busio.I2C(SCL, SDA)
# Initialise the PCA9685 using the default address (0x40).
pca = PCA9685(i2c, address=0x40)
pca.frequency = 100
#pca.channels[0].duty_cycle = 0xFFFF
motor4 = motor.DCMotor(pca.channels[0], pca.channels[1])
motor4.decay_mode = motor.SLOW_DECAY
"""

"""


def LeftGo(value):
    pwm2.value = SPEED
    print('left speed :',SPEED)
    if(value > 30000):
        motor2.forward()
    else:
        motor2.backward()

def RightGo(value):
    pwm1.value = SPEED
    print('right speed :',SPEED)
    if(value > 30000):
        motor1.forward()
    else:
        motor1.backward()

def on_key_press(key):  # clavier
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