import os
import subprocess
import webbrowser

def handle_files(text: str):
    text = text.lower()

    if "shutdown" in text:
        os.system("shutdown /s /t 1")
        return "Shutting down system."

    if "restart" in text:
        os.system("shutdown /r /t 1")
        return "Restarting system."

    if "lock system" in text:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking system."

    if "sleep system" in text:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting system to sleep."

    return None
