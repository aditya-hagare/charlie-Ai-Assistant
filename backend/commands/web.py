import webbrowser

def handle_web(text):
    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    
    if "open chrome" in text:
        webbrowser.open("C:/Users/91935/OneDrive/Desktop/35 Aditya (35 Aditya hagare) - Chrome.lnk")
        return "Opening Chrome."
    
    if "open colab" in text:
        webbrowser.open("https://colab.research.google.com/#scrollTo=qwUcj3Acv5lr")
        return "Opening Google Colab."

    if "play music" in text:
        webbrowser.open("https://music.youtube.com")
        return "Opening Play Music."

    if "open github" in text:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    if "open linkedin" in text:
        webbrowser.open("https://linkedin.com")
        return "Opening LinkedIn."

    if "search google for" in text:
        query = text.replace("search google for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}."

    if "search youtube for" in text:
        query = text.replace("search youtube for", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Searching YouTube for {query}."
     
    if "chatgpt" in text:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT."
    
    return None
