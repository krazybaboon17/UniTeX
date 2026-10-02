from pynput.keyboard import Key, Controller
import shortcutDetection
import keyboardInput
import time

keyboard = Controller()

def deleteShortcut(word):
    for i in range(len(word)):
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)