from math import acos,atan2,sqrt,degrees,pi
import time

cSpeed = 0.009#0.003 #vitesse de mouvement d'une patte
cCoxaLenght = 45 #longueur coxa
cFemurLenght = 80 #longueur femur
cTibiaLenght = 140 #longueur tibia
cFemurMountAngle = 43 #angle d'installation du servo-moteur gérant le femur
cTibiaMountAngle = 4 #angle d'installation du servo-moteur gérant le tibia

class Leg:
    """
    définition d'une patte
        
    """
    def __init__(self,id,coxa,femur,tibia):
        """
        id => identifiant de la patte

        front
        1   2
         \ / 
       3 -O- 4
         / \ 
        5   6
        back

        coxa , femur , tibia => adresse des servos
        
        """
        self.Id = id
        # patte gauche droite
        if(id == 1 or id == 3 or id == 5):
            self.Invert = True
        else:
            self.Invert = False
        # patte avant milieu arrière
        if(id == 1 or id == 2 ):
            self.AjustCoorDir = 1
        elif(id == 3 or id == 4 ):
            self.AjustCoorDir = 0
        else:
            self.AjustCoorDir = -1
        self.Coxa = coxa
        self.Femur = femur
        self.Tibia = tibia
        self.X = 0
        self.Y = 110
        self.Z = 0

        
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
        # patch de sécurité femur
        if(fAngle > 180):
            fAngle = 180
        elif(fAngle < 0):
            fAngle = 0
        # patch de sécurité tibia
        if(tAngle > 180):
            tAngle = 180
        elif(tAngle < 0):
            tAngle = 0
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
            ajustCoxa += 45
        elif(self.AjustCoorDir == -1):
            ajustCoxa -= 45
        angles = self.Inverse_kinematics([x,y,z])
        self.SetAngles(angles[0] + ajustCoxa, angles[1], angles[2])

    def Proceed(self,x,y,z):
        """
        déplacement progressif vers une coordonnée x,y,z

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
            time.sleep(cSpeed) #vitesse de mouvement de la patte
            self.Transform(self.X,self.Y,self.Z)
        
    @staticmethod
    def Inverse_kinematics(pos):
        """
        transforme une coordonnée x,y,z en 3 angles (coxa,femur,tibia) via calcul de cynématique inverse

        """
        x, y, z = pos[0],pos[1],pos[2]
        
        # Avoid zero-division
        y += 0.00000001
        z += 0.00000001
        x += 0.00000001

        try:
            if(sqrt(x**2 + y**2 + z**2) > cFemurLenght + cTibiaLenght):
                print("!!! Coordonnées Inatteignable !!!")
        
            d = sqrt(x **2 + y**2)
            r = d - cCoxaLenght
            c = sqrt(z**2 + r**2)
        
            # calcule des angles en degrés
            theta1 = atan2(y, x) * 180.0 / pi
            theta2 = 180 - ( atan2(r,-z) * 180.0 / pi + acos((cFemurLenght**2 + c**2 - cTibiaLenght**2) / (2 * cFemurLenght * c)) * 180.0 / pi ) + cFemurMountAngle 
            theta3 = (acos((cFemurLenght**2 + cTibiaLenght**2 - c**2) / (2 * cFemurLenght * cTibiaLenght)) * 180.0 / pi) - cTibiaMountAngle
            
            if __debug__:
                print(f"x = {x:.2f} , y = {y:.2f} , z = {z:.2f}")
                print(f"coxa = {theta1} , femur = {theta2} , tibia = {theta3}")

            return (theta1,theta2,theta3)
        
        except:
            print("!!!!!!!!!!!!!!  Inverse_kinematics : échec de calcules   !!!!!!!!!!!!!!!!!!")
            # retourne la position de patte initial
            return 90,0,10
        
if __name__ == "__main__":
     print("!!!!!!!!!!!!!!  hexapodLeg.py n'est pas supposé être le script de démarage   !!!!!!!!!!!!!!!!!!")