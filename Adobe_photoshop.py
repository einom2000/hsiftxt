
# version 1.9

# move cursor with Bézier curve
# put info window down center and attach the scope frame
# rename program verytime run
# silent running



import pyautogui, win32gui,keyboard
import time
import random, winsound
from tkinter import *


# set window to 1280x720, high resolusion, zoom till no head, move horizon to the top
# lefttop = 500,130, rightbottom = 900, 300

fields = 'Screen Size X', 'Screen Size Y"', 'Wonder Factor X Low', 'Wonder Factor X High', 'Wonder Factor Y Low',\
         'Wonder Factor Y High', 'Wonder Factor Duration Low ', 'Wonder Factor Duration High', 'Min Volume Threshold %',\
         'Max Volume Threshold %', 'Swap pixels over boob(0=no)', 'Start Key', \
         'Stop Key', 'Run for minutes'

defaultvalues = [1280, 720, 6, 16, 6, 10, 250, 400, 35, 80, 0, 'F10', 'F12', 480]

entrycolors = "lemon chiffon", "lemon chiffon", "white", "white", "lemon chiffon", "lemon chiffon", "white", "white", \
             "lemon chiffon", "lemon chiffon", "white", "lemon chiffon", "lemon chiffon",  "LightSkyBlue1"

keysindic = 'SCREENSIZE', 'LEFTTOP', 'RIGHTBOTTOM ', 'RATIO', 'XWONDER', 'YWONDER', 'DURWONDER', 'MINVOLUME ', \
            'MAXVOLUME', 'SWAPPIXEL', 'STARTKEY', 'STOPKEY', 'ELASPE', 'REALELASPE'

# AUDIO_SAMPLE_RATE = 48e3
# AUDIO_FRAME_SAMPLES = 1024 * 7
# LEFT_CHANNEL = 0
# RIGHT_CHANNEL = 1

VARTXT = ""
MISSHK = 0
MISSSND =0
COUNT = 0


