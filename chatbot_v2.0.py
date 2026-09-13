import os
import random
import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# -------------------------------------------------------------
# Configuration & Supported Languages
# -------------------------------------------------------------
SUPPORTED_LANGUAGES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'nl': 'Dutch', 'ru': 'Russian',
    'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic',
    'hi': 'Hindi', 'tr': 'Turkish', 'vi': 'Vietnamese', 'pl': 'Polish'
}

EXIT_COMMANDS = {'stop', 'quit', 'close', 'q', 'break', 'exit'}

class HeyrronChat2:
    def __init__(self, api_key: str, user_lang: str = 'en'):
        self.user_lang = user_lang if user_lang in SUPPORTED_LANGUAGES else 'en'
        self.lang_name = SUPPORTED_LANGUAGES[self.user_lang]
        
        # Audio setup
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        # Gemini 2.0 Client setup
        self.client = genai.Client(api_key= API_KEY)
        self.model_id = "gemini-3.5-flash"

        # Initialize multi-turn chat with persistent system instructions
        system_instruction = (
            f"You are HeyrronChat 2.0, a friendly and intelligent personal assistant. "
            f"Always reply in {self.lang_name}. "
            f"Keep vocal responses concise, natural, and conversational (1-3 sentences) "
            f"so they are comfortable to listen to via text-to-speech."
        )

        self.chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )

    def speak(self, text: str):
        """Outputs text through the local TTS engine."""
        print(f"\nHeyrronChat: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        """Captures mic input with fallback to keyboard input."""
        with sr.Microphone() as source:
            print("Listening (speak or press Ctrl+C to type)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language=self.user_lang)
                print(f"You (voice): {text}")
                return text.strip()
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return input("Didn't catch that. Type here: ").strip()
            except (sr.RequestError, KeyboardInterrupt):
                return input("Audio unavailable. Type here: ").strip()

    def generate_response(self, prompt: str) -> str:
        """Sends the message to Gemini Chat and returns the text."""
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    def run(self):
        # Startup greeting
        welcome = self.generate_response(
            "Start by saying 'Hello! I am HeyrronChat version 2.0, ready to assist you.'"
        )
        self.speak(welcome)

        while True:
            user_input = self.listen()

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                farewell = self.generate_response("Say a short polite goodbye.")
                self.speak(farewell)
                break

            # Send prompt directly to Gemini
            bot_reply = self.generate_response(user_input)
            self.speak(bot_reply)

# -------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------
if __name__ == "__main__":
    # Get API key from environment, or enter it manually
    API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"

    print("--- Supported Languages ---")
    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"[{code}] {name}")

    selected_lang = input("\nSelect your language code (default 'en'): ").strip().lower()

    bot = HeyrronChat2(api_key=API_KEY, user_lang=selected_lang)
    bot.run()