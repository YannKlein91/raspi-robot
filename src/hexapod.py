import adafruit_servokit
from adafruit_servokit import ServoKit
import time
from sshkeyboard import listen_keyboard
import sys

import threading

from math import sin,cos,acos,atan,atan2,sqrt,degrees,radians,pi
import math

# --------------- constantes + variables globales --------------- #

speed = 0.003

Right = ServoKit(channels=16 , address=0x40)
Left = ServoKit(channels=16 , address=0x41, reference_clock_speed=35000000) #original value => reference_clock_speed=25000000 OK

coxaMin = 35
coxaMax = 145

femurMin = 0
femurMax = 90

tibiaMin = 5
tibiaMax = 150

STARTSTOP = True


class Leg:
    """
    définition d'une patte
        
    """

    def __init__(self,invert,coxa,femur,tibia,ajustCoorDir):
        """
        initialisation de la position des pattes
        
        """
        self.Invert = invert 
        self.Coxa = coxa
        self.Femur = femur
        self.Tibia = tibia
        self.AjustCoorDir = ajustCoorDir
        self.X = 0
        self.Y = 60
        self.Z = 50

    def SetAngles(self,cAngle,fAngle,tAngle):
        """
        déplacemnt sur position angulaire
        avec ajustement gauche / droite + inversion de l'instalation des femurs / tibias 
        
        """
        if(self.Invert == True):
            # coté gauche => femur et tibia sont plié à 180° et déplié à 0°, coté droit c'est l'inverse
            fAngle = 180 - fAngle
            tAngle = 180 - tAngle
            # ajustement coxa gauche droite pour s'alligner sur l'axe avant / arrière
            cAngle = 180 - cAngle
        
        #if(fAngle > 180 or fAngle < 0):
            #print(f"!!!!!!!!!!!!!!!!!!!!!   femur = {fAngle}    X = {self.X}  Y = {self.Y}  Z = {self.Z}    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(fAngle > 180):
            fAngle = 180
        elif(fAngle < 0):
            fAngle = 0

        self.Coxa.angle = cAngle
        self.Femur.angle = fAngle
        self.Tibia.angle = tAngle


    def Transform(self,x,y,z):
        """
        déplacement directe à une coordonné x,y,z
        avec : 
            * ajustement de la coordoné x des pattes selon : avant / arrière
            * ajustement de l'instalation des 45° des pattes avants / arrière
        
        """
        self.X = x
        self.Y = y
        self.Z = z
        ajustCoxa = 0
        if(self.AjustCoorDir == 1):
            x += 80
            ajustCoxa += 45
        elif(self.AjustCoorDir == -1):
            x -= 70
            ajustCoxa -= 45

        angles = Inverse_kinematics([x,y,z])
        self.SetAngles(angles[0] + ajustCoxa, angles[1], angles[2])


    def Proceed(self,x,y,z):
        """
        déplacement progressif vers une coordonnée x,y,z
        un premier appel de Transform() est obligatoire pour initialiser correctement x,y,z ( à revoir )  

        """
        while(self.X != x or self.Y != y or self.Z != z):    
            if(self.X > x):
                self.X -= 1
            elif(self.X < x):
                self.X += 1
            if(self.Y > y):
                self.Y -= 1
            elif(self.Y < y):
                self.Y += 1
            if(self.Z > z):
                self.Z -= 1
            elif(self.Z < z):
                self.Z += 1
            time.sleep(speed)
            self.Transform(self.X,self.Y,self.Z)
            
        
# --------------- Liste des 6 pattes --------------- #

LegFL = Leg(True,Left.servo[8],Left.servo[9],Left.servo[10],+1)
LegML = Leg(True,Left.servo[4],Left.servo[5],Left.servo[6],0)
LegBL = Leg(True,Left.servo[0],Left.servo[1],Left.servo[2],-1)

LegFR = Leg(False,Right.servo[8],Right.servo[9],Right.servo[10],+1)
LegMR = Leg(False,Right.servo[4],Right.servo[5],Right.servo[6],0)
LegBR = Leg(False,Right.servo[0],Right.servo[1],Right.servo[2],-1)


def On_key_press(key):
    """
    Lecture clavier mannette
        
    """
    global STARTSTOP
    print(f"press : {key}")

    if(key == "i"):
        Init(True)

    elif(key == "d"):
        STARTSTOP = True
        Walk()

    elif(key == "g"):
        Grounded()
    
    elif(key == "c"):
        y = 100
        z= 50
        while(z > 0):
            time.sleep(1)
            z-=1
            print(z)
            LegFL.Transform(0,y,z)
            LegML.Transform(0,y,z)
            LegFR.Transform(0,y,z)
            LegMR.Transform(0,y,z)
            LegBL.Transform(0,y,z)
            LegBR.Transform(0,y,z)

    elif(key == "s"):
        STARTSTOP = False
        #Init()
        sys.exit()

    else:
        sys.exit() 