def main(entries, rttk):
    newvalues = fetch(entries)
    global COUNT
    starttime = time.time()
    timelast = starttime
    # print(newvalues)
    rttk.destroy()
    try:
        setGlobal(newvalues)
    except ValueError:
        sys.exit()
    # print ('SCREENSIZE=', SCREENSIZE, 'LEFTTOP=', LEFTTOP, 'RIGHTBOTTOM=', RIGHTBOTTOM,
    #        'XWONDER=', XWONDER, 'YWONDER=', YWONDER, 'DURWONDER=', DURWONDER, 'MINVOLUME=', MINVOLUME,
    #        'MAXVOLUME=', MAXVOLUME,'SEARCHINGCURSORSTEP=', 'SWAPPIXEL=', SWAPPIXEL,
    #        'STARTKEY=', STARTKEY, 'STOPKEY=', STOPKEY, 'REALELASPE=', REALELASPE)
    global VARTXT
    VARTXT ='SCREENSIZE='+ str(SCREENSIZE) + '; LEFTTOP=' + str(LEFTTOP) + '; RIGHTBOTTOM=' + str(RIGHTBOTTOM) +\
            '; XWONDER=' + str(XWONDER) + '; YWONDER=' + str(YWONDER) + '; DURWONDER=' + str(DURWONDER) + '; MINVOLUME='\
            + str(MINVOLUME) + '; MAXVOLUME=' + str(MAXVOLUME) + \
            '; SWAPPIXEL=' + str(SWAPPIXEL) + '; STARTKEY=' + str(STARTKEY) + '; STOPKEY=' + str(STOPKEY) + \
            '; REALELASPE=' + str(REALELASPE) + '\n' + '/console weatherDensity 0'
    frame = Tk()
    frame.overrideredirect(1)
    frame.attributes("-topmost", True)
    frame.geometry('400x80+0+0')
    text = Text(frame, wrap=WORD, height=7)
    text.config(background="gray", foreground="black")
    # scrollbar = Scrollbar(frame)
    # scrollbar.config(command=text.yview)
    # text.config(yscrollcommand=scrollbar.set)
    text.insert('1.0', VARTXT)
    # scrollbar.pack(side=RIGHT, fill=Y)
    text.pack(expand=YES, fill=BOTH)
    VARTXT = 'Press ' + str(STARTKEY) + 'to Continue or Press ' + str(STOPKEY) + 'to Stop! \n'
    text.insert('1.0',VARTXT)
    frame.update()

    scopelength = RIGHTBOTTOM[0] - LEFTTOP[0]
    scopehight = RIGHTBOTTOM[1] - LEFTTOP[1]
    masterup = Tk()
    masterup.overrideredirect(1)
    masterup.attributes("-topmost", True)
    geo0 = str(scopelength) + 'x2+' + str(LEFTTOP[0]) + '+' + str(LEFTTOP[1])
    masterup.geometry(geo0)
    # canvasup = Canvas(masterup)
    # canvasup.pack()
    # canvasup.create_line(LEFTTOP[0] , LEFTTOP[1] , LEFTTOP[0] + scopelength, LEFTTOP[1])
    masterdown = Tk()
    masterdown.overrideredirect(1)
    masterdown.attributes("-topmost", True)
    geo1 = str(scopelength) + 'x2+' + str(LEFTTOP[0]) + '+' + str(RIGHTBOTTOM[1])
    masterdown.geometry(geo1)
    masterleft = Tk()
    masterleft.overrideredirect(1)
    masterleft.attributes("-topmost", True)
    geo2 = '2x' + str(scopehight) + '+' + str(LEFTTOP[0]) + '+' + str(LEFTTOP[1])
    masterleft.geometry(geo2)
    masterright = Tk()
    masterright.overrideredirect(1)
    masterright.attributes("-topmost", True)
    geo3 = '2x' + str(scopehight+2) + '+' + str(LEFTTOP[0]+scopelength) + '+' + str(LEFTTOP[1])
    masterright.geometry(geo3)
    masterup.update()
    masterdown.update()
    masterleft.update()
    masterright.update()
    # print(LEFTTOP, RIGHTBOTTOM)

    for i in range(0, 5):
        speakerintensitycoor = pyautogui.locateOnScreen('speaker.png', region=(SCREENSIZE[0], 0, \
                                                        SCREENSIZE[0] + 500, 800), confidence=0.5)
        if speakerintensitycoor != None:
            break
    if speakerintensitycoor == None:
        text.destroy()
        frame.destroy()
        popAndEnd("\n There is no mixer found on screen in slient mode!")

      # ======================

    c = waitForKeyin()

    if c == 0:
        text.destroy()
        frame.destroy()
        popAndEnd("")

    pyautogui.moveTo(LEFTTOP[0] + (RIGHTBOTTOM[0]-LEFTTOP[0]) * 10 / 20, LEFTTOP[1] + (RIGHTBOTTOM[1]-LEFTTOP[1]) \
                     * 10 / 20, random.randint(300, 500) / 1000, pyautogui.easeOutQuad)


    randomcheck = random.randint(580, 780)
    while True:
        VARTXT = ""
        main1(speakerintensitycoor)
        checkQuit()
        randomWait(1200,1500)
        if time.time() - timelast >= randomcheck:
            randomWait(800, 1200)
            pyautogui.press('f4')
            randomWait(1200, 1500)
            pyautogui.press('space')
            randomWait(500, 700)
            timelast = time.time()
            randomcheck = random.randint(600, 880)
        if time.time() - starttime >= REALELASPE:
            # print('It is time to stop!')
            text.insert('1.0', 'It is time to stop!\n')
            randomWait(1200, 1500)
            pyautogui.press('f8')
            frame.destroy()
            popAndEnd("")
        COUNT += 1
        # print("Time to exit:", REALELASPE - time.time() + starttime, " and loops = ", COUNT, "times.")
        text.insert('1.0', "Time to exit:" + str(int(REALELASPE - time.time() + starttime)) + " and loops = " + \
                    str(COUNT) + "times.\n")
        text.insert('1.0', VARTXT)
        text.insert('1.0', "Hk missed total = " + str(MISSHK) + ";  Sound Missed = " + str(MISSSND) + "\n")
        frame.update()
        masterup.update()
        masterdown.update()
        masterleft.update()
        masterright.update()
        checkQuit()


def main1(speakerintensitycoors):
    #normalCursorHandle = getNormalCursorhandle()
    # print ('original mouse handle = ', normalCursorHandle)
    randomWait(1000, 1800)
    #get normalCursorHandle

    castPole(1, 4, 1, 5, 200, 400)
    randomWait(800, 1200)

    findHooker = findimgHooker(LEFTTOP, RIGHTBOTTOM)
    hookerposition = findHooker[1]

    if findHooker[0] and hookerposition != None:
            pyautogui.moveTo(hookerposition[0], hookerposition[1], random.randint(400,900)/1000,  pyautogui.easeOutQuad)
            if SWAPPIXEL != 0:
                swap = random.randint(int(0.6 * SWAPPIXEL), int(1.2 * SWAPPIXEL))
                shakeToSecure(findHooker[1], swap)
            l = listenMic(MINVOLUME, speakerintensitycoors)
            randomWait(400, 600)
            if l == 1:
                randomWait(400, 600)
                pyautogui.rightClick()
                # castPole(-2, 2, -2, 2, 200, 400)


    #cast works as pickup

