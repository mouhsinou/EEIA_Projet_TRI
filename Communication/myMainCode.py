# import libraries
import socket
import time
import torch
import numpy as np
import pandas as pd
import os
from PIL import Image
import socket
import time
from myFunctionsCode import snap_and_get_picture, get_only_components_zone

model_home = "C:\\Users\\EEIA\\Desktop\\TRI AUTOMATIQUE\\yolov5-master\\"
IMG_BASE = "C:\\Users\\EEIA\\Desktop\\TRI AUTOMATIQUE\\yolov5-master\\LES IMAGES\\"

#Load Model
print("Loading model ... ")
modelV5n = torch.hub.load('.', 'custom', os.path.join(model_home, 'New_Model_s_Epochs_50.pt'), source='local')  
print("modelV5n OK")

#Init connection to ESP
host = '192.168.137.141'
port = 5000
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Init CNC position
while True:
    try :
        print("Tentative de connextion à ESP32 en cours ... ")
        connection.connect((host, port))
       
        if connection.recv(1024).decode() == "READY ==>" :
            print("Connection établie")
            message = "INIT"
            connection.send(message.encode())
            time.sleep(7)
            break
    except OSError:
        print("Une opération a été tentée sur un hôte impossible à atteindre")

#Load Image and make inference
snap_and_get_picture()

detectionList = np.array([])
with Image.open(os.path.join(IMG_BASE, 'image.jpg'), mode='r') as img1:
    img1 = get_only_components_zone(np.array(img1))
    img1 = Image.fromarray(img1)
    print("Component Zone OK")
    img1 =  modelV5n(img1)

    #img1.save(save_dir=IMG_BASE, exist_ok=True)
    img1.save(exist_ok=True)

    #See models.common.Detections at line 807 for more detail
    detectionDF = pd.DataFrame((img1).pandas().xyxy[0])
    print(detectionDF)

    #After calculating the mean, we devide by the zoom_multiple and take the round
    x_list = ((detectionDF["xmin"].to_numpy() + detectionDF["xmax"].to_numpy())/2) / 3
    y_list = ((detectionDF["ymin"].to_numpy() + detectionDF["ymax"].to_numpy())/2) / 3
    x_list = x_list.round().astype(int)
    y_list = y_list.round().astype(int)
    class_list = detectionDF["class"].to_numpy()
    conf_list = detectionDF["confidence"].to_numpy()

    x_list = x_list.reshape((1,len(x_list)))[0]
    y_list = y_list.reshape((1,len(y_list)))[0]
    class_list = class_list.reshape((1,len(class_list)))[0]

    detectionList = np.vstack([x_list, y_list, class_list, conf_list]) 

    print(detectionList)
    
# detectionList = [[        207,          58,         256,         48,         273,         110],
#                [        151,          59,          58,         174,         158,         105],
#                 [          0,           1,           3,           0,           1,           2],
#                 [     0.73424,     0.73346,     0.72128,     0.70247,     0.68175,     0.60635]] 

#Place a la defraisseuse numérique
startProcess = True
"""

startProcess = False
while True:
    answer = str.upper(input("Lancer le processus de triage (O/N) : "))
    if answer == 'O':
        startProcess = True
        break
    elif answer == 'N':
        break


if startProcess :
    print("Demarrage du Trie")
    while True:
        if connection.recv(1024).decode() == "READY ==>" :
            print("Initialisation...")
            message = "AUTOHOME"
            connection.send(message.encode())
            time.sleep(2)
            break
    
    x_list = detectionList[0]
    y_list = detectionList[1]
    class_list = detectionList[2]
    class_name = ["CAPACITOR", "LED", "RESISTOR", "TRANSISTOR"]

    message_list = []
    separator = " "
    for pos in range(len(detectionList[0])):
        positionToStr = str(x_list[pos]) + separator + str(y_list[pos]) + separator + str(class_list[pos])
        message_list.append(positionToStr)
    print(message_list)

    notDone = True
    component_position = 0
    while notDone:
        # Réception de données de l'ESP32
        data = connection.recv(1024)
        received_message = data.decode()
        print('Message reçu :', received_message)
        time.sleep(2)

        if received_message == "READY ==>" :
            message = message_list[component_position]
            connection.send(message.encode())
            print('Composant élèctronique n =', component_position + 1, "     Info = " , message)

            if component_position == len(message_list) - 1 :
                notDone = False
            else :
                component_position += 1
        
"""        
