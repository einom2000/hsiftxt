# Auto Simple Fishing v2.0
# No overlay windows
# No info. windows during fishing
# will have a text windows after fishing
# auto close wow
# auto anti-AFK
# optimized sound detect

import pyautogui, win32gui, keyboard
import time, random, winsound
from tkinter import *

# user options as constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLUR_PIXEL = [6, 16]
BLUR_DUR = [250, 400]
SOUND_THRESHOLD = 0.50
HAND_SHAKE_FACTOR = 0
START_KEY = 'F10'
STOP_KEY = 'F12'
TIME_TO_RUN = 480
ANTI_AFT_TIME = 10

def getRandomWait(min, max):
    time.sleep(random.randint(min, max) / 1000)

def blurPosDur():
    blurXplus = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    blurYplus = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    blurTime = random.randint(BLUR_DUR[0], BLUR_DUR[1])
    return (blurXplus, blurYplus, blurTime)

# Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0

# load standard images
dobberImgs = []
for i in range(1, 10+1):
    dobberImgs.append("pp{}.png".format(i))


class CastPole:
    # cast the pole and looking for the dobber
    # move mouse to the dobber

    def __init__(self, mousePosition):
        self.mousePosition = mousePosition

    def castPole(self):
        getRandomWait(100, 300)
        blur = blurPosDur()
        print(blur)
        pass


def temp():
    print('here i am called')


cl = CastPole((300, 400))
cl.castPole()