def findimgHooker(ltp, rbtm):
    global VARTXT, MISSHK
    flag = 0
    images = 'pp1.png', 'pp2.png','pp3.png','pp4.png','pp5.png','pp6.png','pp7.png','pp8.png','pp9.png','pp10.png'
    # print(ltp,rbtm)
    for i in range(0, 5):
        for image in images:
            foundimg = pyautogui.locateCenterOnScreen(image, region=(ltp[0], ltp[1], rbtm[0], rbtm[1]), confidence=.5)
            if foundimg != None:
                flag = 1
                break
        checkQuit()

    if flag != 1:
        # print('Can not find the hongkong!')
        VARTXT = VARTXT+ 'Can not find the hongkong!\n'
        MISSHK += 1
        pyautogui.moveTo(LEFTTOP[0] + (RIGHTBOTTOM[0] - LEFTTOP[0]) * 10 / 20,
                         LEFTTOP[1] + (RIGHTBOTTOM[1] - LEFTTOP[1]) \
                         * 10 / 20, random.randint(300, 500) / 1000, pyautogui.easeOutQuad)
        foundimg = None
    randomWait(300,500)
    checkQuit()
    return (flag, foundimg)

def setGlobal(newvalues):
    global SCREENSIZE, LEFTTOP, RIGHTBOTTOM, RATIO, XWONDER, YWONDER, DURWONDER, MINVOLUME, MAXVOLUME, \
           SWAPPIXEL, STARTKEY, STOPKEY, REALELASPE, PROGRAMSTARTTIME
    SCREENSIZE = (newvalues[0],newvalues[1])
    LEFTTOP = (int(SCREENSIZE[0] * 0.20), 80)
    RIGHTBOTTOM = (int(2.2 * SCREENSIZE[0] / 3), int(SCREENSIZE[1] * 0.45))
    RATIO = RATIO = SCREENSIZE[0] / SCREENSIZE[1]
    XWONDER = (newvalues[2],newvalues[3])
    YWONDER = (newvalues[4],newvalues[5])
    DURWONDER = (newvalues[6],newvalues[7])
    MINVOLUME = newvalues[8]
    MAXVOLUME = newvalues[9]
    SWAPPIXEL = newvalues[10]
    STARTKEY = newvalues[11]
    STOPKEY = newvalues[12]
    REALELASPE = random.randint(int(0.8 * newvalues[13]*60), int(1.2 * newvalues[13]*60))
    PROGRAMSTARTTIME = time.time()


def fetch(entries):
    newvalues =[]
    for entry in entries:
        text = entry[1].get()
        try:
            newvalues.append(int(text))
        except ValueError:
            newvalues.append(text)
    return newvalues


def makeform(root, fields, defaultvalues, entrycolors):
    entries = []
    for i in range(0, len(fields)):
        # print(i)
        row = root
        lab = Label(row, text=fields[i], font=("arial", 10, "bold"), fg="black")
        ent = Entry(row)
        ent.config({"background": entrycolors[i]})
        ent.delete(0, END)
        ent.insert(END, defaultvalues[i])
        lab.grid(row=i, sticky=E)
        ent.grid(row=i, column=1)
        entries.append((fields[i], ent))
    return entries

def getRandomNum(mimium, maxium):
    randomNum = random.randint(mimium,maxium)
    return randomNum

def check_for_key_in():
    if keyboard.is_pressed(STARTKEY):
        key = 1
    elif keyboard.is_pressed(STOPKEY):
        key = 0
    else:
        key = 99
    return key

def listenMic(threshold, speakerintensityposition):
    global VARTXT, MISSSND
    result = 99
    t=time.time()
    randomWait(800, 1000)

    # speakerintesityX = int(speakerintensityposition[0] + 3)
    # speakerintensityY = int(speakerintensityposition[1] + (140 - threshold) - (threshold - 40) / 2)

    im = pyautogui.screenshot(region=(speakerintensityposition[0], speakerintensityposition[1], \
                                      speakerintensityposition[0] + 20, speakerintensityposition[1] + 150))
    # pyautogui.moveTo(speakerintensityposition[0], speakerintensityposition[1])
    # pyautogui.moveTo(speakerintensityposition[0] + 20, speakerintensityposition[1] + 150)
    # while True:
    #     pass
    checkcolor = im.getpixel((3, int((140 - threshold) - (threshold - 40) / 2)))
    while True:
        checkQuit()
        im2 = pyautogui.screenshot(region=(
        speakerintensityposition[0], speakerintensityposition[1], speakerintensityposition[0] + 20,
        speakerintensityposition[1] + 150))

        checkcolor2 = im2.getpixel((3, int((140 - threshold) - (threshold - 40) / 2)))
        if checkcolor != checkcolor2:
            result = 1
            VARTXT = ""
            break
        if time.time() - t > 22:
            result = 0
            VARTXT = "sorry Buddy!\n"
            MISSSND += 1
            break
    return result



