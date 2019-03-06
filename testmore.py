

# (83, 263) KUAISUBISAI
# (315, 346) SHISHIZHANCHANG
# (400, 530) CONFIRMED
# (575, 322) jiaruzhandou
# (516, 303)(638, 338) squre jiaruzhandou
#----ABOVE ON 1280X 710

# import numpy as np
#
# a = (1, 2, 3, 4)
# b = (1,1,1,1)
# print(np.add(a, b))

# int('d')

import keyboard
import pyautogui
import time

while True:
    while keyboard.is_pressed(' '):
        print(pyautogui.position())
        time.sleep(1)
#
# import random, pyautogui,time,keyboard
# lst = [(281, 440), (276, 473), (283, 509), (277, 544)]
# running = True
# t = 0
# while running:
#     ran_pos = lst[random.randint(0, 3)]
#     pyautogui.moveTo(ran_pos[0], ran_pos[1])
#     time.sleep(.5)
#     pyautogui.click()
#     time.sleep(.5)
#     t += 1
#     if keyboard.is_pressed(' ') or t >= 100:
#         running = False


