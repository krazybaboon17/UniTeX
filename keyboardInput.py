from pynput import keyboard
import mathTyping
import sys

charList = []

if sys.platform == "darwin":
    from Quartz import CGEventGetIntegerValueField, kCGEventKeyDown, kCGEventKeyUp, kCGKeyboardEventKeycode

    def interceptTab(eventType, event):
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        if keycode == 48 and eventType in (kCGEventKeyDown, kCGEventKeyUp) and mathTyping.isTabPending():
            if eventType == kCGEventKeyUp:
                mathTyping.clearTabPending()
            return None
        return event

def onPress(key):
    if mathTyping.handleKey(key):
        return
    if key == keyboard.Key.space:
        charList.append(" ")
    elif key == keyboard.Key.backspace:
        if charList:
            charList.pop()
    elif getattr(key, "char", None) is not None:
        charList.append(key.char)
    if len(charList) > 256:
        del charList[:-256]

def onRelease(key):
    if key == keyboard.Key.esc:
        return False

def returnWord():
    return("".join(charList))

def setWord(word):
    charList[:] = list(word)[-256:]

def startListener():
    listenerOptions = {}
    if sys.platform == "darwin":
        listenerOptions["darwin_intercept"] = interceptTab
    listener = keyboard.Listener(on_press=onPress, on_release=onRelease, **listenerOptions)
    listener.start()
    return listener

if __name__ == "__main__":
    listener = startListener()
    listener.join()