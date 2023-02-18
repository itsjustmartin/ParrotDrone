import time
from KB_Get_Module import KeyBoard
from time import sleep
import cv2
import numpy as np


class DroneControler():
    listener = KeyBoard()
    speed = 0
    angularspeed = 0  # 22.5 so when it doubles will be 45-degree  but i cant use float

    def __init__(self, speed=10, angularspeed=22):
        self.speed = speed
        self.angularspeed = angularspeed
        self.listener.init()

    def setSpeed(self, val):
        # Limit the value of speed between 0 and 30
        self.speed = min(max(val, 0), 30)

    def getSpeed(self): return self.speed

    def KeyPressCommand(self):
        lr, fb, ud, yv = 0, 0, 0, 0

        if self.listener.getkeyPressed("o"):
            self.setSpeed(self.getSpeed()+10)
        elif self.listener.getkeyPressed("p"):
            self.setSpeed(self.getSpeed()-10)

        if self.listener.getkeyPressed("u"):
            self.angularspeed += 10
        elif self.listener.getkeyPressed("i"):
            self.angularspeed += -10

        # moving controls
        if self.listener.getkeyPressed("LEFT"):
            lr = -self.speed
        elif self.listener.getkeyPressed("RIGHT"):
            lr = self.speed

        if self.listener.getkeyPressed("UP"):
            fb = self.speed
        elif self.listener.getkeyPressed("DOWN"):
            fb = -self.speed

        if self.listener.getkeyPressed("w"):
            ud = self.speed
        elif self.listener.getkeyPressed("s"):
            ud = -self.speed

        if self.listener.getkeyPressed("a"):
            yv = -self.angularspeed
        elif self.listener.getkeyPressed("d"):
            yv = self.angularspeed

        if self.listener.getkeyPressed("l"):
            # drone land
            pass
        if self.listener.getkeyPressed("t"):
            # drone.takeoff()
            pass

        if self.listener.getkeyPressed("b"):
            # drone.flip_forward()
            pass

        # capture image
        if self.listener.getkeyPressed("c"):
            pass
            # cv2.imwrite(f"Resources/Images/{time.time()}.jpg", img)
           # time.sleep(0.3)  # so il will not take alot of pics
        if self.listener.getkeyPressed("ESCAPE"):
            self.listener.exit()
            # drone land

        return [lr, fb, ud, yv]

    def keyReleaseCommand(self):
        # on release reset state speed
        pass


if __name__ == '__main__':

    # print("power level : ", drone.get_battery(), " % 'controler' ")
    # # drone.takeoff()
    contoler = DroneControler(10, 22)
    while True:
        # moves
        contoler.listener.wait()
        values = contoler.KeyPressCommand()
        print(contoler.speed, contoler.angularspeed)
        if (values[0] == 0 and values[1] == 0 and values[2] == 0 and values[3] == 0):
            print("---no command---")
        else:
            print(values)
        # camera
        # img = drone.get_frame_read().frame
        # img = cv2.resize(img, (360, 240))
        # cv2.imshow("image", img)
        # sleep(0.05)
