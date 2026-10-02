templates = {
    "//frac": "□/□",
    "//pow": "□^□",
    "//log": "log_□(□)",
    "//cbrt": "∛(□)",
    "//ln": "ln(□)",
    "//sin": "sin(□)",
    "//cos": "cos(□)",
    "//tan": "tan(□)",
}

superscripts = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
                "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
subscripts = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
              "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}


def small(number, table):
    result = ""
    for digit in number:
        result = result + table[digit]
    return result


def finalText(name, boxes):
    if name == "//frac" and boxes[0].isdigit() and boxes[1].isdigit():
        return small(boxes[0], superscripts) + "⁄" + small(boxes[1], subscripts)
    if name == "//frac":
        return "(" + boxes[0] + ")/(" + boxes[1] + ")"
    if name == "//pow" and boxes[1].isdigit():
        return boxes[0] + small(boxes[1], superscripts)
    if name == "//log" and boxes[0].isdigit():
        return "log" + small(boxes[0], subscripts) + "(" + boxes[1] + ")"
    text = templates[name]
    for box in boxes:
        text = text.replace("□", box, 1)
    return text