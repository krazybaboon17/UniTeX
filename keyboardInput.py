from pynput import keyboard
import mathTyping
import sys

charList = []
cursorPosition = 0

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
    global cursorPosition
    if mathTyping.handleKey(key):
        return
    if key == keyboard.Key.space:
        charList.insert(cursorPosition, " ")
        cursorPosition += 1
    elif key == keyboard.Key.backspace:
        if cursorPosition > 0:
            del charList[cursorPosition - 1]
            cursorPosition -= 1
    elif key == keyboard.Key.delete:
        if cursorPosition < len(charList):
            del charList[cursorPosition]
    elif key == keyboard.Key.left:
        cursorPosition = max(0, cursorPosition - 1)
    elif key == keyboard.Key.right:
        cursorPosition = min(len(charList), cursorPosition + 1)
    elif getattr(key, "char", None) is not None:
        charList.insert(cursorPosition, key.char)
        cursorPosition += len(key.char)
    if len(charList) > 256:
        overflow = len(charList) - 256
        del charList[:overflow]
        cursorPosition = max(0, cursorPosition - overflow)

def onRelease(key):
    if key == keyboard.Key.esc:
        return False

def returnWord():
    return("".join(charList))

def setWord(word):
    global cursorPosition
    charList[:] = list(word)[-256:]
    cursorPosition = len(charList)

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