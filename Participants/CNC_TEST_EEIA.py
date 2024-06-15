import time
import math
import machine as m
import os
import sys
import _thread
import main

from cnc import MyCNC
from DCMotor import DCMotor
from Servo_Motor import Servo

    
cnc = MyCNC()

"""
#HOME
cnc.autohome()
cnc.goto_mm(0,320)# Prise de photo
time.sleep(4)
cnc.autohome()
time.sleep(2)

cnc.goto_mm(50,50) # Fonction de départ 0
time.sleep(4)
cnc.get_position(0)
time.sleep(2)
main.prise()
time.sleep(2)
cnc.goto_box_position(0)
main.pince_ouvert()
time.sleep(2)
main.pince_fermer()
time.sleep(4)

cnc.goto_mm(100,100) # Fonction de départ 0
time.sleep(4)
cnc.get_position(1)
time.sleep(2)
main.prise()
time.sleep(2)
cnc.goto_box_position(1)
main.pince_ouvert()
time.sleep(2)
main.pince_fermer()
time.sleep(4)

cnc.goto_mm(200,200) # Fonction de départ 0
time.sleep(4)
cnc.get_position(2)
time.sleep(2)
main.prise()
time.sleep(2)
cnc.goto_box_position(2)
main.pince_ouvert()
time.sleep(2)
main.pince_fermer()
time.sleep(4)


cnc.goto_mm(250,250) # Fonction de départ 0
time.sleep(4)
cnc.get_position(3)
time.sleep(2)
main.prise()
time.sleep(2)
cnc.goto_box_position(3)
main.pince_ouvert()
time.sleep(2)
main.pince_fermer()
time.sleep(4)

"""
cnc.autohome()