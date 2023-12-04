#!/usr/bin/python
import os
import time
import cv2
import cvzone
import json
import requests
from threading import Thread
from cvzone.ClassificationModule import Classifier
 
 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
classifier = Classifier('./Model/keras_model.h5', '../Resources/Model/labels.txt')
imgArrow = cv2.imread('../Resources/arrow.png', cv2.IMREAD_UNCHANGED)
classIDBin = 0

# Import all the waste images
imgBinsList = []
pathFolderBins = "../Resources/Bins"
pathList = os.listdir(pathFolderBins)
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))
 
# 5 = Plastic bottle
# 1 = General waste
# 2 = Tin can
# 3 = Cup
# 4 = Background
 
classDic = {0: None,
            1: 5,
            2: 1,
            3: 2,
            4: 3,
            5: 4
            }
 
class PrintA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
 
    def run(self):      
        while self.running:
            _, img = cap.read()
            imgResize = cv2.resize(img, (454, 340))
 
            imgBackground = cv2.imread('../Resources/background.png')
 
            prediction = classifier.getPrediction(img)
 
            classID = prediction[1]
 
            imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classID], (895, 200))
 
            imgBackground[148:148 + 340, 159:159 + 454] = imgResize
            # Displays
            # cv2.imshow("Image", img)

            cv2.imshow("SPT Recycle Bank", imgBackground)
            cv2.waitKey(1)
 
            


 
    def stop(self):
        self.running = False
 
class PrintB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
 
    def run(self):
        while self.running:
            _, img = cap.read()
            prediction = classifier.getPrediction(img)
            classID = prediction[1]
            print("ClassID:", classID)  # Print classID for debugging
            if classID != 0:
                mat_data_list = classID.tolist()
                data = {
                    'data': mat_data_list,
                }
                # Send data to the server
                try:
                    response = requests.post("http://172.16.123.187:5000/update_endpoint", data=data)
                    print("Server response:", response.text)
                except Exception as e:
                    print("Error sending data to the server:", str(e))
 
                # Sleep for 5 seconds before sending the next request
                time.sleep(1)
 
            classIDBin = classDic.get(classID, None)  # Update classIDBin based on classDic
 
    def stop(self):
        self.running = False


a = PrintA()
b = PrintB()
 
a.start()
b.start()