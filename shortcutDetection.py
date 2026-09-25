import keyboardInput
# Shortcut table: key is what the user types, value is the Unicode symbol.
# Names follow LaTeX command names so they're easy to remember.
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
    return shortcuts[key]
