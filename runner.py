import keyboardInput
import time
import shortcutDetection
import deletingShortcut
import writingValue
import mathShortcuts
import mathTyping

def main():

    userChoice = input("Enter 0 for Settings, Enter 1 for Start: ")
    while (userChoice != "0" and userChoice != "1"):
        print("Invalid input")
        userChoice = input("Enter 0 for Settings, Enter 1 for Start: ")

    if userChoice == "0":
        print("Settings")
        print("Currently, the only option is to use Unicode. LaTeX will come with UniTeX 2.0")
    elif userChoice == "1":
        listener = keyboardInput.startListener()

        lastWord = ""
        pendingWord = None
        pendingSince = None
        while listener.is_alive():
            word = keyboardInput.returnWord()
            if word != lastWord:
                print("word:", word)
                lastWord = word

            match = shortcutDetection.findShortcut(word)
            templateMatch = None
            if match is None:
                templateMatch = mathShortcuts.findTemplate(word, shortcutDetection.shortcuts)

            if match is None and templateMatch is None:
                pendingMatch = shortcutDetection.findShortcut(word, allowAmbiguous=True)
                pendingTemplate = False
                if pendingMatch is None:
                    pendingMatch = mathShortcuts.findTemplate(
                        word, shortcutDetection.shortcuts, allowAmbiguous=True
                    )
                    pendingTemplate = pendingMatch is not None

            if pendingMatch is None:
                pendingWord = None
                pendingSince = None
            elif word != pendingWord:
                pendingWord = word
                pendingSince = time.monotonic()
            elif time.monotonic() - pendingSince >= 0.4:
                if pendingTemplate:
                    templateMatch = pendingMatch
                else:
                    match = pendingMatch
                pendingWord = None
                pendingSince = None
            else:
                pendingWord = None
                pendingSince = None

            if match is not None:
                shortcut, start, end = match
                suffix = word[end:]
                symbol = shortcutDetection.getSymbol(shortcut)
                print(shortcut, "is a shortcut for", symbol)
                deletingShortcut.deleteShortcut(shortcut + suffix)
                writingValue.writeValue(symbol + suffix)
                keyboardInput.setWord(suffix)

            elif templateMatch is not None:
                template, start, end = templateMatch
                suffix = word[end:]
                print(template, "is a math template")
                deletingShortcut.deleteShortcut(template + suffix)
                keyboardInput.setWord(suffix)
                mathTyping.start(template, suffix)

            time.sleep(0.1)

        print("listener stopped")
        listener.stop()

if __name__ == "__main__":
    main()