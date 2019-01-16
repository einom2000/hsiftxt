import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime


def key_2_sent(key):
    key_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5) # I shortened this to match the new value in your arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        if msg[0:4] == 'Done':
            # print("Message from arduino: ")
            # print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.3)
    return

def


logging.basicConfig(filename='running.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')

if os.path.basename(__file__) == 'hsiftxt_v3.01.py':
    port = 'COM10'  # note I'm not using Mac OS-X
elif os.path.basename(__file__) == 'hsiftxt_v3.01_sur.py':
    port = 'COM3'
else:
    port = ''
    print('Wrong file name found!')
    sys.exit()
try:
    ard = serial.Serial(port, 9600, timeout=5)
    time.sleep(2)  # wait for arduino
except FileNotFoundError:
    print('There is no port named ' + port + ' !' )
    sys.exit()
except:
    print('Unexpected Error!')
    sys.exit()
