import keyboard, pyautogui,time, winshell, os
# while True:
#     if keyboard.is_pressed(' '):
#         print(pyautogui.position())
#         time.sleep(1)

# SPEECH_BOX = (39, 610, 60, 40)
# print(pyautogui.locateCenterOnScreen('speech_box.png', region=SPEECH_BOX))
#
acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
log_in_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path

print(log_in_data)
print(bn_target)