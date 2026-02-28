from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.commands.apps import handle_apps
from backend.commands.web import handle_web
from backend.commands.files import handle_files
from backend.system import handle_system

from backend.tools.weather import get_weather
from backend.tools.news import get_news
from backend.tools.stocks import get_stock

from Core.Brain import think
from Core.text_to_speech import speak, stop_speaking
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ================= APP =================

app = FastAPI()

ui_path = resource_path("ui")

app.mount("/ui", StaticFiles(directory=ui_path), name="ui")

@app.get("/")
def root():
    return FileResponse(os.path.join(ui_path, "index.html"))



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= TTS STATE =================

app.state.tts_enabled = True


# ================= COMMAND ROUTER =================

def route_command(text: str):
    text = text.lower()

    for handler in (
        handle_apps,
        handle_web,
        handle_files,
        handle_system,
        
    ):
        result = handler(text)
        if result:
            return result

    return None


# ================= API ENDPOINTS =================

@app.get("/api/weather")
def weather(city: str = "Pune"):
    return get_weather(city)


@app.get("/api/news")
def news(topic: str = "india"):
    return get_news(topic)


@app.get("/api/stocks")
def stocks():
    return get_stock()


# ================= TEXT COMMAND =================

class CommandRequest(BaseModel):
    text: str


@app.post("/command")
def command(req: CommandRequest):

    # Stop any current speech first
    stop_speaking()

    # Check system commands
    result = route_command(req.text)

    if result:
        response = result
    else:
        response = think(req.text)

    # Speak only if enabled
    if app.state.tts_enabled:
        speak(response)

    return {"response": response}


# ================= TOGGLE TTS =================

@app.post("/toggle-tts")
def toggle_tts():
    app.state.tts_enabled = not app.state.tts_enabled

    if not app.state.tts_enabled:
        stop_speaking()

    return {"tts_enabled": app.state.tts_enabled}