def Walk():
    """
    tests de mouvements (unité mm)
        
    """
    print("commence à marcher")
    y = 70 #écartement des pattes
    x = 50 #longueur de pas

    # position initial au sol
    Grounded() # 0,100,50
    
    # se relever
    MoveSelectedLegs([([1,2,3,4,5,6],0,y,110)])

    time.sleep(1)
    
    #leve les pattes 2 3 6 pose 1 4 5 (déjà posé au départ)
    MoveSelectedLegs([([2,3,6],0,y,50),([1,4,5],0,y,110)])

    i = 0
    while(i < 3):

        #avance les pattes 2 3 6 et recule 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,50),([1,4,5],-x,y,110)])

        #pose les pattes 2 3 6 et leve 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,110),([1,4,5],-x,y,50)])

        #recule les pattes 2 3 6 et avance 1 4 5
        MoveSelectedLegs([([2,3,6],-x,y,110),([1,4,5],x,y,50)])

        # pose les pattes 1 4 5 et leve 2 3 6
        MoveSelectedLegs([([1,4,5],x,y,110),([2,3,6],-x,y,50)])

        i+=1

    
    print("fini de marcher")


def Grounded():
    """
    initialisation de la position des pattes (ventre au sol + pattes au sol)
        
    """
    MoveSelectedLegs([([1,2,3,4,5,6],0,70,50)])

def StopMoving():
    """
    revenir à une position initial debout
        
    """
    lst = [([1,2,3,4,5,6],0,70,110)]
    MoveSelectedLegs(lst)    

def MoveSelectedLegs(lst):
    """
    Bouge l'ensemble des pattes sélectionnées à une coordonnée x , y , z

     front
     1   2
      \ / 
    3 -O- 4
      / \ 
     5   6
     back

    """
    threads = []
    
    for numbers,x,y,z in lst :
        if(numbers.count(1) > 0):
            t = threading.Thread(target=LegFL.Proceed, args=(x,y,z))
            threads.append(t)
        if(numbers.count(2) > 0):
            t = threading.Thread(target=LegFR.Proceed, args=(x,y,z))
            threads.append(t)
        if(numbers.count(3) > 0):
            t = threading.Thread(target=LegML.Proceed, args=(x,y,z))
            threads.append(t)
        if(numbers.count(4) > 0):
            t = threading.Thread(target=LegMR.Proceed, args=(x,y,z))
            threads.append(t)
        if(numbers.count(5) > 0):
            t = threading.Thread(target=LegBL.Proceed, args=(x,y,z))
            threads.append(t)
        if(numbers.count(6) > 0):
            t = threading.Thread(target=LegBR.Proceed, args=(x,y,z))
            threads.append(t)

    # Start each thread
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def Start():
    """
    Entrée principal du script
        
    """
    try:
        print("Hexapod ON")
        Init(False)
        time.sleep(1)
        Grounded()
        listen_keyboard(on_press=On_key_press)
    except KeyboardInterrupt:
        Init(True)
    finally:
        print("Hexapod OFF")
        Init(True)
        # quitteur le programme
        sys.exit() 


def Init(isGroundedBefore):
    """
    initialisation de la position des pattes (position de transport)
        
    """
    if(isGroundedBefore is True):
        Grounded()

    LegFL.SetAngles(90,0,10)
    LegML.SetAngles(90,0,10)
    LegBL.SetAngles(90,0,10)
    LegFR.SetAngles(90,0,10)
    LegMR.SetAngles(90,0,10)
    LegBR.SetAngles(90,0,10)


def Inverse_kinematics(pos):
    """
    transforme une coordonnée x,y,z en 3 angles (coxa,femur,tibia) via calcul de cynématique inverse

    """
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
        Lt=sqrt((L - coxaLenght)**2 + z**2)
        gamma = atan2((L - coxaLenght), z)

        valBeta = (femurLenght**2 + Lt**2 - tibiaLenght**2) / (2*femurLenght*Lt)
        #beta = acos((femurLenght**2 + Lt**2 - tibiaLenght**2) / (2*femurLenght*Lt))
        if(valBeta < -1):
            valBeta = -1
        elif(valBeta > 1):
            valBeta = 1

        beta = acos(valBeta)
        
        valAlpha = (femurLenght**2 + tibiaLenght**2 - Lt**2) / (2*femurLenght*tibiaLenght)
        #alpha = acos((femurLenght**2 + tibiaLenght**2 - Lt**2) / (2*femurLenght*tibiaLenght))
        if(valAlpha < -1):
            valAlpha = -1
        elif(valAlpha > 1):
            valAlpha = 1
        alpha = acos(valAlpha)

        # tibia angle + adjustment:
        theta1 = (degrees(alpha))

        # femur angle + adjustment:
        theta2 = 200 - (degrees(gamma) + degrees(beta)) #200 - (degr...)

        # coxa Base angle + adjustment::
        theta_base = 90-(degrees(atan2(x, y)))
        '''
            obtient des 180,1 ou -0,1 ...
        #return round(theta_base,1), round(theta2,1), round(theta1,1) 
        '''
        return math.trunc(theta_base), math.trunc(theta2), math.trunc(theta1)

    except:
        print("!!!!!!!!!!!!!!  IK : échec de calcules   !!!!!!!!!!!!!!!!!!")
        Init(True)

'''
def adjustServo():
    """
    Permet le reglage de l'amplitude des servo-moteurs
    faire des tests en modifiant la fréquence du Adafruit PCA9685, voir ServoKit => reference_clock_speed

    """
    time.sleep(2)
    Right.servo[10].angle = 0
    time.sleep(2)
    Right.servo[10].angle = 180
    time.sleep(2)
''' 

'''
    limites de coordonnées
    x =  entre -150 et 150 théorique, entre -80 à 80 pour ne pas s'entrechoquer les pattes en marchant
    y = entre 60 et 200
    z = 50 # 50 entre 150 et 30 avec y = 150
'''

if __name__ == "__main__":
    Start()
