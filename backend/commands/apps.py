import subprocess
import os

def handle_apps(text: str):
    text = text.lower().strip()

    if not text.startswith("open"):
        return None

    app_name = text.replace("open", "").strip()

    # Built-in Windows apps
    known_apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "file manager": "explorer",
        "explorer": "explorer",
        "cmd": "cmd",
        "whatsapp": r"C:\\Users\%USERNAME%\AppData\\Local\\WhatsApp\\WhatsApp.exe"
    }
    # Open Chrome
    if "open chrome" in text:
        subprocess.Popen("start chrome", shell=True)
        return "Opening Chrome."

    # Open VS Code
    if "open vs code" in text or "open vscode" in text:
        vscode_path = r"C:\Users\91935\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
        subprocess.Popen("vscode_path")
        return "Opening VS Code."
    
    if app_name in known_apps:
        try:
            subprocess.Popen(known_apps[app_name])
            return f"Opening {app_name}."
        except Exception as e:
            return f"Could not open {app_name}."

    return None
