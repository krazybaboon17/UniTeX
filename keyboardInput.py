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

def onRelease(key):
    if key == keyboard.Key.esc:
        return False

def returnWord():
    return("".join(charList))

def startListener():
    listener = keyboard.Listener(on_press=onPress, on_release=onRelease)
    listener.start()
    return listener

if __name__ == "__main__":
    listener = startListener()
    listener.join()
        

