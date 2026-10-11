templates = {
    "//frac": "□/□",
    "//pow": "□^□",
    "//log": "log_□(□)",
    "//cbrt": "∛(□)",
    "//ln": "ln(□)",
    "//sin": "sin(□)",
    "//cos": "cos(□)",
    "//tan": "tan(□)",
    "//arcsin": "arcsin(□)",
    "//arccos": "arccos(□)",
    "//arctan": "arctan(□)",
    "//sinh": "sinh(□)",
    "//cosh": "cosh(□)",
    "//tanh": "tanh(□)",
    "//cot": "cot(□)",
    "//sec": "sec(□)",
    "//csc": "csc(□)",
    "//_": "□"
}

superscripts = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ",
    "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ⁱ", "j": "ʲ",
    "k": "ᵏ", "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ",
    "p": "ᵖ", "r": "ʳ", "s": "ˢ", "t": "ᵗ", "u": "ᵘ",
    "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ",
    "+": "⁺", "-": "⁻", "=": "⁼",
    "(": "⁽", ")": "⁾"
}

subscripts = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
    "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
    "a": "ₐ", "e": "ₑ", "h": "ₕ", "i": "ᵢ", "j": "ⱼ",
    "k": "ₖ", "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ",
    "p": "ₚ", "r": "ᵣ", "s": "ₛ", "t": "ₜ", "u": "ᵤ",
    "v": "ᵥ", "x": "ₓ",
    "+": "₊", "-": "₋", "=": "₌",
    "(": "₍", ")": "₎"}


def small(number, table):
    result = ""
    for digit in number:
        result = result + table[digit]
    return result


def finalText(name, boxes):
    if name == "//frac":
        return "(" + boxes[0] + ")/(" + boxes[1] + ")"
    if name == "//pow" and all(c in superscripts for c in boxes[1]):
        return boxes[0] + small(boxes[1], superscripts)
    if name == "//log" and all(c in subscripts for c in boxes[0]):
        return "log" + small(boxes[0], subscripts) + "(" + boxes[1] + ")"
    if name == "//_" and all(c in subscripts for c in boxes[0]):
        return small(boxes[0], subscripts)
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