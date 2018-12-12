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

def get_random_wait(low, high):
    # wait for a random time
    time.sleep(random.randint(low, high) / 1000)

def blur_pos_dur():
    # get a random blur relevant x and y and random time according to the constants
    x = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    y = random.randint(BLUR_PIXEL[0], BLUR_PIXEL[1]) * random.choice([-1, 1])
    t = random.randint(BLUR_DUR[0], BLUR_DUR[1])
    return x, y, t


# Game variables
infoTxt = ''
hookMissed = 0
soundMissed = 0
count = 0

# load standard images
dobber_images = []
for i in range(1, 10+1):
    dobber_images.append("pp{}.png".format(i))


class CastPole:
    # cast the pole and looking for the dobber
    # move mouse to the dobber

    def __init__(self, mouse_position):
        self.mouse_pos = mouse_position

    def cast(self):
        # get a blur
        blur_x, blur_y, dur_t = blur_pos_dur()
        self.mouse_pos =tuple(map(lambda x, y: x + y, self.mouse_pos,
                                      (blur_x * 3, blur_y * 3)))
        # right double click
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(100, 300)
        pyautogui.rightClick(self.mouse_pos[0], self.mouse_pos[1], dur_t)
        get_random_wait(500, 800)

    def find_hooker(self, rect, confi):
        found_hook = False
        for i in range(0, 5):
            for img in dobber_images:
                img_found = pyautogui.locateCenterOnScreen()






cl = CastPole((300, 400))
cl.cast()

