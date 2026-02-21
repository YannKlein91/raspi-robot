from adafruit_servokit import ServoKit
import time
from sshkeyboard import listen_keyboard
import sys

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
    elif(key == "s"):
        STARTSTOP = False
        init()
        sys.exit()
    else:
        sys.exit() 



def init():
    DARcoxa.angle = 90
    DMIcoxa.angle = 90
    DAVcoxa.angle = 90

    GARcoxa.angle = 180-90
    GMIcoxa.angle = 180-90
    GAVcoxa.angle = 180-90  

    DARfemur.angle = 0
    DMIfemur.angle = 0
    DAVfemur.angle = 0

    GARfemur.angle = 180-0
    GMIfemur.angle = 180-0
    GAVfemur.angle = 180-0    

    DARtibia.angle = 0
    DMItibia.angle = 0
    DAVtibia.angle = 0

    GARtibia.angle = 180-0
    GMItibia.angle = 180-0
    GAVtibia.angle = 180-0     

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

"""
def testAxis(key):
        # initial pos
        x= 0  # 0 beetween -150 and 150
        y= 150 # 100 beetween 200 and 1
        z= 50 # 50 beetween 150 and 30 with y = 150

        angles = inverse_kinematics([x,y,z])
        c = angles[0]
        f = angles[1]
        t = angles[2]

        coxa.angle = c
        femur.angle = f
        tibia.angle = t

        time.sleep(1)

        # move one side
        while(x < 150):
            x += 1
            angles = inverse_kinematics([x,y,z])
            c = angles[0]
            f = angles[1]
            t = angles[2]

            coxa.angle = c
            femur.angle = f
            tibia.angle = t
            time.sleep(speed)

        # move to the other side
        while(x > -150):
            x -= 1
            angles = inverse_kinematics([x,y,z])
            c = angles[0]
            f = angles[1]
            t = angles[2]

            coxa.angle = c
            femur.angle = f
            tibia.angle = t
            time.sleep(speed)



        # initial pos
        
        time.sleep(1)

        x= 0  # beetween -100 and 100
        y=100
        z=50

        angles = inverse_kinematics([x,y,z])
        
        c = angles[0]
        f = angles[1]
        t = angles[2]

        coxa.angle = c
        femur.angle = f
        tibia.angle = t
        

       # coxa.angle = c
        #femur.angle = f
        #tibia.angle = t

        
        print(f'c = {c} / f = {f} / t = {t}')

        #init()

        upDown = True
        while(STARTSTOP == True):
            time.sleep(0.005)
            if(key == 'x'):
                if(upDown == True):
                    x = x+1
                else:
                    x = x-1
                if(x > 100):
                    upDown = False
                elif(x < -100):
                    upDown = True
            elif(key == 'y'):
                if(upDown == True):
                    y = y+1
                else:
                    y = y-1
                if(y > 140):
                    upDown = False
                elif(y < 60):
                    upDown = True
            elif(key == 'z'):
                if(upDown == True):
                    z = z+1
                else:
                    z = z-1
                if(z > 150):
                    upDown = False
                elif(z < 50):
                    upDown = True
            
            angles = inverse_kinematics([x,y,z])
            c = angles[0]
            f = angles[1]
            t = angles[2]

             #print(f'x={x} y={y} z={z}')
            print(f'c = {c} / f = {f} / t = {t}')

            
           # if c < coxaMin or c > coxaMax or f < femurMin or f > femurMax or t < tibiaMin or t > tibiaMax:
            #   print(f'limite servo atteinte : c = {c} / f = {f} / t = {t}')

           # else:
            #    coxa.angle = c
            #    femur.angle = f
            #    tibia.angle = t
"""



# ----------------------------------------------------------------  Inverse Kinematics  -------------------------------------------------------



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
































def coordinate_to_degrees(x,y):
    x += 0.00001

    if (x >= 0 and y >= 0):
        angle = degrees(atan(y/x))
    elif(x < 0 and y >= 0):
        angle = 180 + degrees(atan(y/x))
    elif(x < 0 and y < 0):
        angle = 180 + degrees(atan(y/x))
    elif(x < 0 and y >= 0):
        angle = 360 + degrees(atan(y/x))
    
    return round(angle,1)

