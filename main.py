import sys
import win32event
import win32api
import win32gui
import win32con
import winerror

from poppy.app import App

APP_MUTEX_HANDLE: int | None = None

def is_already_running():
    global APP_MUTEX_HANDLE
    mutex_name = "Global\\PoppyMutex"
    mutex = win32event.CreateMutex(None, False, mutex_name)

    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        win32api.CloseHandle(mutex)
        return True

    APP_MUTEX_HANDLE = mutex
    return False

def show_already_running_message():
    from poppy.app_info import app_name
    win32gui.MessageBox(
        0,
        f"{app_name} is already running in the background.\nCheck the system tray.",
        "Already running",
        win32con.MB_ICONWARNING
    )

def cleanup_mutex():
    global APP_MUTEX_HANDLE
    if APP_MUTEX_HANDLE:
        try:
            win32api.CloseHandle(APP_MUTEX_HANDLE)
        except Exception:
            pass
        APP_MUTEX_HANDLE = None

if __name__ == "__main__":
    if is_already_running():
        show_already_running_message()
        sys.exit(1)

    app = App()

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
    finally:
        app.cleanup()
        cleanup_mutex()
        print("exit")
        # import os
        # os._exit(0)