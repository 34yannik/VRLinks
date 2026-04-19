import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow


LOCK_FILE = os.path.join(os.environ.get("APPDATA"), "VRLinks", "app.lock")


def resource_path(relative_path: str) -> str:
    """Gibt den korrekten Pfad zurück – sowohl im Dev-Modus als auch als EXE."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def is_process_running(pid: int) -> bool:
    try:
        output = subprocess.check_output(
            ["tasklist", "/FI", f"PID eq {pid}"],
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode()
        return str(pid) in output
    except:
        return False


def already_running():
    if not os.path.exists(LOCK_FILE):
        return False

    try:
        with open(LOCK_FILE, "r") as f:
            pid = int(f.read().strip())

        if is_process_running(pid):
            return True

    except:
        pass

    try:
        os.remove(LOCK_FILE)
    except:
        pass

    return False


def create_lock():
    os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def remove_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass


def main():

    if already_running():
        print("App läuft bereits!")
        sys.exit(0)

    create_lock()

    app = QApplication(sys.argv)
    app.setApplicationName("VR Links")
    app.setOrganizationName("VRLinks")

    icon_path = resource_path(os.path.join("resources", "icon.ico"))
    icon = QIcon(icon_path)

    app.setWindowIcon(icon)

    window = MainWindow()
    window.setWindowIcon(icon)
    window.show()

    try:
        sys.exit(app.exec())
    finally:
        remove_lock()


if __name__ == "__main__":
    main()