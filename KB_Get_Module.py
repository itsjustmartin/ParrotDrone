import pygame
import time

class KeyBoard:
    def init(self):
        pygame.init()
        win = pygame.display.set_mode((360, 240))
    # get keypress

    def getkeyPressed(self, keyName):
        ans = False
        for event in pygame.event.get():pass
        myKey = getattr(pygame, 'K_{}'.format(keyName))
        keyInput = pygame.key.get_pressed()
        return keyInput[myKey]

    def wait(self,t=0.1):
        time.sleep(t)    

    def getkeyRelease(self, keyName):
        ans = False
        for event in pygame.event.get():pass
        myKey = getattr(pygame, 'K_{}'.format(keyName))
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == myKey:
                    ans = True  
        return ans
    def exit(self) :
        pygame.quit()

# if iam running as main file
if __name__ == '__main__':
    command = KeyBoard()
    command.init()
    pyrun = True
    while pyrun:
        command.wait()
        if command.getkeyPressed("a"):
            print("a pressed")   
        if command.getkeyPressed("s"):
            print("s pressed")
        if command.getkeyRelease("s"):
            print("s released")
        if command.getkeyPressed("LEFT"):
            print("a pressed")
        if command.getkeyPressed("ESCAPE") :
            pygame.quit()
            break


        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pyrun = False
        #         pygame.quit()
