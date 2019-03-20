from cash import coordination
import pyautogui
import time
import keyboard
import json
from colorama import init, Fore, Back, Style
import winsound
import pyperclip
init()
SPF = 1.5
# while not keyboard.is_pressed(','):
# #     pass
# # time.sleep(3)


def auto_key_in(cd, pr, vl):
    # biding
    time.sleep(SPF)
    pyautogui.click(coordination.BIDDING_BUTTON)
    time.sleep(SPF)
    # code
    pyautogui.click(coordination.CODE_INPUT_BOX)
    time.sleep(SPF)
    pyperclip.copy(cd)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(SPF)
    # make sure paste is ok
    # # price
    # pyautogui.click(coordination.PRICE_INPUT_BOX)
    # time.sleep(SPF)
    # pyautogui.dragRel(-80, 0, 1, button='left')
    # time.sleep(SPF)
    pyperclip.copy(pr)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(SPF)
    # volume
    pyautogui.click(coordination.BIDDING_VOLUME_INPUT_BOX)
    time.sleep(SPF)
    pyperclip.copy(vl)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(SPF)
    # go
    pyautogui.click(coordination.GO_BID_BUTTON)
    time.sleep(3)
    pyautogui.click(coordination.CONFIRM)
    time.sleep(2)
    pyautogui.click(coordination.CONFIRM)
    time.sleep(2)
    pyautogui.click(coordination.END_BUTTON)
    time.sleep(2)

with open('snipper_nextday.json', 'r') as fp:
    dic = json.load(fp)
snipper_list = []
for item in dic:
    if len(item) > 6:
        code = item[1:]
        name = dic.get(code)
        plan = dic.get(item)
        snipper_list.append((code, name, plan))
total_value = 0
for stock_2_snipper in snipper_list:
    code = stock_2_snipper[0]
    bidding_price = stock_2_snipper[2][0]
    bidding_volume = int(stock_2_snipper[2][1])
    total_value += float(bidding_price) * bidding_volume
    print(code, bidding_price, bidding_volume, stock_2_snipper[1])

print(Fore.RED + Style.BRIGHT + 'PLEASE CHECK CAREFULLY BEFORE AUTO KEY IN!')
print('TOTAL VALUE = ' + str(total_value))
print('请仔细检查，确保无误，资金充足，回到交易界面，按，键开始')

while not keyboard.is_pressed(','):
    pass

for stock_2_snipper in snipper_list:
    code = stock_2_snipper[0]
    bidding_price = stock_2_snipper[2][0]
    bidding_volume = int(stock_2_snipper[2][1])
    auto_key_in(code, bidding_price, bidding_volume)
