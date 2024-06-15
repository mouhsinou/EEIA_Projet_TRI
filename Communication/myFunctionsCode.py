import cv2
import numpy as np


# Using paramiko in order to snap and get picture from Raspberry Pi
#-------------------------------------------------------------------
import paramiko
import time

def open_connection(RPI_ip='192.168.137.58', username='pi', password='root'):
    paramiko_ssh_client = paramiko.SSHClient()
    paramiko_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko_ssh_client.connect(RPI_ip, username=username, password=password)
    return paramiko_ssh_client

def cmd_on_pi(paramiko_ssh_client, cmd):
    ssh_stdin, ssh_stdout, ssh_stderr = paramiko_ssh_client.exec_command(cmd)
    return ssh_stdin, ssh_stdout, ssh_stderr

def snap_picture():
    ssh_client = open_connection()
    cmd_on_pi(ssh_client, 'raspistill -o image1.jpg')
    #ssh_client.close()

def get_picture():
    ssh_client = open_connection()
    ftp_client = ssh_client.open_sftp()
    ftp_client.get("/home/pi/image1.jpg", "C:\\Users\\EEIA\\Desktop\\TRI AUTOMATIQUE\\yolov5-master\\LES IMAGES\\image.jpg")
    ftp_client.close()
    ssh_client.close()

#Snap and get picture from raspberry pi
def snap_and_get_picture():
    snap_picture()
    print("Capture effectuée !")
    time.sleep(6)
    get_picture()
    print("Téléchargement effectuée")
#-------------------------------------------------------------------



# OpenCV usage
#-------------------------------------------------------------------
widthImg = 297 * 3 
heightImg = 210 * 3

def empty(a):
    pass

def getThreshold():
    threshold1 = cv2.getTrackbarPos("Seuil_1", "Parametre")
    threshold2 = cv2.getTrackbarPos("Seuil_2", "Parametre")
    return threshold1, threshold2

def preProcessing(img):     #OK
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
    threshold1, threshold2 = getThreshold()
    imgCanny = cv2.Canny(imgBlur,threshold1,threshold2)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=1)
    imgProcessed = cv2.erode(imgDial, kernel, iterations=1)
    return imgProcessed

def getContours(imgProcessed,imgOriginal):
    imgCopie = imgOriginal.copy()
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(imgProcessed,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000 :
            #print("area : ", area)
            #cv2.drawContours(img, cnt, -1, (0,0,255), 2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            #print(len(approx))
            if area > maxArea and len(approx) == 4 :
                biggest = approx
                maxArea = area
    cv2.drawContours(imgCopie, biggest, -1, (0,0,255), 5)

    # print("biggest = ", biggest)
    return biggest, imgCopie 

def reorder(points):
    if points.size != 0 :
        points = points.reshape((4,2))
        reordoredPoints = np.zeros((4,1,2), np.int32)
        add = points.sum(1)

        reordoredPoints[0] = points[np.argmin(add)]
        reordoredPoints[3] = points[np.argmax(add)]
        diff = np.diff(points, axis=1)
        reordoredPoints[1] = points[np.argmin(diff)]
        reordoredPoints[2] = points[np.argmax(diff)]
        return reordoredPoints
    else :
        print("Can't process because size of arg is 0")
        return -1

def getWarp(biggest,imgOriginal):
    if biggest.size != 0:
        biggest = reorder(biggest)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0],[widthImg, 0],[0, heightImg],[widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOutput = cv2.warpPerspective(imgOriginal, matrix, (widthImg, heightImg))
        return imgOutput
    else :
        print("Can't process because size of arg is 0")
        return -1

def trackbar_windows():
    win = cv2.namedWindow("Parametre")
    cv2.resizeWindow("Parametre", 640, 240)
    cv2.createTrackbar("Seuil_1", "Parametre",220,255,empty)
    cv2.createTrackbar("Seuil_2", "Parametre",98,55,empty)
    return win

def get_only_components_zone(img):
    trackbar_windows()
    
    
    img = cv2.resize(img,(widthImg,heightImg))
    imgCopie = img.copy()

    imgProcessed = preProcessing(img)
    biggestRectPoint, _ = getContours(imgProcessed,imgCopie)
    imgWarped = getWarp(biggestRectPoint,imgCopie)
    # cv2.destroyWindow(win)

    if isinstance(imgWarped, int) :
        return img
    else :
        return imgWarped


def test_function_relative_to_opencv(img):
    trackbar_windows()

    img = cv2.resize(img,(widthImg,heightImg))
    imgCopie = img.copy()

    while True:
        
        imgProcessed = preProcessing(img)
        biggestRectPoint, imgWithPoint = getContours(imgProcessed,imgCopie)
        imgWarped = getWarp(biggestRectPoint,imgCopie)
        
        #cv2.imshow("result", imgProcessed)
        #cv2.imshow("result", imgWithPoint)
        cv2.imshow("result", imgWarped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
#-------------------------------------------------------------------
#snap_and_get_picture()
#img = cv2.imread("C:\\Users\\EEIA\\Desktop\\TRI AUTOMATIQUE\\yolov5-master\\LES IMAGES\\image.jpg")
#test_function_relative_to_opencv(img)


