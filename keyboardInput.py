from pynput import keyboard

charList = []

def onPress(key):
    if key == keyboard.Key.space:
        charList.clear()
    elif key == keyboard.Key.backspace:
        if charList:
            charList.pop()
    elif getattr(key, "char", None) is not None:
        charList.append(key.char)
    returnWord()

def onRelease(key):
    if key == keyboard.Key.esc:
        return False

def returnWord():
    return("".join(charList))

with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()
        
