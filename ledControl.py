from gpiozero import LED

Rouge = LED(6)
Jaune = LED(13)
Vert = LED(12)
Bleu = LED(5)

Leds = {}

# B6612FNG
Leds[0.2] = Rouge
Leds[0.3] = Jaune
Leds[0.5] = Vert
Leds[0.7] = Bleu

"""
# L298N
Leds[0.6] = Rouge
Leds[0.7] = Jaune
Leds[0.85] = Vert
Leds[1.0] = Bleu
"""
def MinimalSpeed():
    for key,value in Leds.items():
        return key

# alumer/éteindre une led
def TurnLed(couleur:LED, onOff):
    couleur.value = onOff
    
# indicateur de vitesse, retourne la vitesse à atteindre en allumant/étaignant les leds au fur et à mesure
def SpeedIndicator(upDown):
    #invertedLeds = reversed(Leds.items())
    
    #allumer la prochaine led
    if(upDown == True):
        for key, value in Leds.items():
            led:LED = value
            if(led.value == False):
                led.value = True
                break
    
    #étaindre la prochaine led
    else:
        for key, value in reversed(Leds.items()):
            led:LED = value
            if(led.value == True and led is not Rouge):
                led.value = False
                break
    
    #renvoie de la vitesse sélectionné
    for key, value in reversed(Leds.items()):
            led:LED = value
            if(led.value == True):
                return float(key)

"""
else:
        for key, value in reversed(Leds.items()):
            led:LED = value
            if(led.value == True and led is not Rouge):
                led.value = False
                return float(key)
        return 0.6
"""

""" else:
        for led in reversed(Leds):
             if(led.value == True):
                led.value = False
                return Leds[led]
"""


"""
# indicateur de vitesse, retourne la vitesse à atteindre
def SpeedIndicator(value):
    if(value == True):
        if(Jaune.value == False):
            Jaune.value = True
            return 0.7
        elif(Vert.value == False):
            Vert.value = True
            return 0.85
        elif(Bleu.value == False):
            Bleu.value = True
            return 1
        return 1
    elif(value == False):
        if(Bleu.value == True):
            Bleu.value = False
            return 0.85
        elif(Vert.value == True):
            Vert.value = False
            return 0.7
        elif(Jaune.value == True):
            Jaune.value = False   
            return 0.6
        return 0.6
"""

# éteindre toutes les leds
def LedsOff():
    Rouge.off()
    Jaune.off()
    Vert.off()
    Bleu.off()