import pyautogui, random

k1 = pyautogui.easeInQuad
k2 = pyautogui.easeOutQuad
k3 = pyautogui.easeInOutQuad
k4 = pyautogui.easeInBounce
k5 = pyautogui.easeInElastic

pyautogui.moveTo(200, 300, 2, random.choice([k1, k2, k3, k4,k5]))