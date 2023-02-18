class VirtualBox():
    # Y-axis X-axis Z-axis
    current_pos = [0, 0, 0, 0]
    MAX_POS = [0, 0, 0]
    # [[y,-y],[x,-x],[z,-z]]
    valid_move = [[False, False], [False, False], [False, False]]
    last_move = [0, 0, 0, 0]
    online_flag = True

    def __init__(self, maxx, maxy, maxz):
        self.MAX_POS = [maxx, maxy, maxz]
        self.__updateValid()

    def reset(self):
        self.last_move = [0, 0, 0, 0]
        self.current_pos = [0, 0, 0, 0]

    def set_MAX_POS(self, val):
        self.MAX_POS = val

    def getCurrent(self):
        return self.current_pos

    def set_online_flag(self, falg):
        # on or off virtual box
        self.online_flag = falg
        # when it change from False to true check if am i out of box so go back or reset
        if self.online_flag == True:
            # if its out of range max go back
            self.reset()

    def addDegree(self, val):
        # degree must be between 0 and 360  from the north
        self.current_pos[3] = ((val + self.current_pos[3]) % 360)

    def __isValidmoveAt(self, pos, pos2):
        return self.valid_move[pos][pos2]

    def getlastmove(self):
        return self.last_move

    def __updateValid(self):
        for i in range(3):
            if self.current_pos[i] + self.last_move[i] >= self.MAX_POS[i]:
                self.valid_move[i][0] = False
            else:
                self.valid_move[i][0] = True

            if self.current_pos[i] + self.last_move[i] <= - self.MAX_POS[i]:
                self.valid_move[i][1] = False
            else:
                self.valid_move[i][1] = True

    def makeValidMove(self, lr, fb, ud, yv):
        self.last_move = [lr, fb, ud, yv]
        self.__updateValid()

        for i in range(3):
            if self.last_move[i] >= 0 and not self.__isValidmoveAt(i, 0):
                self.last_move[i] = 0
            if self.last_move[i] < 0 and not self.__isValidmoveAt(i, 1):
                self.last_move[i] = 0

        self.__makeMove(self.last_move)

        return self.last_move

    def __makeMove(self, move):
        self.addDegree(move[3])
        for i in range(3):
            self.current_pos[i] += move[i]


if __name__ == '__main__':
    from keyboardcontroler import DroneControler
    box = VirtualBox(50, 50, 50)
    controller = DroneControler(10, 22)
    while True:
        controller.listener.wait(0.3)
        # Drone get command
        """------ start the virtual box after the take off 
        so 0,0,0  will set on air after takeoff not be on the ground """
        [lr, fb, ud, yv] = controller.KeyPressCommand()
        values = [lr, fb, ud, yv]
        print("command :", values)
        values = box.makeValidMove(lr, fb, ud, yv)
        print("sent valid command ", values)
        print("current ", box.getCurrent())
