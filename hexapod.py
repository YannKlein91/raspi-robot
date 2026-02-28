from adafruit_servokit import ServoKit
import time
from sshkeyboard import listen_keyboard
import sys
import gpiozero

from math import sin,cos,acos,atan,atan2,sqrt,degrees,radians,pi

# --------------- constantes + variables globales --------------- #
speed = 0.015
Droite = ServoKit(channels=16 , address=0x40)
Gauche = ServoKit(channels=16 , address=0x41, reference_clock_speed=30000000) #original value => reference_clock_speed=25000000

#droite
DARcoxa = Droite.servo[0]
DARfemur = Droite.servo[1]
DARtibia = Droite.servo[2]  

DMIcoxa = Droite.servo[4]
DMIfemur = Droite.servo[5]
DMItibia = Droite.servo[6]  

DAVcoxa = Droite.servo[8]
DAVfemur = Droite.servo[9]
DAVtibia = Droite.servo[10]  

#gauche
GARcoxa = Gauche.servo[0]
GARfemur = Gauche.servo[1]
GARtibia = Gauche.servo[2]  

GMIcoxa = Gauche.servo[4]
GMIfemur = Gauche.servo[5]
GMItibia = Gauche.servo[6]  

GAVcoxa = Gauche.servo[8]
GAVfemur = Gauche.servo[9]
GAVtibia = Gauche.servo[10]  

class Leg:
    def __init__(self,coxa,femur,tibia): 
        self.Coxa = coxa
        self.Femur = femur
        self.Tibia = tibia
    def MoveTo(self,cAngle,fAngle,tAngle):
        self.Coxa.angle = cAngle
        self.Femur.angle = fAngle
        self.Tibia.angle = tAngle
        

LegFL = Leg(Gauche.servo[8],Gauche.servo[9],Gauche.servo[10])


coxaMin = 35
coxaMax = 145

femurMin = 0
femurMax = 90

tibiaMin = 5
tibiaMax = 150

STARTSTOP = True

def Start():
    try:
        print("Hexapod ON")
        init()
        listen_keyboard(on_press=on_key_press)
    except KeyboardInterrupt:
        init()
    finally:
        print("Hexapod OFF")
        # quitter le programme
        sys.exit() 

def on_key_press(key):
    global STARTSTOP
    print(f"press : {key}")

    if(key == "i"):
        STARTSTOP = False
        time.sleep(1)
        init()

    elif(key == "t"):
        STARTSTOP = True
        TestMoove()

    elif(key == "1"):
        STARTSTOP = True
        TestCoordinate(DMIcoxa,DMIfemur,DMItibia)
        TestCoordinate(DAVcoxa,DAVfemur,DAVtibia)
        TestCoordinate(DARcoxa,DARfemur,DARtibia)
        TestCoordinate(GMIcoxa,GMIfemur,GMItibia)
        TestCoordinate(GAVcoxa,GAVfemur,GAVtibia)
        TestCoordinate(GARcoxa,GARfemur,GARtibia)


    elif(key == "s"):
        STARTSTOP = False
        init()
        gpiozero.close()
        sys.exit()

    else:
        sys.exit() 


def init():

    LegFL.MoveTo(90,160,160)
    DARcoxa.angle = 90
    DMIcoxa.angle = 90
    DAVcoxa.angle = 90

    GARcoxa.angle = 180-90
    GMIcoxa.angle = 180-90

    DARfemur.angle = 0
    DMIfemur.angle = 0
    DAVfemur.angle = 0

    GARfemur.angle = 180-0
    GMIfemur.angle = 180-0

    DARtibia.angle = 0
    DMItibia.angle = 0
    DAVtibia.angle = 0

    GARtibia.angle = 180-0
    GMItibia.angle = 180-0

def TestMoove():
    c=90
    t=90
    f=45
    upDown = True
    while(STARTSTOP == True):
        DARcoxa.angle = c
        DMIcoxa.angle = c
        DAVcoxa.angle = c

        GARcoxa.angle = 180 - c
        GMIcoxa.angle = 180 - c
        GAVcoxa.angle = 180 - c

        DARfemur.angle = f
        DMIfemur.angle = f
        DAVfemur.angle = f

        GARfemur.angle = 180-f
        GMIfemur.angle = 180-f
        GAVfemur.angle = 180-f   

        DARtibia.angle = t
        DMItibia.angle = t
        DAVtibia.angle = t

        GARtibia.angle = 180 - t
        GMItibia.angle = 180 - t
        GAVtibia.angle = 180 - t

        if(upDown == True):
            c+=1
            f+=1
            t = c
        else:
            f-=1
            c-=1
            t = c
        
        if(c > 130):
            upDown = False
        elif(c < 50):
            upDown = True

        print(f'c = {c}  f = {f}  t = {t}')
        
        time.sleep(0.001)

def inverse_kinematics(pos):
    x, y, z = pos[0],pos[1],pos[2]
     
    coxaLenght = 45
    femurLenght = 80
    tibiaLenght = 140

    # Avoid zero-division
    y += 0.00000001
    z += 0.00000001
    x += 0.00000001

    try:
        L = sqrt(x**2 + y**2)
        Lt = sqrt((L - coxaLenght)**2 + z**2)
        gamma = atan2((L - coxaLenght), z)
        beta = acos((femurLenght**2 + Lt**2 - tibiaLenght**2) / (2*femurLenght*Lt))
        alpha = acos((femurLenght**2 + tibiaLenght**2 - Lt**2) / (2*femurLenght*tibiaLenght))

        # tibia angle adjustment:
        theta1 = (degrees(alpha))

        # femur angle adjustment:
        theta2 = 200 - (degrees(gamma) + degrees(beta)) #200 - (degr...)

        # coxa Base angle:
        theta_base = 90-(degrees(atan2(x, y)))

        return round(theta_base,1), round(theta2,1), round(theta1,1)
    except:
        init()

def ConvertPosToAngle(pos):
    angles = inverse_kinematics(pos)

def TestCoordinate(coxa,femur,tibia):
        
    # initial pos
    x= 0  # 0 beetween -150 and 150
    y= 100 # 100 beetween 200 and 1
    z= 50 # 50 beetween 150 and 30 with y = 150

    angles = inverse_kinematics([x,y,z])
    c = angles[0]
    f = angles[1]
    t = angles[2]

    coxa.angle = c
    femur.angle = f
    tibia.angle = t

    while(z < 150):
        time.sleep(speed)
        z += 1
        angles = inverse_kinematics([x,y,z])
        c = angles[0]
        f = angles[1]
        t = angles[2]

        coxa.angle = c
        femur.angle = f
        tibia.angle = t
    
    time.sleep(3)

    while(z > 50):
        time.sleep(speed)
        z -= 1
        angles = inverse_kinematics([x,y,z])
        c = angles[0]
        f = angles[1]
        t = angles[2]

        coxa.angle = c
        femur.angle = f
        tibia.angle = t
    

if __name__ == "__main__":
    Start()