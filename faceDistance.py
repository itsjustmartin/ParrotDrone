import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cap =  cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

while True :
    _ , img = cap.read()

    img ,faces =detector.findFaceMesh(img)
    if faces :
        myface = faces[0]

        pointleft = myface[145]
        pointright = myface[374]
        cv2.line(img,pointleft,pointright,(0,200,0),3)
        cv2.circle(img,pointleft,5,(255,0,255),cv2.FILLED)
        cv2.circle(img,pointright,5,(255,0,255),cv2.FILLED)

        eyes_width_px , _ = detector.findDistance(pointleft,pointright)
        eyes_width_cm = 6.3
        # real_distance = 50 # cm
        # focal_length = (eyes_width_px * real_distance ) / eyes_width_cm
        # print(focal_length)
        # after founding focal_length we assign it
        focal_length = 840
        real_Distance = (focal_length * eyes_width_cm ) / eyes_width_px 
        print(real_Distance)
        cvzone.putTextRect(img,f'Depth : {int(real_Distance)}cm',(myface[10][0]-100,myface[10][1]-50),scale=2)

        



    cv2.imshow("Image",img)
    cv2.waitKey(1)
