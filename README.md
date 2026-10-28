# UniFlow

UniFlow is a lightweight global keyboard shortcut expander for math, physics, and science writing. Type shorthand like `//pi`, `//theta`, or `//int`, and UniFlow replaces it instantly with clean, universal Unicode symbols and formatted math expressions.

This project is designed for students, researchers, and anyone who types math frequently and wants a faster way to write equations without leaving the keyboard.

## Design Philosophy: Why Pure Unicode Instead of LaTeX?

A deliberate, core architectural decision of UniFlow is to focus exclusively on standard Unicode math notation rather than generating LaTeX syntax:

- **LaTeX tools already have LaTeX**: Modern technical writing environments (Overleaf, Obsidian, Typst, MS Word Equation Editor, Notion math blocks) already feature native LaTeX input and autocomplete.
- **Everywhere else lacks math tools**: In Google Docs, Discord, Slack, emails, GitHub issues, Jupyter notebook comments, code docstrings, and browser text fields, there is no built-in math compiler.
- **Universal portability**: Unicode symbols are standard characters. Expressions typed with UniFlow can be copied, pasted, and rendered anywhere on any operating system, phone, or browser without needing MathJax, KaTeX, or a TeX distribution.

## What UniFlow does

UniFlow listens for your keystrokes globally and watches for known shortcuts. When it sees a match, it:

- deletes the typed shortcut text
- inserts the symbolic replacement
- keeps your cursor in a usable position

Examples:

- `//pi` → `π`
- `//theta` → `θ`
- `//int` → an interactive integral template (with sub/superscript limits)
- `//sum` → `∑`
- `//frac` → an interactive fraction template

The project supports both direct symbol replacement and interactive math templates for common notation.

## Why this is useful

If you write a lot of math, you probably know the pain of:

- typing out verbose names like `theta`, `times`, or `sqrt`
- hunting for Greek letters in symbol pickers or copy-pasting from Wikipedia
- trying to format fractions, exponents, or integrals in messaging apps, Google Docs, or forum posts

UniFlow makes that much faster by turning a short typed sequence into proper math notation instantly.

## Supported shortcut examples

Core math shortcuts:

- `//alpha` → `α`
- `//beta` → `β`
- `//pi` → `π`
- `//theta` → `θ`
- `//int` → `∫`
- `//sum` → `∑`
- `//prod` → `∏`
- `//sqrt` → `√`
- `//infty` → `∞`
- `//to` → `→`
- `//deg` → `°`

Interactive templates:

- `//frac` → fraction template
- `//pow` → power/superscript template
- `//_` → subscript template
- `//int`, `//oint`, `//iint`, `//iiint` → integral templates (subscript lower limit, superscript upper limit)
- `//sin`, `//cos`, `//tan`, `//ln` → function templates
- `//ddx`, `//ddt` → derivative templates

## How it works

At a high level, UniFlow does this:

1. Captures keyboard input globally.
2. Keeps a small rolling buffer of recent keys.
3. Checks the latest text against a dictionary of known shortcuts.
4. If a shortcut matches, it removes the typed text and inserts the replacement.
5. For templates, it creates an interactive editing flow using the keyboard.

This approach works especially well for fast math typing in text fields and editors.

## Installation

### Option 1: Install from the repo directly

Clone the repo and install dependencies:

```bash
git clone https://github.com/krazybaboon17/UniFlow.git
cd UniFlow
python3 -m pip install -r requirements.txt
```

Then run:

```bash
python3 runner.py
```

You will be prompted with:

```text
Enter 0 for Settings, Enter 1 for Start:
```

Choose:

- `1` to start UniFlow
- `0` to open the settings menu and add custom shortcuts

### Option 2: Install as a command

From the repo root:

```bash
python3 -m pip install -e .
```

After that, you can run:

```bash
uniflow
```

### Option 3: Install script

There is also an install script in the repo:

```bash
bash install.sh
```

This copies the installed binary to `/usr/local/bin` and allows it to be run from anywhere.

## First-time usage

When the app starts:

1. Run `python3 runner.py` or `uniflow`
2. Press `1` to start
3. Begin typing a shortcut like `//pi`
4. When the shortcut is detected, it will be replaced automatically
5. Press `Esc` to pause or resume the app
6. Press `Esc` while a template is active to cancel it

Example:

```text
Type: //pi
Result: π
```

## Pausing and resuming

UniFlow can be paused with the `Esc` key.

- Press `Esc` once to pause
- Press `Esc` again to resume
- If a math template is active, `Esc` cancels the active template flow

This is useful when you want to type normal text without triggering shortcuts.

## Adding custom shortcuts

At startup, choose `0` for Settings.

From there, you can add your own shortcut mappings in the form:

```text
shortcut : value
```

Example:

```text
//dx : dx
//vec : v⃗
//ff : f(x)
```

Custom shortcuts are saved and loaded automatically.

## Interactive math templates

Some shortcuts trigger a guided template flow instead of a direct replacement.

Examples:

