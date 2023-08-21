import cv2
import pyttsx3
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import  Classifier
import numpy as np
import math
import time


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/PLEASE"
counter = 0



labels = [ "FATHER" , "FOOD" , "I LOVE YOU" , "NO" , "TEN" , "THANK YOU" , "WEDNESDAY" , "WHERE" , "YOUR TRAIN WILL ARRIVE ON PLATFORM NUMBER THREE PLEASE GRAB YOUR LUGGAGE AND GET READY MAKE SURE YOU HAVE YOUR PHYSICAL TICKETS WITH YOU HAVE A GOOD DAY"]

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)

            print(prediction , index, "accuracy : ",prediction[index]*100)

            SpeakText(labels[index])

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(img)



        cv2.putText(imgOutput," {}%, {} ".format(round(prediction[index]*100),labels[index]), (x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)


        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)