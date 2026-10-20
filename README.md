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
- `//int` → `∫`
- `//sum` → `∑`
- `//frac` → an interactive fraction template
- `//lim` → a limit template

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
- `//lim` → limit template
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

- `//frac` → creates a fraction template
- `//pow` → creates a power template
- `//lim` → creates a limit template
- `//sin` → creates a sine template

Once a template is open:

- use `Tab` or Right Arrow to move to the next input box
- type into the highlighted box
- press `Enter` or move to the final box to finish
- press `Space` in the final field to complete the expression

This makes expressions like fractions, powers, and derivatives much easier to build without needing to type everything manually.

## Common examples

### Greek letters

```text
//alpha  -> α
//beta   -> β
//gamma  -> γ
//theta  -> θ
//pi     -> π
``` 

### Operations

```text
//sum    -> ∑
//prod   -> ∏
//int    -> ∫
//sqrt   -> √
//deg    -> °
//pm     -> ±
//neq    -> ≠
``` 

### Relations and arrows

```text
//to     -> →
//approx -> ≈
//leq    -> ≤
//geq    -> ≥
//in     -> ∈
//subset -> ⊂
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

## A note for demo / school presentation

This project is particularly strong as a demo for a CS audience because it combines:

- keyboard event handling
- text processing
- global input hooks
- UI/UX around productivity tools
- shortcut matching and state management
- interactive template flows

It is a good example of a focused, original tool that solves a real pain point for math-heavy users.

## Related landing page and setup guide

The companion landing page for UniFlow is intended to help users understand installation and setup. If you are using the website/chatbot flow for onboarding, the recommended structure is:

1. Explain the problem: typing math is slow
2. Show the shortcut examples
3. Tell users how to install the tool
4. Show how to run it from the terminal
5. Explain the `Esc` pause behavior
6. Provide a short list of useful shortcuts to start with
7. Offer a quick custom-shortcut example

That combination makes the project much easier to understand for new users.

---

If you want, I can also help with one of these next:

- tighten up the README for a more polished “product” tone
- add a screenshot-friendly quickstart section for the landing page
- draft a setup guide specifically for the school website/chatbot
- create a short install script for Windows/macOS users to make this easier to launch
