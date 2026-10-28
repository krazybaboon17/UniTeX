"""
ipc.py - UniFlow Inter-Process Communication & Session Manager
Synchronizes state (Pause/Resume, Quit, Process Lifecycle) between
the background UniFlow runner process and the floating macOS widget overlay.
"""

import os
import sys
import json
import time
import signal

SESSION_DIR = os.path.expanduser("~/.uniflow")
SESSION_FILE = os.path.join(SESSION_DIR, "session.json")
COMMAND_FILE = os.path.join(SESSION_DIR, "command.json")


def ensure_dir():
    try:
        os.makedirs(SESSION_DIR, exist_ok=True)
    except Exception:
        pass


def is_process_alive(pid):
    if pid is None or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False


def kill_process(pid, sig=signal.SIGTERM):
    if pid is None or pid <= 0:
        return
    try:
        os.kill(pid, sig)
    except Exception:
        pass


def get_session():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def get_paused():
    session = get_session()
    if session and "paused" in session:
        return bool(session["paused"])
    return False


def init_session(runner_pid, paused=False):
    ensure_dir()
    # Check if a previous widget from an old session is still running and kill it
    old_session = get_session()
    if old_session and old_session.get("widget_pid"):
        old_widget_pid = old_session.get("widget_pid")
        if is_process_alive(old_widget_pid):
            kill_process(old_widget_pid, signal.SIGTERM)

    # Clean up old command file
    try:
        if os.path.exists(COMMAND_FILE):
            os.remove(COMMAND_FILE)
    except Exception:
        pass

    session_data = {
        "runner_pid": runner_pid,
        "widget_pid": None,
        "paused": paused,
        "updated": time.time(),
    }
    _atomic_write_json(SESSION_FILE, session_data)


def register_widget(widget_pid):
    ensure_dir()
    session = get_session() or {}
    session["widget_pid"] = widget_pid
    session["updated"] = time.time()
    _atomic_write_json(SESSION_FILE, session)


def set_paused(paused):
    ensure_dir()
    session = get_session() or {}
    session["paused"] = bool(paused)
    session["updated"] = time.time()
    _atomic_write_json(SESSION_FILE, session)


def send_command(cmd, runner_pid=None):
    """Send command from widget to runner process."""
    ensure_dir()
    cmd_data = {
        "cmd": cmd,
        "time": time.time(),
    }
    _atomic_write_json(COMMAND_FILE, cmd_data)

    target_pid = runner_pid
    if target_pid is None:
        session = get_session()
        if session:
            target_pid = session.get("runner_pid")

    if target_pid and is_process_alive(target_pid):
        try:
            if cmd in ("toggle_pause", "pause", "resume") and hasattr(signal, "SIGUSR1"):
                os.kill(target_pid, signal.SIGUSR1)
            elif cmd == "quit" and hasattr(signal, "SIGTERM"):
                os.kill(target_pid, signal.SIGTERM)
        except Exception:
            pass


def pop_command():
    """Read and remove pending command, if any."""
    if not os.path.exists(COMMAND_FILE):
        return None
    try:
        with open(COMMAND_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            os.remove(COMMAND_FILE)
        except Exception:
            pass
        return data
    except Exception:
        return None


def cleanup():
    """Remove session and command files upon shutdown."""
    for path in (COMMAND_FILE, SESSION_FILE):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass


def _atomic_write_json(path, data):
    tmp_path = path + f".tmp.{os.getpid()}"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp_path, path)
    except Exception:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

