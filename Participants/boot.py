# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


import socket
import network
import time
from machine import Pin
from cnc import MyCNC
from main import prise, pince_ouvert, pince_fermer
#Declaration

#led = Pin(2, Pin.OUT)

# Connexion au réseau WiFi
ssid = 'PROJET_IA'
password = '12345678'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('PROJET_IA', '12345678')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# Création du serveur socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5000))
s.listen(10)
print('En attente de connexion...')

cnc = MyCNC()
message = "READY ==>"
while True:
    conn, addr = s.accept()
    print('Client connecté :', addr)
    while True:
        # Envoi d'un message au client
        conn.send(message.encode())
        print('Message envoyé :', message)
        
        # Réception de données du client
        data = conn.recv(1024)
        received_mesage = data.decode()
        
        if not data:
            print('Connexion interrompue')
            break
        
        elif received_mesage == "INIT":
            print("Auto-home et déplacement à l'origine")
            cnc.autohome()
            time.sleep(1)
            print('Déplacement = Hors champs de vision Camera')
            cnc.goto_mm(0,320)
        
        elif received_mesage == "AUTOHOME":
            print("Déplacement à l'origine")
            cnc.autohome()
            
        else :
            component_data = received_mesage.split()
            print(component_data)
            x_mm_component = int(float(component_data[0]))
            y_mm_component = int(float(component_data[1]))
            class_component = int(float(component_data[2]))
            print("Pause de 1 s")
            time.sleep(1)
            
            
            # Mooving to the right position of the component
            print("Deplacement à : ", x_mm_component, "   ", y_mm_component)
            cnc.goto_mm(x_mm_component, y_mm_component)
            
            # Take the component
            # Code de la pince
            prise()
            
            # Moove to the component class position
            cnc.goto_box_position(class_component)
            
            # Throw the component in the box
            # Code de la pince
            pince_ouvert()
            time.sleep(1)
            pince_fermer()
            time.sleep(1)
                
    # Attendre un certain temps avant d'envoyer le prochain message
    time.sleep(1)
    print("En écoute...")
    
conn.close()
