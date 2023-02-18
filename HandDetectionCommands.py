import cv2
from time import sleep
import time

from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math


class HandCommands():
    detector = HandDetector(maxHands=1)
    Classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
    # change this value when adding new data
    folder = "Data/back"
    counter = 0

    def detectHand(self, img):
        offset = 20
        imgSize = 300
        imgOutput = img.copy()
        # hands, img = self.detector.findHands(img)
        hands = self.detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            # making a frame include the hand with the same ratio and centrized
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
            # add try to avoid go bigger than the frame
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
            aspectratio = h/w
            if aspectratio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                wGap = math.ceil((imgSize - wCal)/2)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgWhite[:, wGap:wCal+wGap] = imgResize
                prediction, index = Classifier.getPrediction(
                    imgWhite, draw=False)
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                hGap = math.ceil((imgSize - hCal)/2)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgWhite[hGap:hCal+hGap, :] = imgResize
                prediction, index = Classifier.getPrediction(
                    imgWhite, draw=False)

            cv2.putText(imgOutput, f"{index}", (x, y-20),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                          (x+w+offset, y+h+offset), (255, 0, 255), 4)

            if cv2.waitKey(1) == ord("s"):
                self.counter += 1
                cv2.imwrite(f'{self.folder}/Image_{time.time()}.jpg', imgWhite)
                print(self.counter)

            cv2.imshow("imgCrop", imgCrop)
            cv2.imshow("imgWhite", imgWhite)
            return imgOutput


if __name__ == '__main__':
    # cam
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 360)
    HandCommand = HandCommands()
    while True:
        _, frame = cap.read()
        frame = HandCommand.detectHand(frame)
        cv2.imshow('Video', frame)
        sleep(0.3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
