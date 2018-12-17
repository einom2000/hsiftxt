import time
from tkinter import *


frame = Tk()
frame.overrideredirect(1)
frame.attributes("-topmost", True)
frame.geometry('400x80+0+0')
frame.update()
time.sleep(2)
frame.destroy()
time.sleep(100)
