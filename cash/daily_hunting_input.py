import time
import re
import json
import easyquotation
import winsound
from colorama import init, Fore, Back, Style
import ast

init()
quotation = easyquotation.use('sina')


def get_yesterday(data_file_name):
    with open(data_file_name, mode='rb') as file:
        file.seek(-32, 2)
        dt = int.from_bytes(file.read(4), byteorder='little')
        opn_at = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
        hghst = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
        lwst = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
        cls_at = round(int.from_bytes(file.read(4), byteorder='little') / 100, 2)
    return dt, opn_at, hghst, lwst, cls_at


def get_name(code):
    name = quotation.stocks(code).get(code).get('name')
    return name


def line_shape():
    if close_at > open_at:
        sta = 1
        hd = highest - close_at
        ft = open_at - lowest
        bd = close_at - open_at
    elif close_at < open_at:
        sta = -1
        hd = highest - open_at
        ft = close_at - lowest
        bd = open_at - close_at
    else:
        sta = bd = 0
        hd = highest - open_at
        ft = open_at - lowest
    return sta, round(hd, 2), round(ft, 2), round(bd, 2)

def algorithm():

    # 最高收 或者 开最低且上影短于本体1/3, redcross
    if close_at == highest or (open_at == lowest and head * HDFT_BODY_RATIO <= body)\
            or (status == 1 and body / close_at <= 0.01):
        print(Fore.RED + Style.BRIGHT + '|' + code[1:] + '|' + name + '|' + str(date) + '|开:' + str(open_at) + '|收:' + str(close_at)
              + '|高:' + str(highest) + '|低:' + str(lowest))
        print(Fore.RED + Style.DIM + '最高收 或者 开最低且上影短于本体1/3, redcross', end='')
        print(Style.RESET_ALL)
        suggested_hunting_bid = close_at
        classification = 1
    # 阳线，上影线短于下影线1/3, 或者阴线， 下影线长于上影线5倍, 或者阳线，无下影线
    elif (status == 1 and head * HEAD_FOOT_RATIO <= foot) or \
            (status == -1 and foot >= head * HEAD_FOOT_RATIO * 1.66) or \
            (status == 1 and foot == 0 and head * HDFT_BODY_RATIO <= body):
        print(Fore.MAGENTA + Style.BRIGHT + '|' + code[1:] + '|' + name + '|' + str(date) + '|开:' + str(open_at) + '|收:' + str(close_at)
              + '|高:' + str(highest) + '|低:' + str(lowest))
        print(Fore.MAGENTA + Style.DIM + '阳线，上影线短于下影线1/3, 或者阴线， 下影线长于上影线5倍, 或者阳线，无下影线', end='')
        print(Style.RESET_ALL)
        suggested_hunting_bid = close_at * 1.01
        classification =2
    # 最低收 或者 最高开 且下影短于本体1/3
    elif close_at == lowest or (open_at == highest and foot * HDFT_BODY_RATIO <= body):
        print(Fore.GREEN + Style.BRIGHT + '|' + code[1:] + '|' + name + '|' + str(date) + '|开:' + str(open_at) + '|收:' + str(close_at)
              + '|高:' + str(highest) + '|低:' + str(lowest))
        print(Fore.GREEN + Style.DIM + '最低收 或者 最高开 且下影短于本体1/3', end='')
        print(Style.RESET_ALL)
        suggested_hunting_bid = close_at - (close_at * 0.1) * 0.40
        classification = 5
    # 阳线，上影线大于下影线5倍，或阴线 下阴线短于上阴线1/3
    elif (status == 1 and head >= foot * HEAD_FOOT_RATIO * 1.66 and foot != 0) or \
            (status == -1 and foot * HEAD_FOOT_RATIO <= head):
        print(Fore.YELLOW + Style.BRIGHT + '|' + code[1:] + '|' + name + '|' + str(date) + '|开:' + str(
            open_at) + '|收:' + str(close_at)
              + '|高:' + str(highest) + '|低:' + str(lowest))
        print(Fore.YELLOW + Style.DIM + '阳线，上影线大于下影线5倍，或阴线 下阴线短于上阴线1/3', end='')
        print(Style.RESET_ALL)
        suggested_hunting_bid = close_at - (close_at * 0.1) * 0.20
        classification = 4
    else:
        print(Fore.CYAN + Style.BRIGHT + '|' + code[1:] + '|' + name + '|' + str(date) + '|开:' + str(
            open_at) + '|收:' + str(close_at)
              + '|高:' + str(highest) + '|低:' + str(lowest))
        print(Fore.CYAN + Style.DIM + '无明显特征', end='')
        print(Style.RESET_ALL)
        suggested_hunting_bid = close_at - (close_at - lowest) / 2
        classification = 3
    print('we suggest hunting at: ', end='')
    print(PRT_LIB[classification-1] + Style.BRIGHT + str(round(suggested_hunting_bid, 2)), end='')
    print(Style.RESET_ALL)
    return suggested_hunting_bid


today = time.localtime()
timestamp = time.strftime('%b-%d-%Y', today)

file_path = 'C:\\new_ajzq_v6\\T0002\\blocknew\\'
block_name = timestamp + '-in-pool.blk'

PRT_LIB = [Fore.RED, Fore.MAGENTA, Fore.WHITE, Fore.YELLOW, Fore.GREEN]
HEAD_FOOT_RATIO = 2.3
HDFT_BODY_RATIO = 2.3

with open(file_path + block_name, 'r') as daily_block:
    daily_hunting_list = re.findall(r'\d+', daily_block.read())

print(daily_hunting_list)

'''
hunting file module
timestamp_hunting_record.json
{'code': 123123, 'buy_at': 22.22, 'buy_vol': 100, 'done?': False}
'''

# try to get yesterday /open / close /high and /low
filename = ''
classification= 0

for code in daily_hunting_list:
    if code[0] == '1':
        filename = 'C:\\new_ajzq_v6\\vipdoc\\sh\\lday\\sh' + code[1:] + '.day'
    elif code[0] == '0':
        filename = 'C:\\new_ajzq_v6\\vipdoc\\sz\\lday\\sz' + code[1:] + '.day'
    date, open_at, highest, lowest, close_at = get_yesterday(filename)

    name = get_name(code[1:])
    status, head, foot, body = line_shape()

    hunting_bid = algorithm()

    max_bid = round(close_at * 1.1, 2)
    min_bid = round(close_at * 0.9, 2)
    print(Fore.LIGHTBLUE_EX + 'Max at: ' + str(max_bid) + ' | Min at: ' + str(min_bid), end='')
    print(Style.RESET_ALL)

    input_is_done = False
    while not input_is_done:
        print('press enter to accept ', end='')
        print(Fore.RED + str(hunting_bid), end='')
        print(Style.RESET_ALL + ' ', end='')
        key = input('or type a new price')
        if key == '':
            input_is_done = True
        else:
            try:
                number = round(ast.literal_eval(key), 2)
                if number > max_bid or number < min_bid:
                    print(Fore.LIGHTYELLOW_EX + 'please input a valid price', end='')
                    print(Style.RESET_ALL)
                    winsound.Beep(2000, 400)
                else:
                    hunting_bid = number
                    input_is_done = True
            except SyntaxError:
                print(Fore.LIGHTYELLOW_EX + 'please input a valid price', end='')
                print(Style.RESET_ALL)
                winsound.Beep(2000, 400)
            except ValueError:
                print(Fore.LIGHTYELLOW_EX + 'please input a valid price', end='')
                print(Style.RESET_ALL)
                winsound.Beep(2000, 400)






