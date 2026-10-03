shortcuts = {
    # Greek lowercase
    "//alpha": "α",
    "//beta": "β",
    "//gamma": "γ",
    "//delta": "δ",
    "//epsilon": "ε",
    "//zeta": "ζ",
    "//eta": "η",
    "//theta": "θ",
    "//iota": "ι",
    "//kappa": "κ",
    "//lambda": "λ",
    "//mu": "μ",
    "//nu": "ν",
    "//xi": "ξ",
    "//pi": "π",
    "//rho": "ρ",
    "//sigma": "σ",
    "//tau": "τ",
    "//upsilon": "υ",
    "//phi": "φ",
    "//chi": "χ",
    "//psi": "ψ",
    "//omega": "ω",

    # Greek uppercase
    "//Gamma": "Γ",
    "//Delta": "Δ",
    "//Theta": "Θ",
    "//Lambda": "Λ",
    "//Xi": "Ξ",
    "//Pi": "Π",
    "//Sigma": "Σ",
    "//Phi": "Φ",
    "//Psi": "Ψ",
    "//Omega": "Ω",

    # Operators
    "//times": "×",
    "//div": "÷",
    "//pm": "±",
    "//mp": "∓",
    "//cdot": "·",
    "//sqrt": "√",
    "//sum": "∑",
    "//prod": "∏",
    "//int": "∫",
    "//oint": "∮",
    "//partial": "∂",
    "//nabla": "∇",
    "//infty": "∞",

    # Relations
    "//neq": "≠",
    "//leq": "≤",
    "//geq": "≥",
    "//approx": "≈",
    "//equiv": "≡",
    "//sim": "∼",
    "//propto": "∝",

    # Arrows
    "//rightarrow": "→",
    "//leftarrow": "←",
    "//leftrightarrow": "↔",
    "//Rightarrow": "⇒",
    "//Leftarrow": "⇐",
    "//Leftrightarrow": "⇔",
    "//uparrow": "↑",
    "//downarrow": "↓",
    "//mapsto": "↦",

    # Sets
    "//in": "∈",
    "//notin": "∉",
    "//subset": "⊂",
    "//supset": "⊃",
    "//subseteq": "⊆",
    "//supseteq": "⊇",
    "//cup": "∪",
    "//cap": "∩",
    "//emptyset": "∅",
    "//naturals": "ℕ",
    "//integers": "ℤ",
    "//rationals": "ℚ",
    "//reals": "ℝ",
    "//complex": "ℂ",

    # Logic
    "//forall": "∀",
    "//exists": "∃",
    "//neg": "¬",
    "//land": "∧",
    "//lor": "∨",
    "//therefore": "∴",
    "//because": "∵",

    # Misc
    "//degree": "°",
    "//angle": "∠",
    "//perp": "⊥",
    "//parallel": "∥",
    "//hbar": "ℏ",
    "//ell": "ℓ",
}


def isShortcut(word):
    #return true if word from returnWord() is exactly one of the shortcuts.
    return word in shortcuts


def getShortcutName(word):
    #return the matching key from the shortcuts dictionary, or None if it isn't one.
    for key in shortcuts:
        if key == word:
            return key
    return None


def getSymbol(key):
    #return the Unicode symbol for a shortcut, e.g. "//alpha" -> "α"
    return shortcuts[key]


def findShortcut(text, allowAmbiguous=False):
    matches = []
    for shortcut in shortcuts:
        start = text.find(shortcut)
        while start != -1:
            matches.append((start, shortcut))
            start = text.find(shortcut, start + 1)

    matches.sort(key=lambda match: (match[0], -len(match[1])))
    for start, shortcut in matches:
        typedTail = text[start:]
        if not allowAmbiguous and any(
            len(candidate) > len(typedTail) and candidate.startswith(typedTail)
            for candidate in shortcuts
        ):
            continue
        return shortcut, start, start + len(shortcut)
    return None


if __name__ == "__main__":
    #self test
    testWords = ["//alpha", "//Omega", "//reals", "//nope", "alpha", "//ALPHA"]
    for word in testWords:
        if isShortcut(word):
            print(word, "is a shortcut for", getSymbol(word))
        else:
            print(word, "is not a shortcut")