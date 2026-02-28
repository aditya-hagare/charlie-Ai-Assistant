
from groq import Groq
from Core.interrupt import is_interrupted, interrupt
import os

# Hardcode temporarily (or use env variable)
client = Groq(api_key=os.getenv("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"))


# ================= BASIC THINK =================
def think(text: str) -> str:
    lower = text.lower()

    if any(word in lower for word in ["stop", "wait", "cancel", "quiet"]):
        interrupt()
        return "Okay, stopping."

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Updated model
            messages=[
                {
                    "role": "system",
                    "content": "You are Charlie, a smart and professional AI assistant. Give structured and helpful answers."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=800
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Groq API Error: {str(e)}"



# ================= STREAMING THINK =================
def stream_think(text: str):
    lower = text.lower()

    if any(word in lower for word in ["stop", "wait", "cancel", "quiet"]):
        interrupt()
        yield "Okay, stopping."
        return

    try:
        stream = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Charlie, a smart, professional AI assistant. "
                        "Give clear and helpful answers."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=800,
            stream=True
        )

        for chunk in stream:
            if is_interrupted():
                return

            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"Groq API Error: {str(e)}"
