from adafruit_servokit import ServoKit
from hexapodLeg import Leg
import time

Right = ServoKit(channels=16 , address=0x40) 
LegMR = Leg(4,Right.servo[4],Right.servo[5],Right.servo[6])

def TestMove():
    print("début essaie")
    time.sleep(2)
    LegMR.SetAngles(90,0,10)
    time.sleep(2)

    LegMR.Proceed(0,200,0)

    LegMR.Proceed(150,200,0)

    LegMR.Proceed(-150,200,0)

    LegMR.Proceed(0,200,0)

    LegMR.Proceed(0,110,0)

    time.sleep(2)
    #LegMR.SetAngles(90,0,10)
    
    #x =  entre -150 et 150 théorique, entre -80 à 80 pour ne pas s'entrechoquer les pattes en marchant
    #y = entre 60 et 200
    #z = 50 # 50 entre 150 et 30 avec y = 150
    #while STARTSTOP == True:

        #test x
        #MoveSelectedLegs([([1,2,3,4,5,6],-30,cEcartY,100)])
        #MoveSelectedLegs([([1,2,3,4,5,6],30,cEcartY,100)])
        #MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,100)])

        #test y
        #LegMR.SetAngles(90,0,0)
        #time.sleep(10)
        #MoveSelectedLegs([([4],0,60,0)])
        #time.sleep(1)
        #MoveSelectedLegs([([4],0,200,0)])
        #time.sleep(1)
        #MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,100)])


        #test z
        #MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,30)])
        #MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,150)])
        #MoveSelectedLegs([([1,2,3,4,5,6],0,cEcartY,100)])
        
    print("fin essaie")


if __name__ == "__main__":
    TestMove()
