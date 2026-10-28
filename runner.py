import keyboardInput
import time
import shortcutDetection
import deletingShortcut
import writingValue
import mathShortcuts
import mathTyping
from pynput import keyboard

import sys
import os
import signal
import ipc

def main():
    if "--widget" in sys.argv:
        import widget
        parent_pid = None
        if "--parent-pid" in sys.argv:
            try:
                idx = sys.argv.index("--parent-pid")
                parent_pid = int(sys.argv[idx + 1])
            except Exception:
                pass
        widget.run_standalone(parent_pid=parent_pid)
        return

    userChoice = input("Enter 0 for Settings, Enter 1 for Start: ")
    while (userChoice != "0" and userChoice != "1"):
        print("Invalid input")
        userChoice = input("Enter 0 for Settings, Enter 1 for Start: ")

    if userChoice == "0":
        print("\n--- Settings ---")
        print("UniFlow is dedicated to universal Unicode math symbols and interactive templates.")
        print("Note: LaTeX is intentionally omitted—modern LaTeX editors have native support,")
        print("while UniFlow brings portable math to any app, browser, or editor without a compiler.\n")
        
        while True:
            choice = input("Enter [1] to add shortcut, [2] to view custom shortcuts, or [0] to finish settings: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                key = input("Enter shortcut (e.g. //hbar): ").strip()
                value = input("Enter replacement symbol (e.g. ℏ): ").strip()
                if key and value:
                    shortcutsFile = shortcutDetection.getShortcutsPath()
                    with open(shortcutsFile, "a", encoding="utf-8") as f:
                        f.write(f"{key} : {value}\n")
                    shortcutDetection.shortcuts[key] = value
                    print(f"Shortcut added: {key} -> {value}\n")
                else:
                    print("Shortcut and value cannot be empty.\n")
            elif choice == "2":
                shortcutsFile = shortcutDetection.getShortcutsPath()
                print(f"\nCustom shortcuts from {shortcutsFile}:")
                try:
                    with open(shortcutsFile, "r", encoding="utf-8") as f:
                        lines = [l.strip() for l in f if l.strip()]
                        if lines:
                            for l in lines:
                                print(f"  {l}")
                        else:
                            print("  (No custom shortcuts found)")
                except Exception as e:
                    print(f"  (Could not read shortcuts: {e})")
                print()
            else:
                print("Invalid input. Please enter 0, 1, or 2.\n")

        user = input("Start UniFlow now? (y/n): ").strip().lower()
        while user not in ("y", "n"):
            print("Invalid input")
            user = input("Start UniFlow now? (y/n): ").strip().lower()
        if user == "y":
            userChoice = "1"
        else:
            return
    if userChoice == "1":
        runner_pid = os.getpid()
        ipc.init_session(runner_pid=runner_pid, paused=False)

        listener = None

        def sigusr1_handler(signum, frame):
            keyboardInput.toggle_pause(from_source="widget")

        def sigterm_handler(signum, frame):
            print("\n[UniFlow] Quit requested from widget. Exiting...")
            if listener:
                try:
                    listener.stop()
                except Exception:
                    pass
            ipc.cleanup()
            os._exit(0)

        if hasattr(signal, "SIGUSR1"):
            try:
                signal.signal(signal.SIGUSR1, sigusr1_handler)
            except Exception:
                pass
        if hasattr(signal, "SIGTERM"):
            try:
                signal.signal(signal.SIGTERM, sigterm_handler)
            except Exception:
                pass

        try:
            import widget
            widget.launch_overlay(parent_pid=runner_pid)
        except Exception:
            pass
        shortcutDetection.loadShortcuts()
        keyboardInput.charList.clear()
        keyboardInput.cursorPosition = 0
        listener = keyboardInput.startListener()

        print("UniFlow is running in the background. Press Esc to pause.")
        print("\n")

        lastWord = ""
        pendingWord = None
        pendingSince = None
        try:
            while listener.is_alive():
                # Process any pending command from widget
                cmd_data = ipc.pop_command()
                if cmd_data:
                    cmd = cmd_data.get("cmd")
                    if cmd == "quit":
                        print("\n[UniFlow] Quit requested from widget. Exiting...")
                        try:
                            listener.stop()
                        except Exception:
                            pass
                        ipc.cleanup()
                        os._exit(0)
                    elif cmd == "toggle_pause":
                        keyboardInput.toggle_pause(from_source="widget")
                    elif cmd == "pause":
                        keyboardInput.set_paused_state(True, from_source="widget")
                    elif cmd == "resume":
                        keyboardInput.set_paused_state(False, from_source="widget")

                if keyboardInput.paused:
                    time.sleep(0.05)
                    continue

                if mathTyping.isActive():
                    time.sleep(0.05)
                    continue

            word = keyboardInput.returnWord()
            if word != lastWord:
                lastWord = word

            match = shortcutDetection.findShortcut(word, otherShortcuts=mathShortcuts.templates)
            templateMatch = None
            if match is None:
                templateMatch = mathShortcuts.findTemplate(word, shortcutDetection.shortcuts)

            pendingMatch = None
            pendingTemplate = False
            if match is None and templateMatch is None:
                pendingMatch = shortcutDetection.findShortcut(
                    word, otherShortcuts=mathShortcuts.templates, allowAmbiguous=True
                )
                if pendingMatch is None:
                    pendingMatch = mathShortcuts.findTemplate(
                        word, shortcutDetection.shortcuts, allowAmbiguous=True
                    )
                    pendingTemplate = pendingMatch is not None

            if pendingMatch is None:
                pendingWord = None
                pendingSince = None
            elif word != pendingWord:
                pendingWord = word
                pendingSince = time.monotonic()
            elif time.monotonic() - pendingSince >= 0.4:
                if pendingTemplate:
                    templateMatch = pendingMatch
                else:
                    match = pendingMatch
                pendingWord = None
                pendingSince = None

            if match is not None:
                shortcut, start, end = match
                suffix = word[end:]
                symbol = shortcutDetection.getSymbol(shortcut)
                print(shortcut, "is a shortcut for", symbol)
                deletingShortcut.deleteShortcut(shortcut + suffix)
                writingValue.writeValue(symbol + suffix)
                keyboardInput.setWord(suffix)

            elif templateMatch is not None:
                template, start, end = templateMatch
                prefix = word[:start]
                suffix = word[end:]
                print(template, "is a math template")
                if (template == "//pow" or template == "//_") and prefix:
                    deletingShortcut.deleteShortcut(template + suffix)
                    keyboardInput.setWord(suffix)
                    mathTyping.start(template, suffix, prefix=prefix)
                else:
                    deletingShortcut.deleteShortcut(template + suffix)
                    keyboardInput.setWord(suffix)
                    mathTyping.start(template, suffix)

            time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n[UniFlow] Interrupted by user. Exiting...")
        finally:
            print("[UniFlow] Stopping listener and cleaning up...")
            if listener:
                try:
                    listener.stop()
                except Exception:
                    pass
            ipc.cleanup()

if __name__ == "__main__":
    main()