import cv2
from time import sleep
import numpy as np


class FaceTracker ():
    # general
    on_flag = True
    drawonframe = True
    width, height = 640, 480  # change it to the best value to apply

    window_w = width
    window_h = height
    # make sure center is integer tuple so //
    center = (width//2, height//2)
    window_area = window_w * window_h

    frame = None
    # findface
    # trackface

    def findface(self, inframe):
        faceCascade = cv2.CascadeClassifier(
            "Resources/haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(inframe, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                             minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        # print(len(faces))

        # it could be many faces in frame so we wil choose the biggest one
        myfacelistcenter = []
        myfacelistarea = []
        myfacelistdistance = []

        gapX, gapY = 0, 0

        for (x, y, w, h) in faces:
            # cv2.rectangle(image, start_point, end_point, color, thickness)
            cv2.rectangle(inframe, (x, y),
                          (x + w, y + h), (255, 0, 0), 5)  # face

            face_centerx = x + (w // 2)
            face_centery = y + (h // 2)

            cv2.circle(inframe, (face_centerx, face_centery), 5,
                       (0, 255, 0), cv2.FILLED)  # face center

            cv2.circle(inframe, self.main_frame_det['center'],
                       5, (255, 255, 0), cv2.FILLED)  # center image point

            # left right , up and dawn
            gapX = face_centerx - self.main_frame_det['center'][0]
            gapY = face_centery - self.main_frame_det['center'][1]
            # back and forward
            face_area = w * h
            # rotation

            myfacelistcenter.append([face_centerx, face_centery])
            myfacelistarea.append(face_area)
            myfacelistdistance.append([gapX, gapY])
        # if drawing on then apply
        if self.drawonframe:
            self.frame = inframe

        # if face found
        if len(myfacelistarea) != 0:
            # choose the big face
            i = myfacelistarea.index(max(myfacelistarea))
            return self.frame, [myfacelistcenter[i], myfacelistarea[i], myfacelistdistance[i]]
        else:
            return self.frame, [[0, 0], 0, [0, 0]]

    def trackface(self, info):

        fpoint = self.center
        # static vars
        # find the best value for it so it will not continusly shake
        TOLERANCE_X, TOLERANCE_Y = 20, 20
        SLOWDOWN_THRESHOLD = 20
        SPEED = 10

        AreaValidRange = [6600, 6800]

        # ---- fetch vars
        gapX, gapY = info[2][0], info[2][1]
        face_area = info[1]
        face_centerx, face_centery = info[0][0], info[0][1]
        face_percent = face_area / self.window_area  # to help with forward upgrade
        print(
            f"""distanceX : {gapX}  distanceY : {gapY}
            \nface_area {face_area}\nface_center ({face_centerx},{face_centery})\n\n""")

        right, forward, up, yaw = 0, 0, 0, 0

        # i need to check i a face is found so it not go to the corner when no face found
        if face_area != 0:
            # left right track
            # face found checked before  so distance zero now mean for sure the x axis is right
            # if object on the left
            if gapX < -TOLERANCE_X:
                # right = distanceX
                right = - SPEED
            elif gapX > TOLERANCE_X:
                # right = distanceX
                right = SPEED

            # up dawn
            # if object is upper
            if gapY < -TOLERANCE_Y:
                # up = - distanceY
                up = SPEED

            elif gapY > TOLERANCE_Y:
                # up = - distanceY
                up = - SPEED

            # back and forward
            # if  in range or nothing detected  ( 0 )  it will not go forward
            if (face_area > AreaValidRange[0] and face_area < AreaValidRange[1]):
                forward = 0
            elif face_area > AreaValidRange[1]:
                # maybe you need to change speed to distance when you get a good value to the range so distance will be right
                forward = -SPEED
            elif face_area < AreaValidRange[0]:
                forward = SPEED

            # rotation track
            # yaw rotation is on the X axis
            # find the good pid value
            pid = 0.3
            yaw = pid * gapX

        up = min(SLOWDOWN_THRESHOLD, max(-SLOWDOWN_THRESHOLD, up))
        right = min(SLOWDOWN_THRESHOLD, max(-SLOWDOWN_THRESHOLD, right))
        forward = min(SLOWDOWN_THRESHOLD, max(-SLOWDOWN_THRESHOLD, forward))
        yaw = int(np.clip(yaw, -30, 30))

        # send command
        print(
            f"\nright :{right}, forward :{forward}, up:{up}, rotate:{yaw}\n")
        # sendcommand(,blocking=False)
        return [right, forward, up, yaw]


if __name__ == '__main__':

    tracker = FaceTracker()
    # cam
    cap = cv2.VideoCapture(0)
    cap.set(3, tracker.window_w)
    cap.set(4, tracker.window_h)
    while True:
        ret, frame = cap.read()
        frame, info = tracker.findface(frame)
        values = tracker.trackface(info)
        cv2.imshow('Video', frame)
        sleep(0.3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
