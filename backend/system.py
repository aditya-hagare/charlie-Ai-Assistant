import os
import datetime
import psutil

from backend.commands.confirm import set_pending


def handle_system(text: str):
    """
    Handles system-level commands.
    Returns a response string if matched, otherwise None.
    """
    text = text.lower()

    # ================= TIME & DATE =================
    if "what time is it" in text or "tell me the time" in text:
        now = datetime.datetime.now()
        return now.strftime("The time is %I:%M %p.")

    if "what is the date" in text or "today's date" in text:
        today = datetime.date.today()
        return today.strftime("Today is %B %d, %Y.")

    # ================= SYSTEM STATUS =================
    if "battery status" in text or "battery percentage" in text:
        battery = psutil.sensors_battery()
        if battery:
            return f"Battery level is {battery.percent} percent."
        return "I cannot read the battery status."

    if "cpu usage" in text:
        cpu = psutil.cpu_percent(interval=1)
        return f"Current CPU usage is {cpu} percent."

    if "ram usage" in text or "memory usage" in text:
        ram = psutil.virtual_memory().percent
        return f"Current memory usage is {ram} percent."

    # ================= SCREEN / SESSION =================
    if "lock computer" in text or "lock system" in text:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking the computer."

    # ================= SHUTDOWN / RESTART (CONFIRMATION) =================
    if "shutdown computer" in text or "shut down system" in text:
        set_pending("shutdown")
        return "Are you sure you want to shut down the computer? Say yes or no."

    if "restart computer" in text or "restart system" in text:
        set_pending("restart")
        return "Are you sure you want to restart the computer? Say yes or no."

    # ================= NO MATCH =================
    return None
