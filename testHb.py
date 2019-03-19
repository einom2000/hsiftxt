import keyboard, pyautogui,time
# while True:
#     if keyboard.is_pressed(' '):
#         print(pyautogui.position())
#         time.sleep(1)

SPEECH_BOX = (39, 610, 60, 40)
print(pyautogui.locateCenterOnScreen('speech_box.png', region=SPEECH_BOX))