def OLDIK(pos):
    try:
        x, y, z = pos[0],pos[1],pos[2]
        x += 0.0000001 # évitons les divisions par 0

        coxa = 45
        femur = 80
        tibia = 140

        offset = 0 # à modifier pour chaque pied

        theta1 = coordinate_to_degrees(x, y) - offset

        #décalage du point 0,0,0 par rapport à la longueur de coxa pour avoir ce point à la jointure de coxa
        x -= coxa*cos(radians(theta1))
        y -= coxa*sin(radians(theta1))

        if theta1 > 180:
            theta1 -= 360
    
        p = sqrt(x**2 + y**2)

        if sqrt(x**2 + y**2 + z**2) > femur + tibia:
            print("MATH ERROR: coordinate too far")
            return[0,90,100]
    
        alpha = atan(z/p)

        c = sqrt(p**2 + z**2)

        beta = acos((femur**2 + c**2 - tibia**2)/(2*femur*c))
        theta2 = beta + alpha
        #theta3 = acos((tibia**2+femur**2-c**2)/(2*tibia*femur)) #- pi
        theta3 = acos((tibia**2+femur**2-c**2)/(2*tibia*femur))

        return round(theta1,1), round(180-degrees(theta2),1), round(degrees(theta3),1)
    except KeyboardInterrupt:
        return[0,90,100]





if __name__ == "__main__":
    Start()

# ----------------------------------------------------------------  Inverse Kinematics  -------------------------------------------------------
"""
def walk2():
    femur.angle = 22
    tibia.angle = 30
    c = coxa.angle
    f = femur.angle
    t = tibia.angle
    vector = True

    coxaMin = 90
    coxaMax = 145

    femurMin = 22
    femurMax = 43

    tibiaMin = 30
    tibiaMax = 75


    while(STARTSTOP == True):
        
        if(c>coxaMax):
            vector = False
            print(f"MIN coxa = {c} / femur = {f} / tibia = {t}" ) 
                
        elif(c<coxaMin):
            vector = True
            print(f"MAX coxa = {c} / femur = {f} / tibia = {t}" ) 
            
        if(vector == True):
            c = c + 1
            f = f + 0.363
            t = t + 0.82
            
        else: 
            c = c - 1
            f = f - 0.363
            t = t - 0.82
            
            
        #f = ((c * femurMax) / coxaMin) - femurMin

        #t = (((c * tibiaMax) / coxaMin) - tibiaMin)
        
        coxa.angle = c
        femur.angle = f
        tibia.angle = t


        print(f"coxa = {c} / femur = {f} / tibia = {t}" ) 
        time.sleep(speed)
    

def walk():
    c = coxa.angle
    f = femur.angle
    t = tibia.angle
    vector = True

    while(STARTSTOP == True):
        
        if(c>150):
            vector = False
            #pause la patte au sol
                #while(t>10):
                #t = t - 1
                #tibia.angle = 90 #t
                #time.sleep(speed)
                
        elif(c<30):
            vector = True
            
        if(vector == True):
            #leve le pied et avance la patte
            c = c + 1
            t = t + 1
        else:
            #recule et pousse la patte 
            c = c - 1
            if(c>90):
                f = f - 0.5
            else:
                f = f + 0.5

        print(f"coxa = {c} / femur = {f} / tibia = {t}" )
        tibia.angle = 90 #t 
        coxa.angle = c
        if(f<0):
            f=0
        femur.angle = f
        time.sleep(speed)

def ManualServoSetting(key):

    if(key == '1'):
        coxa.angle = coxa.angle + 1
    elif(key == '2'):
        coxa.angle = coxa.angle - 1

    if(key == '4'):
        femur.angle = femur.angle + 1
    elif(key == '5'):
        femur.angle = femur.angle - 1

    if(key == '7'):
        tibia.angle = tibia.angle + 1
    elif(key == '8'):
        tibia.angle = tibia.angle - 1

    print(f"coxa = {coxa.angle} / femur = {femur.angle} / tibia = {tibia.angle}" )

""" 