- `//int` → creates an interactive integral template with lower and upper limit boxes
- `//oint` → contour line integral template
- `//iint`, `//iiint` → double and triple integral templates
- `//frac` → creates a fraction template `(numerator)/(denominator)`
- `//pow` → creates a power/superscript template (e.g. `x//pow` -> `x²`)
- `//_` → creates a subscript template (e.g. `x//_` -> `x₁`)
- `//log` → logarithm template with custom base `log_b(x)`
- `//sin`, `//cos`, `//tan`, `//ln` → function templates with parenthesized arguments
- `//ddx`, `//ddt`, `//ddy` → derivative templates

### How to use Interactive Templates Step-by-Step

1. **Trigger the template**: Type the shortcut anywhere (e.g., type `//int` or `//frac`). UniFlow automatically replaces the shortcut with the placeholder structure (e.g. `∫_□^□` or `(□)/(□)`) and selects the first placeholder box `□`.
2. **Type into the highlighted box**: Since the box `□` is automatically selected, simply type your content. For example, in `//int`, type `0` to set the lower limit: `∫_0^□`.
3. **Navigate to the next box**: Press **`Tab`** or the **Right Arrow `→`**. UniFlow will automatically advance to the second box `□` and highlight it for you.
4. **Type the next limit / argument**: Type your content for the second box (e.g. `1` or `b` or `//infty` / `//inf` → `∞`).
5. **Finish and expand**: 
   - Press **`Enter`** at any time to immediately finalize the expression.
   - Alternatively, press **`Tab`** or **`→`** from the last box, or press **`Space`** to complete it.
   - UniFlow automatically formats the limits into clean Unicode superscripts/subscripts (e.g. `∫₀¹` or `∫ₐᵇ`).
6. **Cancel anytime**: If you want to abort the template, press **`Esc`**.

## Common examples

### Greek letters

```text
//alpha  -> α
//beta   -> β
//gamma  -> γ
//theta  -> θ
//pi     -> π
//lambda -> λ
//sigma  -> σ
//omega  -> ω
//Delta  -> Δ
//Omega  -> Ω
``` 

### Calculus & Operations

```text
//int    -> ∫_□^□ (template: formats to ∫₀¹ or ∫ₐᵇ)
//iint   -> ∬_□^□ (double integral template)
//iiint  -> ∭_□^□ (triple integral template)
//oint   -> ∮_□^□ (contour line integral template)
//ddx    -> d/dx(□) (derivative template)
//ddt    -> d/dt(□) (time derivative template)
//dydx   -> dy/dx
//dydt   -> dy/dt
//sum    -> ∑
//prod   -> ∏
//sqrt   -> √
//cbrt   -> ∛(□)
//partial-> ∂
//nabla  -> ∇
//infty  -> ∞
//inf    -> ∞
//deg    -> °
//pm     -> ±
//mp     -> ∓
``` 

### Relations, Arrows & Sets

```text
//to     -> →
//approx -> ≈
//leq    -> ≤
//geq    -> ≥
//neq    -> ≠
//belong -> ∈
//notin  -> ∉
//subset -> ⊂
//supset -> ⊃
//cup    -> ∪
//cap    -> ∩
//Z      -> ℤ (integers)
//reals  -> ℝ
//naturals-> ℕ
//complex-> ℂ
``` 

## Requirements and permissions

### macOS

If global keyboard monitoring or injection does not work, macOS may require permission for:

- Accessibility
- Input Monitoring

You may need to allow your terminal or Python environment to listen to keyboard input and simulate key presses.

### Windows

Windows may require appropriate permissions depending on how the keyboard hook or input injection is handled. If the app is blocked, try running the terminal or app with the appropriate privileges.

## Troubleshooting

### The app is not detecting shortcuts

Check that:

- UniFlow is actually running
- the app is not paused (`Esc` toggles pause)
- the shortcut you typed matches the dictionary exactly
- the text field accepts normal keyboard input

### It replaces text unexpectedly

This is a known limitation of global keyboard listeners. If your shortcut triggers in text you did not intend, pause UniFlow or use `Esc` to cancel the current session.

### It does not work in certain apps

Some apps restrict global keyboard input or use custom input systems. UniFlow works best in standard text fields and browser text areas, but may behave differently in specialized environments.

### Custom shortcuts are not loading

The app reads from the custom shortcuts file, which is stored in the user home directory or the project directory depending on runtime setup. You can add them through the settings menu, or create/edit the file manually in the expected location.

## Repo structure

The project contains:

- `runner.py` — main app loop
- `keyboardInput.py` — keyboard listener and text buffer
- `shortcutDetection.py` — shortcut matching logic
- `mathShortcuts.py` — template definitions and expansions
- `mathTyping.py` — interactive template editor
- `customShortcuts.txt` — user-defined shortcut mappings
- `install.sh` — install helper script
- `setup.py` — package/install metadata

## Development notes

This project is intentionally small and focused. It is most useful as a terminal-based productivity tool for writing math quickly.

Potential areas for future improvement include:

- a cleaner desktop UI
- better app-level settings
- more discoverability for shortcuts
- better cross-app compatibility
- more safety checks for accidental triggers

## License

This project is distributed under the repository's existing licensing terms.

