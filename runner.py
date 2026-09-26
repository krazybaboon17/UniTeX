import keyboardInput
import time
import shortcutDetection
import deletingShortcut
import writingValue

listener = keyboardInput.startListener()

while listener.is_alive():
    word = keyboardInput.returnWord()
    if shortcutDetection.isShortcut(word):
        print(shortcutDetection.getShortcutName(word), "is a shortcut for", shortcutDetection.getSymbol(shortcutDetection.getShortcutName(word)))
        deletingShortcut.deleteShortcut(word)
        writingValue.writeValue(shortcutDetection.getSymbol(shortcutDetection.getShortcutName(word)))

    time.sleep(0.1)

listener.stop()

