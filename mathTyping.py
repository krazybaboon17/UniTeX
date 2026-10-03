import threading
import time
from pynput.keyboard import Key, Controller
import mathShortcuts

keyboard = Controller()

name = None    # the template being filled in, like "//frac" (None = no template)
boxes = []     # what the user typed in each box
current = 0    # which box the user is typing in
busy = False   # True while this program is typing, so we ignore our own keys
tabPending = False
trailingText = ""
fractionWrapped = False


def press(key, times=1):
    for i in range(times):
        keyboard.press(key)
        keyboard.release(key)


def selectBox(arrow):
    # Shift + arrow highlights the □, so what the user types replaces it
    keyboard.press(Key.shift)
    press(arrow)
    keyboard.release(Key.shift)


def start(shortcut, trailing=""):
    # The runner calls this. Types the template (like □/□) and highlights the first box.
    global name, boxes, current, busy, tabPending, trailingText, fractionWrapped
    busy = True
    pattern = mathShortcuts.templates[shortcut]
    keyboard.type(pattern + trailing)
    press(Key.left, len(trailing) + len(pattern) - pattern.index("□") - 1)   # move back to the first □
    selectBox(Key.left)
    time.sleep(0.1)
    busy = False

    name = shortcut
    boxes = [""] * pattern.count("□")
    current = 0
    tabPending = False
    trailingText = trailing
    fractionWrapped = False


def nextBox():
    # Highlights the next □ (the user's arrow key already moved past the "/")
    global busy
    busy = True
    selectBox(Key.right)
    time.sleep(0.1)
    busy = False


def nextBoxWithTab(previous):
    global busy, fractionWrapped
    busy = True
    pieces = mathShortcuts.templates[name].split("□")
    if name == "//frac" and previous == 0:
        if boxes[previous]:
            keyboard.type(")")
            press(Key.left, len(boxes[previous]) + 1)
            keyboard.type("(")
            press(Key.right, len(boxes[previous]) + 1)
        else:
            keyboard.type("()")
        fractionWrapped = True
    elif not boxes[previous]:
        press(Key.right)
    press(Key.right, len(pieces[previous + 1]))
    selectBox(Key.right)
    time.sleep(0.1)
    busy = False


def finish():
    # Erases the template and types the finished version, like ¹²⁄₃₄
    global name, busy, tabPending, trailingText
    busy = True
    pieces = mathShortcuts.templates[name].split("□")   # "log_□(□)" -> ["log_", "(", ")"]

    before = 1                        # characters before the cursor (1 = the space)
    for i in range(current + 1):
        before = before + len(pieces[i]) + len(boxes[i])
    if name == "//frac" and fractionWrapped:
        before = before + 2

    after = len(trailingText) + len(boxes) - current - 1  # characters after the cursor (the empty □s...)
    for i in range(current + 1, len(pieces)):
        after = after + len(pieces[i])  # ...plus the pattern's leftover pieces

    press(Key.backspace, before)
    press(Key.delete, after)
    keyboard.type(mathShortcuts.finalText(name, boxes) + trailingText + " ")
    name = None
    tabPending = False
    trailingText = ""
    time.sleep(0.1)
    busy = False


def handleKey(key):
    # keyboardInput calls this for every key. Returns True if the key was for a box.
    global current, tabPending
    if busy:
        return True
    if name is None:
        return False

    if key == Key.tab:
        if not tabPending and current < len(boxes) - 1:
            previous = current
            current = current + 1
            tabPending = True
            threading.Timer(0.05, nextBoxWithTab, args=(previous,)).start()
    elif key == Key.right and current < len(boxes) - 1:
        current = current + 1
        threading.Timer(0.05, nextBox).start()   # wait a moment so the arrow reaches the app first
    elif key == Key.space:
        threading.Timer(0.05, finish).start()
    elif key == Key.backspace:
        boxes[current] = boxes[current][:-1]
    elif getattr(key, "char", None) is not None:
        boxes[current] = boxes[current] + key.char
    return True


def isTabPending():
    return tabPending


def clearTabPending():
    global tabPending
    tabPending = False