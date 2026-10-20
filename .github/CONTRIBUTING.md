# Contributing to the Project

Thank you for your interest in contributing!

## Project Scope & Architectural Guidelines

### 1. Pure Unicode Focus (No LaTeX)
This project is **strictly focused on universal, portable Unicode text**. 

- **Do NOT open issues or PRs proposing LaTeX output**: Modern document processors (Overleaf, Obsidian, Typst, MS Word Equation Editor, Notion math blocks) already have built-in LaTeX environments. 
- **Universal compatibility**: Our mission is to allow users to type real Unicode math symbols in text areas where LaTeX is not supported—such as Google Docs, Discord, Slack, email, GitHub comments, and browser inputs—without requiring a TeX distribution or rendering engine.

### 2. Lightweight & Fast
- Keystroke latency must remain negligible (< 10ms).
- Avoid heavy runtime dependencies (e.g. GUI frameworks or complex daemon services).
- Keep shortcuts intuitive and standardized according to standard mathematical and physical conventions.

### 3. Adding New Unicode Symbols
To propose new mathematical, scientific, or Greek shortcuts:
1. Ensure the symbol exists in the Unicode standard and has broad font support across Windows, macOS, and Linux.
2. Follow the double-slash prefix convention (`//symbol_name`).
3. Add the mapping to `shortcutDetection.py`.