# =======================================================

def waitForKeyin():
    # print('Please Press ', STARTKEY, 'to Continue and Press ', STOPKEY, 'to Stop')
    while True:
        checkForKey = check_for_key_in()
        if checkForKey == 1:
            winsound.Beep(1000, 300)
            break
        elif checkForKey == 0:
            winsound.Beep(1000, 200)
            winsound.Beep(500, 300)
            break
        else:
            pass
    return checkForKey

def castPole(minXTrim, maxXTrim, minYTrim, maxYTrim, minDur, maxDur):
    rm = mouseWondering(minXTrim, maxXTrim, minYTrim, maxYTrim, minDur, maxDur)
    mousePosition = pyautogui.position() + (rm[0], rm[1])
    pyautogui.rightClick(mousePosition[0], mousePosition[1], rm[2])
    randomWait(100,300)
    pyautogui.rightClick(mousePosition[0], mousePosition[1], rm[2])
    # print('mouse wonder x y and time is =', rm)

def randomWait(min, max):
    time.sleep(random.randint(min, max) / 1000)

def getNormalCursorhandle():
    randomWait(300,500)
    rm = mouseWondering(XWONDER[0],XWONDER[1], YWONDER[0], YWONDER[1], DURWONDER[0], DURWONDER[1])
    pyautogui.moveRel(rm[0], rm[1], rm[2], pyautogui.easeOutQuad)
    randomWait(200,300)
    mouseInfo = win32gui.GetCursorInfo()
    return mouseInfo[1]

def mouseWondering(minX, maxX, minY, maxY, minDur, maxDur):
    randomXTrim = getRandomNum(minX, maxX)
    randomYTrim = getRandomNum(minY, maxY)
    randomDur = getRandomNum(minDur, maxDur) / 1000
    return (randomXTrim, randomYTrim, randomDur)

def shakeToSecure(currentCursor, step):
    currentMousePosition = pyautogui.position()
    pyautogui.moveRel(step, random.randint(0,step), random.randint(300, 700) / 1000, pyautogui.easeInBounce)
    currentCursor2 = win32gui.GetCursorInfo()
    # print(currentCursor, currentCursor2[1])
    if currentCursor2[1] != currentCursor:
        randomWait(100,300)
        pyautogui.moveRel(step * (-2.0),  random.randint(0, step) * (-1), random.randint(300, 700) / 1000, pyautogui.easeInBounce)
    randomWait(100,300)

def checkQuit():
    isQuit = check_for_key_in()
    if isQuit == 0:
        winsound.Beep(1000, 200)
        winsound.Beep(500, 300)
        popAndEnd("")

def popAndEnd(text):
        msg=text + getCalc()
        pyautogui.press('v')
        popUpMsg(msg)


def getCalc():
    global PROGRAMSTARTTIME, COUNT, MISSSND, MISSHK
    msg = "This program has run for " + str(int(time.time() - PROGRAMSTARTTIME)) + " seconds. \n" + \
          "Totally " + str(COUNT) + " tries.\n"+ \
          "Among them, there are " + str(MISSHK + MISSSND) + " strikes missed.\n" \
          "Approximately " + str(COUNT-MISSHK-MISSSND) + " catches! \n" \
          "They worth about " + str((COUNT-MISSHK-MISSSND)*8) + " golds! \n" \
          "Average effiency is about " + str(int(((COUNT-MISSHK-MISSSND)*8)/int(time.time() - PROGRAMSTARTTIME) \
                                                 * 3600)) + " gold per hour! \n" + "Happy Fishing Wow!"

    return msg

def popUpMsg(msg):
    popup = Tk()
    popup.overrideredirect(1)
    popup.geometry('500x200+250+200')
    popup.attributes("-topmost", True)
    text = Text(popup, wrap=WORD, height=7)
    text.config(background="white", foreground="black", font=("Helvetica", 12))
    scrollbar = Scrollbar(popup)
    scrollbar.config(command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    text.insert('1.0', msg)
    scrollbar.pack(side=RIGHT, fill=Y)
    text.pack(expand=YES, fill=BOTH)
    B1 = Button(popup, text="Exit", font=("Helvetica", 14), command = lambda : sys.exit())
    B1.pack()
    popup.mainloop()

if __name__ == '__main__':

    root = Tk()
    root.title("Students Name List")
    root.resizable(width=False, height=False)
    root.attributes("-topmost", True)

    ents = makeform(root, fields, defaultvalues, entrycolors)
    # root.bind('<Return>', (lambda event, e=ents: main(e)))

    buttonOk = Button(root, text="OK", font=("arial", 16, "bold"))
    buttonOk['command'] = lambda e=ents, rttk=root: main(e, rttk)
    buttonOk.grid(columnspan=2)

    root.mainloop()



