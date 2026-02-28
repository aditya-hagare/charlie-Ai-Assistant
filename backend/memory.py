import json
import os

MEMORY_FILE = "C:/Users/91935/OneDrive/Desktop/Jarvis/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "user_name": "",
            "preferences": {},
            "facts": [],
            "history": []
        }
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def remember_fact(text):
    memory = load_memory()
    memory["facts"].append(text)
    save_memory(memory)

def set_user_name(name):
    memory = load_memory()
    memory["user_name"] = name
    save_memory(memory)

def add_history(user, assistant):
    memory = load_memory()
    memory["history"].append({
        "user": user,
        "assistant": assistant
    })

    # Keep history short (important)
    memory["history"] = memory["history"][-5:]
    save_memory(memory)
