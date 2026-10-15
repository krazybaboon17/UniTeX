import threading
import time
from pynput.keyboard import Key, Controller
import mathShortcuts
import shortcutDetection

keyboard = Controller()

class TemplateState:
    def __init__(self, name, pattern, trailing="", prefix=""):
        self.name = name
        self.pattern = pattern
        self.pieces = pattern.split("□")
        self.boxes = [""] * pattern.count("□")
        self.current = 0
        self.trailingText = trailing
        self.fractionWrapped = False
        self.prefix = prefix

templateStack = []
busy = False

def isActive():
    return len(templateStack) > 0

def cancel():
    global busy, templateStack
    busy = False
    templateStack.clear()

def press(key, times=1):
    for _ in range(times):
        keyboard.press(key)
        keyboard.release(key)

def selectBox(arrow):
    # Shift + arrow highlights the □, so what the user types replaces it
    keyboard.press(Key.shift)
    press(arrow)
    keyboard.release(Key.shift)

def start(shortcut, trailing="", prefix=""):
    global busy
    busy = True
    pattern = mathShortcuts.templates[shortcut]
    state = TemplateState(shortcut, pattern, trailing=trailing, prefix=prefix)
    if prefix and shortcut == "//pow":
        state.boxes[0] = prefix
        state.current = 1
        keyboard.type("^□" + trailing)
        if trailing:
            press(Key.left, len(trailing) + 1)
            selectBox(Key.right)
        else:
            selectBox(Key.left)
    else:
        keyboard.type(pattern + trailing)
        press(Key.left, len(trailing) + len(pattern) - pattern.index("□") - 1)
        selectBox(Key.left)
    time.sleep(0.05)
    busy = False
    templateStack.append(state)

def startNested(shortcut, prefix=""):
    start(shortcut, trailing="", prefix=prefix)

def nextBox(previous):
    global busy
    if not templateStack:
        return
    busy = True
    state = templateStack[-1]
    
    # Expand any pending ambiguous shortcuts in the box we are leaving
    old_box = state.boxes[previous]
    new_box = expandShortcuts(old_box)
    if new_box != old_box:
        press(Key.backspace, len(old_box))
        keyboard.type(new_box)
        state.boxes[previous] = new_box

    pieces = state.pieces
    if state.name == "//frac" and previous == 0:
        press(Key.left, len(pieces[previous + 1]))
        if state.boxes[previous]:
            keyboard.type(")")
            press(Key.left, len(state.boxes[previous]) + 1)
            keyboard.type("(")
            press(Key.right, len(state.boxes[previous]) + 2)
        else:
            keyboard.type("()")
            press(Key.right)
        state.fractionWrapped = True
    else:
        sep_len = len(pieces[previous + 1])
        if sep_len > 0:
            press(Key.right, sep_len)
    selectBox(Key.right)
    time.sleep(0.05)
    busy = False

def expandShortcuts(text):
    while True:
        match = shortcutDetection.findShortcut(text, allowAmbiguous=True)
        if match is None:
            return text
        shortcut, start, end = match
        text = text[:start] + shortcutDetection.getSymbol(shortcut) + text[end:]

def finish(via_space=False):
    global busy
    if not templateStack:
        return
    busy = True
    state = templateStack[-1]
    pieces = state.pieces

    before = 1 if via_space else 0
    if state.prefix and state.name == "//pow":
        before += len(state.prefix) + 1
        before += len(state.boxes[1]) if len(state.boxes) > 1 else 0
    else:
        for i in range(state.current + 1):
            before += len(pieces[i]) + len(state.boxes[i])
        if state.name == "//frac" and state.fractionWrapped:
            before += 2

    after = len(state.trailingText)
    for i in range(state.current + 1, len(pieces)):
        after += len(pieces[i])
        if i < len(state.boxes):
            after += (len(state.boxes[i]) if state.boxes[i] else 1)

    press(Key.backspace, before)
    if after > 0:
        press(Key.delete, after)

    expandedBoxes = [expandShortcuts(b) for b in state.boxes]
    final = mathShortcuts.finalText(state.name, expandedBoxes)

    templateStack.pop()

    if templateStack:
        parent = templateStack[-1]
        keyboard.type(final)
        parent.boxes[parent.current] += final
        time.sleep(0.05)
        busy = False
    else:
        keyboard.type(final + state.trailingText + " ")
        time.sleep(0.05)
        busy = False

def handleKey(key):
    global busy
    if busy:
        return True
    if not templateStack:
        return False

    state = templateStack[-1]

    # Moving to next box
    if (key == Key.right or key == Key.tab) and state.current < len(state.boxes) - 1:
        previous = state.current
        state.current += 1
        threading.Timer(0.02, nextBox, args=(previous,)).start()
        return True

    # Finishing at the last box
    if (key == Key.right or key == Key.tab) and state.current == len(state.boxes) - 1:
        threading.Timer(0.02, finish, kwargs={"via_space": False}).start()
        return True

    # Space key handling
    if key == Key.space:
        if state.current == len(state.boxes) - 1:
            threading.Timer(0.02, finish, kwargs={"via_space": True}).start()
        else:
            state.boxes[state.current] += " "
        return True

    # Enter finishes current template
    if key == Key.enter:
        threading.Timer(0.02, finish, kwargs={"via_space": False}).start()
        return True

    # Backspace inside box
    if key == Key.backspace:
        if state.boxes[state.current]:
            state.boxes[state.current] = state.boxes[state.current][:-1]
        return True

    char = getattr(key, "char", None)
    if char is not None:
        state.boxes[state.current] += char

        # 1. Check if current box just typed a shortcut (e.g. //pi, //to, //sqrt, //deg, etc.)
        match = shortcutDetection.findShortcut(state.boxes[state.current], allowAmbiguous=False)
        if match is not None:
            shortcut, s_idx, e_idx = match
            if e_idx == len(state.boxes[state.current]):
                symbol = shortcutDetection.getSymbol(shortcut)
                busy = True
                press(Key.backspace, len(shortcut))
                keyboard.type(symbol)
                time.sleep(0.02)
                busy = False
                state.boxes[state.current] = state.boxes[state.current][:s_idx] + symbol
                return True

        # 2. Check if current box just typed a nested template (e.g. //frac, //pow, //sin, //lim)
        tmpl_match = mathShortcuts.findTemplate(state.boxes[state.current], shortcutDetection.shortcuts, allowAmbiguous=False)
        if tmpl_match is not None:
            tmpl, s_idx, e_idx = tmpl_match
            if e_idx == len(state.boxes[state.current]):
                prefix_in_box = state.boxes[state.current][:s_idx]
                busy = True
                press(Key.backspace, len(tmpl))
                time.sleep(0.02)
                busy = False
                if tmpl == "//pow" and prefix_in_box:
                    state.boxes[state.current] = ""
                    threading.Timer(0.02, startNested, args=(tmpl,), kwargs={"prefix": prefix_in_box}).start()
                else:
                    state.boxes[state.current] = prefix_in_box
                    threading.Timer(0.02, startNested, args=(tmpl,)).start()
                return True

    return True