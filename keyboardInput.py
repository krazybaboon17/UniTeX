from pynput import keyboard
import mathTyping

charList = []
cursorPosition = 0
paused = False

def toggle_pause(from_source="Esc"):
    global paused, cursorPosition
    if mathTyping.isActive():
        mathTyping.cancel()
        charList.clear()
        cursorPosition = 0
        print("\nUniFlow Template Cancelled")
    paused = not paused
    charList.clear()
    cursorPosition = 0
    if paused:
        print(f"\n[UniFlow] Paused ({from_source}). Press Esc or widget to resume")
    else:
        print(f"\n[UniFlow] Resumed ({from_source})")
    try:
        import ipc
        ipc.set_paused(paused)
    except Exception:
        pass

def set_paused_state(new_state, from_source="widget"):
    global paused, cursorPosition
    if mathTyping.isActive():
        mathTyping.cancel()
        charList.clear()
        cursorPosition = 0
        print("\nUniFlow Template Cancelled")
    if paused != new_state:
        paused = new_state
        charList.clear()
        cursorPosition = 0
        if paused:
            print(f"\n[UniFlow] Paused ({from_source}). Press Esc or widget to resume")
        else:
            print(f"\n[UniFlow] Resumed ({from_source})")
        try:
            import ipc
            ipc.set_paused(paused)
        except Exception:
            pass

def onPress(key):
    global cursorPosition
    global paused
    if key == keyboard.Key.esc:
        if mathTyping.isActive():
            mathTyping.cancel()
            charList.clear()
            cursorPosition = 0
            print("\nUniFlow Template Cancelled")
            return
        toggle_pause(from_source="Esc")
        return
    if paused:
        return
    if mathTyping.handleKey(key):
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
    elif key == keyboard.Key.space:
        charList.insert(cursorPosition, " ")
        cursorPosition += 1
    elif key == keyboard.Key.enter:
        charList.clear()
        cursorPosition = 0
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