import time
import math
import machine as m
import os
import sys
import _thread


capteur_pin35 = m.Pin(35, m.Pin.IN, m.Pin.PULL_UP)
capteur_pin34 = m.Pin(34, m.Pin.IN, m.Pin.PULL_UP)

def detecter_capteurX():
    if capteur_pin35.value() == 0:
        return True
    else:
        return False
def detecter_capteurY():
    if capteur_pin34.value() == 0:
        return True
    else:
        return False

class MyCNC :
    def __init__(self):
        #Position of component classes
        # ["CAPACITOR", "LED", "RESISTOR", "TRANSISTOR"] --> [0,1,2,3]
        self.POSITION_CAPACITOR_BOX = (100, 340)
        self.POSITION_LED_BOX = (200, 340)
        self.POSITION_RESISTOR_BOX = (300, 340)
        self.POSITION_TRANSISTOR_BOX = (400, 340)
        
        # Position of pincers at shooting picture time
        self.POSITION_INIT = (0, 320)

        #Moteur X
        self.dir_pin_x = m.Pin(27, m.Pin.OUT)
        self.step_pin_x = m.Pin(13, m.Pin.OUT)
        self.step_pin_x.off() 
        #enable_pin1 =
        
        #Moteur Y = Y_Left
        self.dir_pin_yl = m.Pin(26, m.Pin.OUT)
        self.step_pin_yl = m.Pin(12, m.Pin.OUT)
        self.step_pin_yl.off()
        #enable_pin2 =
        
        #Moteur Z = Y_Right
        self.dir_pin_yr = m.Pin(25, m.Pin.OUT)
        self.step_pin_yr = m.Pin(14, m.Pin.OUT)
        self.step_pin_yr.off()
        #enable_pin3 =
        
        #Time of delay
        self.DELAY_X = 0.001
        self.DELAY_Y = 0.001
        
        #Current position
        self.current_pos_x = 0
        self.current_pos_y = 0
        
        #Coversion from mm to POSITION_LED_BOXstep
        self.ONE_MM_TO_STEP_X = 5
        self.ONE_MM_TO_STEP_Y = 5
        
    def move_step_x(self, pos_step_x, clockwise=False):
        if clockwise:
            self.dir_pin_x.on()
        else :
            self.dir_pin_x.off()
            
        for i in range(pos_step_x):
            self.step_pin_x.on()
            time.sleep(self.DELAY_X)
            self.step_pin_x.off()
            time.sleep(self.DELAY_X)


    def move_step_y(self, pos_step_y, clockwise_right_Motor=False):
        if clockwise_right_Motor:
            self.dir_pin_yr.on()
            self.dir_pin_yl.off()
        else :
            self.dir_pin_yr.off()
            self.dir_pin_yl.on()
            
        for i in range(pos_step_y):
            self.step_pin_yl.on()
            self.step_pin_yr.on()
            time.sleep(self.DELAY_Y)
            self.step_pin_yl.off()
            self.step_pin_yr.off()
            time.sleep(self.DELAY_Y)

    
    def goto_mm(self, pos_mm_x = 0, pos_mm_y = 0):
        
        step_x = math.ceil((pos_mm_x - self.current_pos_x) * self.ONE_MM_TO_STEP_X)
        step_y = math.ceil((pos_mm_y - self.current_pos_y) * self.ONE_MM_TO_STEP_X)
        # print(step_x, "    ////   ", step_y)
        if step_x < 0 :
            self.move_step_x(-1*step_x, True)
        else:
            self.move_step_x(step_x, False)
        
        if step_y < 0 :
            self.move_step_y(-1*step_y, True)
        else:
            self.move_step_y(step_y, False)
        
        self.current_pos_x = pos_mm_x
        self.current_pos_y = pos_mm_y
    
    def get_position(self, class_number):
        if class_number == 0 :
            return self.POSITION_CAPACITOR_BOX
        elif class_number == 1 :
            return self.POSITION_LED_BOX
        elif class_number == 2 :
            return self.POSITION_RESISTOR_BOX
        elif class_number == 3 :
            return self.POSITION_TRANSISTOR_BOX
        
    def goto_box_position(self, class_number):
        BOX = ["CAPACITOR", "LED", "RESISTOR", "TRANSISTOR"]
        print("Déplacement à la boite : ", BOX[class_number])
        x_box, y_box = self.get_position(class_number)
        self.goto_mm(x_box, y_box)
        
    def autohome(self):
        while True :
            x_capteur = detecter_capteurX()
            y_capteur = detecter_capteurY()
            
            if x_capteur and y_capteur:
                self.current_pos_x = 0
                self.current_pos_y = 0
                break
            if not x_capteur :
                self.move_step_x(2,True)
            if not y_capteur :
                self.move_step_y(2,True)
            

        
# A4 sheet dimension = 297 x 210
#Controling stepper motor of a CNC.

cnc = MyCNC()
