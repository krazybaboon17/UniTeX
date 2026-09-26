import keyboardInput
import time
import shortcutDetection

listener = keyboardInput.startListener()

while listener.is_alive():
    word = keyboardInput.returnWord()
    if shortcutDetection.isShortcut(word):
        print(shortcutDetection.getShortcutName(word), "is a shortcut for", shortcutDetection.getSymbol(shortcutDetection.getShortcutName(word)))
    time.sleep(0.1)

listener.stop()

