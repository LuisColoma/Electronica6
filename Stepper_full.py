import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

ControlPin = [7,11,13,15]
ControlPin2 = [31,33,35,37]

for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

for pin in ControlPin2:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

f1 = open('Azimut.txt', 'r')
if f1.mode=='r':
    posf = int(f1.read())
    
f2 = open('Elevacion.txt', 'r')
if f2.mode=='r':
    posf2= int(f2.read())

seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

sek = [ [1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0] ]

seq2 = [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

sek2 = [[1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0] ]

#Modo de paso completo 4 pasos  ---- 4 * 64 = 256 impulsos 
#Modo de medio paso 8 pasos --- 8 * 64 = 512 impulsos
#Reductora 1/64

# 512 = 360°
# impulso = angulo deseado

#impulso = 512 * angulo // 360

if posf != 0:
    print("Calibrando Azimut")
    pos = posf * -1
    posf = posf - posf
    if pos >= 0:
        pos = abs(pos)
        for i in range(pos):
            for paso in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], sek[paso][pin])
                    time.sleep(0.01)
    if pos < 0:
        pos = abs(pos)
        for i in range(pos):
            for paso in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[paso][pin])
                    time.sleep(0.01)   
    file1 = open("Azimut.txt", "w") 
    file1.write(str(posf) + "\n")
    file1.close()
    
if posf2 != 0:
    print("Calibrando Elevación")
    pos2 = posf2 * -1
    posf2 = posf2 - posf2
    if pos2 >= 0:
        pos2 = abs(pos2)
        for i in range(pos2):
            for paso in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin2[pin], sek2[paso][pin])
                    time.sleep(0.01)

    if pos2 < 0:
        pos2 = abs(pos2)
        for i in range(pos2):
            for paso in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin2[pin], seq2[paso][pin])
                    time.sleep(0.01)


    file2 = open("Elevacion.txt", "w") 
    file2.write(str(posf2) + "\n")
    file2.close()

while(1):

    Ask = input("Calculará un angulo? Si o No \n").upper()
    
    if Ask == "SI":
        
        print(posf, "   ",posf2)
        
        Angulo = int(input("Ingrese el angulo de rotación deseado: "))
        Angulo2 = int(input("Ingrese el angulo de elevación deseado: "))
        
        if Angulo2 <= 180 and Angulo2 >= 0:
            pos = int(((512*Angulo)/360))
            pos2 = int(((512*Angulo2)/360))
            
            pos = int((pos*2)*(-1))
            pos2 = int((pos2*(2.5))*(-1))
    #####################################################################################  
            aux = pos - posf
            aux2 = pos2 - posf2
            pos = aux
            pos2 = aux2 
    #####################################################################################
            if pos >= 0:
                pos = abs(pos)
                print("Derecha")
                for i in range(pos):
                    for paso in range(8):
                        for pin in range(4):
                            GPIO.output(ControlPin[pin], sek[paso][pin])
                        time.sleep(0.01)

            if pos < 0:
                pos = abs(pos)
                print("Izquierda")
                for i in range(pos):
                    for paso in range(8):
                        for pin in range(4):
                            GPIO.output(ControlPin[pin], seq[paso][pin])
                        time.sleep(0.01)    
     
    ######################################################################################## 
            if pos2 >= 0:
                pos2 = abs(pos2)
                #print(pos)
                for i in range(pos2):
                    for paso in range(8):
                        for pin in range(4):
                            GPIO.output(ControlPin2[pin], sek2[paso][pin])
                        time.sleep(0.01)

            if pos2 < 0:
                pos2 = abs(pos2)
                #print(pos)
                for i in range(pos2):
                    for paso in range(8):
                        for pin in range(4):
                            GPIO.output(ControlPin2[pin], seq2[paso][pin])
                        time.sleep(0.01)
                        
            posf = aux + posf
            posf2 = aux2 + posf2
            file1 = open("Azimut.txt", "w") 
            file1.write(str(posf) + "\n")
            file1.close()
            file2 = open("Elevacion.txt", "w") 
            file2.write(str(posf2) + "\n")
            file2.close()

        else:
            print ("Angulo de elevacion fuera de rango")

    elif Ask == "NO":
        GPIO.cleanup()
        break
    
    else:
        print ("Dato invalido ingrese Si o No \n")