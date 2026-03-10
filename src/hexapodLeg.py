from math import sin,cos,acos,atan,atan2,sqrt,degrees,radians,pi,trunc
import time

cSpeed = 0.003

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

        angles = self.Inverse_kinematics([x,y,z])
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
            time.sleep(cSpeed)
            self.Transform(self.X,self.Y,self.Z)
            
    
    @staticmethod
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
            return trunc(theta_base), trunc(theta2), trunc(theta1)

        except:
            print("!!!!!!!!!!!!!!  IK : échec de calcules   !!!!!!!!!!!!!!!!!!")
            # retourne la positrion de patte initial
            return 90,0,10
        