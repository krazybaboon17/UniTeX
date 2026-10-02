import keyboardInput
import time
import shortcutDetection
import deletingShortcut
import writingValue
import mathShortcuts
import mathTyping

listener = keyboardInput.startListener()

lastWord = ""
while listener.is_alive():
    word = keyboardInput.returnWord()
    if word != lastWord:
        print("word:", word)
        lastWord = word

    if shortcutDetection.isShortcut(word):
        print(shortcutDetection.getShortcutName(word), "is a shortcut for", shortcutDetection.getSymbol(shortcutDetection.getShortcutName(word)))
        deletingShortcut.deleteShortcut(word)
        writingValue.writeValue(shortcutDetection.getSymbol(shortcutDetection.getShortcutName(word)))

    elif word in mathShortcuts.templates:
        print(word, "is a math template")
        deletingShortcut.deleteShortcut(word)
        keyboardInput.charList.clear()
        mathTyping.start(word)

    time.sleep(0.1)

print("listener stopped")
listener.stop()