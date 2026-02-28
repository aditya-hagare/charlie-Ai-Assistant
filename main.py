import sys
import os
import threading
import webview
import pystray
from PIL import Image
import socket
import time
import logging
import uvicorn

from router import app
from Core.wake_word import wait_for_wake_word
from Core.text_to_speech import speak


# ================= SINGLE INSTANCE LOCK =================

LOCK_PORT = 65432
lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    lock_socket.bind(("127.0.0.1", LOCK_PORT))
except:
    sys.exit()  # Already running


# ================= LOGGING =================

logging.basicConfig(
    filename="charlie.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ================= RESOURCE PATH =================

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


ICON_PATH = resource_path("assets/icon.ico")

window = None
tray_icon = None
last_wake = 0


# ================= START FASTAPI BACKEND =================

def start_backend():
    try:
        logging.info("Starting FastAPI backend...")
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="warning"
        )
    except Exception as e:
        logging.error(f"Backend error: {e}")


# ================= WINDOW CONTROL =================

def show_window():
    try:
        if webview.windows:
            webview.windows[0].show()
            webview.windows[0].restore()
    except Exception as e:
        logging.error(f"Show window error: {e}")



def hide_window():
    if window:
        window.hide()


def exit_app(icon=None, item=None):
    if tray_icon:
        tray_icon.stop()
    os._exit(0)


# ================= SYSTEM TRAY =================

def create_tray():
    global tray_icon

    image = Image.open(ICON_PATH)

    menu = pystray.Menu(
        pystray.MenuItem("Open Charlie", lambda icon, item: show_window()),
        pystray.MenuItem("Exit", exit_app)
    )

    tray_icon = pystray.Icon("CharlieAI", image, "Charlie AI", menu)
    tray_icon.run()


# ================= WAKE WORD LISTENER =================

def wake_listener():
    global last_wake

    logging.info("Wake listener started")

    while True:
        try:
            wait_for_wake_word()
            logging.info("Wake word detected")

            now = time.time()
            if now - last_wake < 3:
                continue

            last_wake = now

            
            speak("Yes, I'm listening.")
            show_window()

        except Exception as e:
            logging.error(f"Wake error: {e}")
            time.sleep(2)


# ================= MAIN =================

if __name__ == "__main__":

    # 1️⃣ Start FastAPI backend
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Wait for backend to initialize
    time.sleep(3)

    # 2️⃣ Create window (VISIBLE on manual launch)
    window = webview.create_window(
        "Charlie AI",
        "http://127.0.0.1:8000",
        width=1100,
        height=700,
        hidden=False,
        resizable=True
    )

    # Override close → hide instead of exit
    def on_closing():
        hide_window()
        return False

    window.events.closing += on_closing

    # 3️⃣ Start wake listener
    threading.Thread(target=wake_listener, daemon=True).start()

    # 4️⃣ Start tray
    threading.Thread(target=create_tray, daemon=True).start()

    # 5️⃣ Start GUI loop (must be main thread)
    webview.start(gui="edgechromium")
