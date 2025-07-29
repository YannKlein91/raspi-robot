from gpiozero import LED


rouge = LED(13)
jaune = LED(6)
vert = LED(5)
bleu = LED(12)

def Led(couleur,onOff):
    if(couleur == rouge):
        rouge.value = onOff
    elif(couleur == jaune):
        jaune.value = onOff
    elif(couleur == vert):
        vert.value = onOff
    elif(couleur == bleu):
        bleu.value = onOff

def SpeedIndicator(value):
    if(value == True):
        if(jaune.value == False):
            jaune.value = True
        elif(vert.value == False):
            vert.value = True
        elif(bleu.value == False):
            bleu.value = True
    elif(value == False):
        if(bleu.value == True):
            bleu.value = False
        elif(vert.value == True):
            vert.value = False
        elif(jaune.value == True):
            jaune.value = False   

def LedsOff():
    rouge.off()
    jaune.off()
    vert.off()
    bleu.off()