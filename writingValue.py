import shortcutDetection
from pynput.keyboard import Key, Controller

keyboard = Controller()

def writeValue(value):
    keyboard.type(value)