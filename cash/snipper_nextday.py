from cash import coordination
import pyautogui
import time
import keyboard
import shutil

# while not keyboard.is_pressed(','):
# #     pass
# # time.sleep(3)
# # pyautogui.click(coordination.BIDDING_BUTTON)
# # time.sleep(3)
# # pyautogui.click(coordination.SELLING_BUTTON)
today = time.localtime()
timestamp = time.strftime('%b-%d-%Y', today)
shutil.copy(timestamp + 'next_day_hunting.json', 'snipper_nextday.json')