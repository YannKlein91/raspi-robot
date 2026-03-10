from adafruit_servokit import ServoKit
import time
from sshkeyboard import listen_keyboard # clavier
import sys
from hexapodLeg import Leg
from evdev import InputDevice, ecodes, evtest # manette xbox
import threading
import os

'''
    limites de coordonnées
    x =  entre -150 et 150 théorique, entre -80 à 80 pour ne pas s'entrechoquer les pattes en marchant
    y = entre 60 et 200
    z = 50 # 50 entre 150 et 30 avec y = 150
'''

# --------------- constantes + variables globales --------------- #


Right = ServoKit(channels=16 , address=0x40)
Left = ServoKit(channels=16 , address=0x41, reference_clock_speed=35000000) #original value => reference_clock_speed=25000000 OK

coxaMin = 35
coxaMax = 145

femurMin = 0
femurMax = 90

tibiaMin = 5
tibiaMax = 150

STARTSTOP = False

# --------------- Liste des 6 pattes --------------- #

LegFL = Leg(True,Left.servo[8],Left.servo[9],Left.servo[10],+1)
LegML = Leg(True,Left.servo[4],Left.servo[5],Left.servo[6],0)
LegBL = Leg(True,Left.servo[0],Left.servo[1],Left.servo[2],-1)

LegFR = Leg(False,Right.servo[8],Right.servo[9],Right.servo[10],+1)
LegMR = Leg(False,Right.servo[4],Right.servo[5],Right.servo[6],0)
LegBR = Leg(False,Right.servo[0],Right.servo[1],Right.servo[2],-1) 


def Controller():
    #connexion à la manette
    file_path = '/dev/input/event5'
    while (os.path.exists(file_path) == False):
        print('manette non connectée')
        time.sleep(5)
    dev = InputDevice('/dev/input/event5')
    print('manette connectée')

    #evtest.main() # test lecture de la manette

    global STARTSTOP
    #lecture des touches
    for event in dev.read_loop():
        #joystick gauche
        if event.code == ecodes.ABS_Y:   
            #joystick au milieu
            if(event.value > 30000 and event.value < 40000): 
                STARTSTOP = False
            #joystick actionné
            else:  
                STARTSTOP = True
                Walk()
        if event.code == ecodes.BTN_A: 
            STARTSTOP = False
    

def Walk():
    """
    tests de mouvements (unité mm)
        
    """
    print("commence à marcher")
    y = 70 #écartement des pattes
    x = 50 #longueur de pas
    global STARTSTOP
    # position initial au sol
    Grounded() # 0,100,50
    
    # se relever
    MoveSelectedLegs([([1,2,3,4,5,6],0,y,110)])

    time.sleep(1)
    
    #leve les pattes 2 3 6 pose 1 4 5 (déjà posé au départ)
    MoveSelectedLegs([([2,3,6],0,y,50),([1,4,5],0,y,110)])

    while(STARTSTOP == True):

        #avance les pattes 2 3 6 et recule 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,50),([1,4,5],-x,y,110)])

        #pose les pattes 2 3 6 et leve 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,110),([1,4,5],-x,y,50)])

        #recule les pattes 2 3 6 et avance 1 4 5
        MoveSelectedLegs([([2,3,6],-x,y,110),([1,4,5],x,y,50)])

        # pose les pattes 1 4 5 et leve 2 3 6
        MoveSelectedLegs([([1,4,5],x,y,110),([2,3,6],-x,y,50)])


    
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
        Controller()
        #listen_keyboard(on_press=On_key_press)
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


def On_key_press(key):
    """
    Lecture clavier
        
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
        #sys.exit()

    else:
        sys.exit()

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



if __name__ == "__main__":
    Start()
