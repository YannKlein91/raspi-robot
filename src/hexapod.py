from adafruit_servokit import ServoKit # gestion servo-moteurs
import time # temps
from sshkeyboard import listen_keyboard # clavier
import sys # system
from hexapodLeg import Leg # definition des pattes
from evdev import InputDevice, ecodes, evtest # manette xbox
import threading # threading
import os # system linux

'''
    limites + tests de coordonnées (unité mm): https://www.desmos.com/calculator/2uzkupqa2t?lang=fr
    x =  entre -150 et 150 théorique, entre -80 à 80 pour ne pas s'entrechoquer les pattes en marchant
    y = entre 110 et 250
    z = entre 200 et -200
'''

# --------------- constantes + variables globales --------------- #

Right = ServoKit(channels=16 , address=0x40)
Left = ServoKit(channels=16 , address=0x41, reference_clock_speed=35000000) #valeur d'origine => reference_clock_speed=25000000 

cLenghtX = 30 # longueur d'un pas
cEcartY = 150 # écratement des pattes

STARTSTOP = False
INVERTED = False

# --------------- Liste des 6 pattes --------------- #

LegFL = Leg(1,Left.servo[8],Left.servo[9],Left.servo[10])
LegML = Leg(3,Left.servo[4],Left.servo[5],Left.servo[6])
LegBL = Leg(5,Left.servo[0],Left.servo[1],Left.servo[2])

LegFR = Leg(2,Right.servo[8],Right.servo[9],Right.servo[10])
LegMR = Leg(4,Right.servo[4],Right.servo[5],Right.servo[6])
LegBR = Leg(6,Right.servo[0],Right.servo[1],Right.servo[2]) 


def Controller():
    '''
    gestion de la manette Xbox

    '''
    #connexion à la manette
    file_path = '/dev/input/event5'
    while (os.path.exists(file_path) == False):
        print('manette non connectée')
        time.sleep(5)
    dev = InputDevice('/dev/input/event5')
    print('manette connectée')

    #evtest.main() # test lecture de la manette
    global STARTSTOP
    global INVERTED

    tWalk = threading.Thread(target=Walk, args=())
    tSwim = threading.Thread(target=Swim, args=())
    tCrab = threading.Thread(target=CrabWalk, args=())
    
    #lecture des touches
    for event in dev.read_loop():
        #joystick gauche
        if event.code == ecodes.ABS_Y:   
            #joystick au milieu
            if(event.value > 30000 and event.value < 40000): 
               joystickG = 4
        #boutons standards
        elif(event.value != 0):
            # A
            if event.code == ecodes.BTN_A: 
                if(tWalk.is_alive() == False):
                    STARTSTOP = True
                    INVERTED = False
                    tWalk.start()
            # X
            if event.code == ecodes.BTN_X: 
                if(tWalk.is_alive() == False):
                    STARTSTOP = True
                    INVERTED = True
                    tWalk.start()
            # B
            if event.code == ecodes.BTN_B: 
                STARTSTOP = False
                if(tWalk.is_alive() == True):
                    tWalk.join()
                    tWalk = threading.Thread(target=Walk, args=())
                if(tSwim.is_alive() == True):
                    tSwim.join()
                    tSwim = threading.Thread(target=Swim, args=())
                if(tCrab.is_alive() == True):
                    tCrab.join()
                    tCrab = threading.Thread(target=CrabWalk, args=())
            # Y
            if event.code == ecodes.BTN_Y: 
                if(tSwim.is_alive() == False):
                    STARTSTOP = True
                    INVERTED = False
                    tSwim.start()            
            # START
            if event.code == ecodes.BTN_START:
                Init(False)
                sys.exit()
            # SELECT
            if event.code == ecodes.BTN_SELECT:
                select = 1
            # croix haut / bas
            if event.code == ecodes.ABS_HAT0Y:
                if(event.value == 1):
                    Grounded(False)
                else:
                    Grounded(True)
            # croix gauche / droite
            if event.code == ecodes.ABS_HAT0X:
                if(event.value == 1):
                    if(tCrab.is_alive() == False):
                        STARTSTOP = True
                        INVERTED = False
                        tCrab.start()
                else:
                    gauche=-1
    
