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


def findTemplate(text, otherShortcuts=(), allowAmbiguous=False):
    names = tuple(templates) + tuple(otherShortcuts)
    matches = []
    for template in templates:
        start = text.find(template)
        while start != -1:
            matches.append((start, template))
            start = text.find(template, start + 1)

    matches.sort(key=lambda match: (match[0], -len(match[1])))
    for start, template in matches:
        typedTail = text[start:]
        if not allowAmbiguous and any(
            len(candidate) > len(typedTail) and candidate.startswith(typedTail)
            for candidate in names
        ):
            continue
        return template, start, start + len(template)
    return None