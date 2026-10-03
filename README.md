# UniTeX

## Overview
UniTeX is a keyboard shortcut expander for math/physics writing. Type shortcuts like `//pi` and it automatically replaces them with the correct output in either **Unicode** (e.g., `π`) or **LaTeX text** mode (e.g., `\pi`).

## What it does
- Listens for your typing globally
- Detects when you’ve typed a known shortcut
- Deletes the shortcut you typed
- Inserts the mapped replacement:
  - **Unicode mode**: math symbols (e.g., `π`, `θ`, `∫`)
  - **LaTeX mode**: LaTeX strings (e.g., `\pi`, `\theta`, `\int`)
- Avoids repeat-trigger loops while injecting replacements

## Key Features
- Global shorthand detection
- Unicode ↔ LaTeX output modes
- Extensible shortcut mapping table
- Safer injection behavior (guard during replacement)
- Designed to work across common text input apps

## Supported Shortcuts
> Add your real mappings here (example format):

- `//pi` → Unicode: `π` | LaTeX: `\pi`
- `//theta` → Unicode: `θ` | LaTeX: `\theta`
- `//int` → Unicode: `∫` | LaTeX: `\int`
- `//sqrt` → Unicode: `√` | LaTeX: `\sqrt`

## How it works (high level)
1. Capture typed keystrokes (global listener)
2. Maintain a short rolling buffer of recent characters
3. When the buffer ends with a known shortcut:
   - delete back `N` characters (N = shortcut length)
   - insert the replacement text for the current mode

## Mode control
- **Unicode mode**: inserts symbols directly
- **LaTeX mode**: inserts LaTeX strings
- (If you have a toggle hotkey, document it here.)

## Installation
> Update this with your repo’s exact steps.

1. Clone the repo
2. Install dependencies
3. Run the app
4. Grant required permissions (especially on macOS)

## Requirements / Permissions
- **macOS**: may require Accessibility/Input permissions for global input monitoring + injection
- **Windows**: may require appropriate permissions depending on the injection approach

## Usage
1. Start UniTeX
2. Type a shortcut like `//pi`
3. Watch it replace instantly with:
   - Unicode: `π` (Unicode mode)
   - LaTeX: `\pi` (LaTeX mode)

## Development / Contributing
Contributions welcome:
- Add new shortcuts
- Improve injection reliability (timing/backspace behavior)
- Improve mode switching UX
- Add more target-app support

## License
> Add your license here (MIT/Apache/etc.)