def Walk():
    """
    marche avant / arrère 
        
    """
    print("commence à marcher")
    global STARTSTOP
    global INVERTED
    y = cEcartY #écartement des pattes
    x = cLenghtX #longueur de pas
    if(INVERTED == True):
        x = -x
    zp = -100
    zl = -60
    #leve les pattes 2 3 6 pose 1 4 5 (déjà posé au départ)
    MoveSelectedLegs([([2,3,6],0,y,-60),([1,4,5],0,y,zp)])
    while STARTSTOP == True:
        #avance les pattes 2 3 6 et recule 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,zl),([1,4,5],-x,y,zp)])
        #pose les pattes 2 3 6 
        MoveSelectedLegs([([2,3,6],x,y,zp)])
        #leve 1 4 5
        MoveSelectedLegs([([1,4,5],-x,y,zl)])
        #recule les pattes 2 3 6 et avance 1 4 5
        MoveSelectedLegs([([2,3,6],-x,y,zp),([1,4,5],x,y,zl)])
        #pose les pattes 1 4 5
        MoveSelectedLegs([([1,4,5],x,y,zp)])
        #leve 2 3 6
        MoveSelectedLegs([([2,3,6],-x,y,zl)])
    Grounded(True)
    print("fini de marcher")

def Swim():
    '''
    nage la brasse

    '''
    print("commence à nager")
    global STARTSTOP
    global INVERTED
    y = cEcartY #écartement des pattes
    x = cLenghtX #longueur de pas
    while STARTSTOP == True:
        #avance les pattes 2 3 6 et recule 1 4 5
        MoveSelectedLegs([([2,3,6],x,y,0),([1,4,5],x,y,0)])
        #recule les pattes 2 3 6 et avance 1 4 5
        MoveSelectedLegs([([2,3,6],-x,y,0),([1,4,5],-x,y,0)])
    print("fini de nager")

def CrabWalk():
    '''
    marche latérale gauche / droite

    '''
    print("commence à marcher en crab")
    global STARTSTOP
    global INVERTED
    yMin = 60 
    yMax = 100
    x = 0 #longueur de pas
    #if(INVERTED == True):
    #    y = -y
    #leve les pattes 2 3 6 pose 1 4 5 (déjà posé au départ)
    MoveSelectedLegs([([2,3,6],0,cEcartY,50),([1,4,5],0,cEcartY,110)])
    while STARTSTOP == True:
        #avance les pattes 2 3 6 et recule 1 4 5
        MoveSelectedLegs([([2,6],x,yMax,50),(([3],x,yMin,50)),([1,5],x,yMin,110),([4],x,yMax,110)])
        #pose les pattes 2 3 6 et leve 1 4 5
        MoveSelectedLegs([([2,6],x,yMax,110),(([3],x,yMin,110)),([1,5],x,yMin,50),([4],x,yMax,50)])
        #recule les pattes 2 3 6 et avance 1 4 5
        MoveSelectedLegs([([2,6],x,yMin,110),(([3],x,yMax,110)),([1,5],x,yMax,50),([4],x,yMin,50)])
        # pose les pattes 1 4 5 et leve 2 3 6
        MoveSelectedLegs([([2,6],x,yMax,50),(([3],x,yMin,50)),([1,5],x,yMin,110),([4],x,yMax,110)])
    Grounded(True)
    print("fini de marcher en crab")



def Grounded(isUp):
    """
    initialisation de la position des pattes (ventre au sol + pattes au sol)
        
    """
    # se relever
    if(isUp == True):
        MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,-100)])
    else:
        MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,0)])


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

def Init(isGroundedBefore):
    """
    initialisation de la position des pattes (position de transport)
        
    """
    if(isGroundedBefore is True):
        Grounded(False)
    LegFL.SetAngles(90,0,00)
    LegML.SetAngles(90,0,00)
    LegBL.SetAngles(90,0,00)
    LegFR.SetAngles(90,0,00)
    LegMR.SetAngles(90,0,00)
    LegBR.SetAngles(90,0,00)


def On_key_press(key):
    """
    Lecture clavier
        
    """
    print(f"press : {key}")

    if(key == "i"):
        Init(True)
    elif(key == "s"):
        Init()
        sys.exit()
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

def Start():
    """
    Entrée principal du script
        
    """
    try:
        print("Hexapod ON")
        Init(True)
        Grounded(False)        
        Controller()
        #listen_keyboard(on_press=On_key_press)
    except KeyboardInterrupt:
        Init(False)
    finally:
        print("Hexapod OFF")
        Init(True)
        # quitteur le programme
        sys.exit() 

if __name__ == "__main__":
    Start()
