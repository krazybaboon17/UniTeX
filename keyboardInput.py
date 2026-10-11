from pynput import keyboard
import mathTyping

charList = []
cursorPosition = 0
paused = False
def onPress(key):
    global cursorPosition
    global paused
    if mathTyping.handleKey(key):
        return
    if key == keyboard.Key.space or key == keyboard.Key.enter or key == keyboard.Key.tab:
        charList.clear()
        cursorPosition = 0
    if key == keyboard.Key.esc:
        paused = not paused
        charList.clear()
        cursorPosition = 0
        if paused:
            print("\nUniTeX Paused. Press Esc to resume")
        else:
            print("\nUniTeX Resumed")
    if paused:
        return
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
    pass

def returnWord():
    return("".join(charList))

def setWord(word):
    global cursorPosition
    charList[:] = list(word)[-256:]
    cursorPosition = len(charList)

def startListener():
    listener = keyboard.Listener(on_press=onPress, on_release=onRelease)
    listener.start()
    return listener

if __name__ == "__main__":
    listener = startListener()
    listener.join()