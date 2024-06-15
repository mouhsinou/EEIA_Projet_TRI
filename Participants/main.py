#----------------import des bibliothèque
from machine import Pin, PWM
import time
from Servo_Motor import Servo
from DCMotor import DCMotor
#---------------------------------------
#motor = DCMotor(5, 33, 23)
#motor.forward(100)

#----------Initialisation du PWM
frequency = 15000       
pin1 = Pin(33, Pin.OUT)    
pin2 = Pin(5, Pin.OUT)  
enable = PWM(Pin(23), frequency)
motor = DCMotor(pin1, pin2, enable, 350, 1023)
#================================

#-----------Initialisation du servo Moteur
servo_hauteur = Servo(18)
servo_angle= Servo(4)
#================================
capteur = Pin(32, Pin.IN)


def mvt_haut_bas(angle_haut, angle_bas,tm = 1):
    servo_hauteur.write_angle(angle_haut)
    time.sleep(tm)
    servo_hauteur.write_angle(angle_bas)
    
def mvt_lateral(angle_right, angle_left, tm = 1):
    servo_angle.write_angle(angle_right)
    time.sleep(tm)
    servo_angle.write_angle(angle_left)
    
def pince_ouvert():
    #motor.forward(100)
    motor.backwards(100)
    print("j'ouvre")
    time.sleep(2)
    motor.stop()
    print("je ferme")
def pince_fermer():
    while True:
        if etat_capteur():
            motor.stop()
            print('capteur fermer')
            break
        else :
            #motor.backwards(100)
            motor.forward(100)
            print('capteur ouvert')
    #time.sleep(1)
    

def etat_capteur():
    if capteur.value() == 0:
        print(0)
        return True
    else :
        print(1)
        return False
    
def prise():
    servo_hauteur.write_angle(150)
    time.sleep(2)
    servo_angle.write_angle(0)
    time.sleep(2)
    servo_angle.write_angle(90)
    time.sleep(2)
    pince_ouvert()
    time.sleep(2)
    servo_hauteur.write_angle(0)
    time.sleep(2)
    pince_fermer()
    time.sleep(2)
    servo_hauteur.write_angle(150)



