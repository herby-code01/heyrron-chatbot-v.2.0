import json
import pyttsx3
import speech_recognition as sr
from translatepy import Translator
import requests
from bs4 import BeautifulSoup
import random

supported_lang = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'pl': 'Polish',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'sk': 'Slovak',
    'el': 'Greek',
    'he': 'Hebrew',
    'th': 'Thai',
    'ms': 'Malay',
    'id': 'Indonesian',
    'uk': 'Ukrainian',
    'bg': 'Bulgarian',
    'sr': 'Serbian',
    'hr': 'Croatian',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'et': 'Estonian',
    'mt': 'Maltese'
}

for code, name in supported_lang.items():
    print(f"{code}: {name}")

user_lang = input("Enter the language you want so that I can reset psych my brain with that language.\n").lower()
if user_lang not in supported_lang:
    user_lang = 'en'

translator = Translator()

def translate_text(text, target_language):
    """Translate text to the specified language using translatepy."""
    if target_language not in supported_lang:
        print(f"Unsupported language code: {target_language}. Defaulting to English.")
        target_language = 'en'
    try:
        translation = translator.translate(text, target_language).result
        return translation
    except Exception as e:
        print(f"Translation error: {e}. Returning original text.")
        return text

sorrymessage1 = translate_text("Sorry for the delay, I was getting ready for the conversation..", user_lang)
sorrymessage2 = translate_text("Ooosh, I'm doomed..Let's start everything from scratch..", user_lang)
savemessage = translate_text("I've saved it in my brain.", user_lang)
voicemessage1 = translate_text("Sorry, I didn't understand that.", user_lang)
voicemessage2 = translate_text("Sorry, my speech recognition service is down.", user_lang)
askmessage = translate_text("I don't know the answer to that.. Can you please teach me?", user_lang)
askmessage2 = translate_text("I don't have a valid response for this question, you have to train me for that.", user_lang)
learnmessage = translate_text("Thanks! I've learned the new answer..", user_lang)
initializationmessage = translate_text("Hello! I'm your personal Heyrron Artificial Intelligence Chatbot", user_lang)
supportedmessage = translate_text("Supported languages", user_lang)
breakword = translate_text("exit", user_lang)

class HeyrronChatbot:
    def __init__(self, memory_file='E:\projects\Chatbot\chatbot_memory.json'):
        self.memory_file = memory_file
        self.engine = pyttsx3.init()
        self.memory = {}
        self.translator = Translator()
        self.supported_languages = supported_lang
        self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, 'r') as file:
                self.memory = json.load(file)
            self.speak(sorrymessage1)
        except FileNotFoundError:
            self.speak(sorrymessage2)
            self.memory = {}

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)
        self.speak(savemessage)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            self.speak(voicemessage1)
            return None
        except sr.RequestError:
            self.speak(voicemessage2)
            return None

    def ask_question(self, question):
        question = question.lower()
        if question in self.memory:
            responses = self.memory[question]
            if isinstance(responses, list) and responses:
                return random.choice(responses)
            return askmessage2
        else:
            return askmessage

    def learn_answer(self, question, answer):
        question = question.lower()

        if question in self.memory:
            if isinstance(self.memory[question], list):
                self.memory[question].append(answer)
            else:
                self.memory[question] = [self.memory[question], answer]
        else:
            self.memory[question] = answer
        self.save_memory()
        return learnmessage

    def translate_text(self, text, target_language):
        if target_language not in self.supported_languages:
            print(f"Unsupported language code: {target_language}. Defaulting to English.")
            target_language = 'en'
        try:
            translation = self.translator.translate(text, target_language).result
            return translation
        except Exception as e:
            print(f"Translation error: {e}. Returning original text.")
            return text

    def search_web(self, query):
        """Searches the web for an answer using a basic web scraping method."""
        search_url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting search result snippets from Google (assumes snippets are within specific HTML tags)
        results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        if results:
            return results[0].text  # Return the first result snippet
        return "Sorry, I couldn't find an answer on the web."

    def intro(self):
        self.speak(initializationmessage)
        print(initializationmessage)
        self.speak(self.translate_text("What's your name...?", user_lang))
        print(self.translate_text("What's your name..?", user_lang))
    
        user_name = self.listen()
        user_input = None  # Initialize user_input here to avoid unbound errors
    
        if user_name is None:
            self.speak(self.translate_text("Enter your name instead..", user_lang))
            user_name = input(self.translate_text("Enter your name instead...", user_lang) + "\n")
        
        user_input_None_trans = self.translate_text("You can type it here instead", user_lang)
        trans_intro = self.translate_text(f"What's up {user_name}", user_lang)
        self.speak(trans_intro)
        print(trans_intro)

        user_input = self.listen()

        if user_input is None:
            user_input = input(f"..{user_input_None_trans}..\n")

        user_input_def_trans = self.translate_text(user_input, 'en')
        response = self.ask_question(user_input_def_trans)
        response_trans = self.translate_text(response, user_lang)
        print(f"Chatbot: {response_trans}")
        self.speak(response_trans)

        if response == askmessage or response == askmessage2:
            t = "Or 'I don't know' for me to look it up on the internet"
            t_trans = self.translate_text(t, user_lang)
            print(t_trans +"\n")
            self.speak(t_trans)
            user_answer = self.listen()

            if user_answer is None:
                user_answer = input(self.translate_text(t, user_lang))

            if user_answer:
                user_answer_trans = self.translate_text(user_answer, 'en')

                if user_answer_trans.lower() in ["i don't know", "search it for me"]:
                    web_answer = self.search_web(user_input_def_trans)
                    web_answer_trans = self.translate_text(web_answer, 'en')
                    self.speak(self.translate_text(f"Here is what I got: {web_answer_trans}", user_lang))
                    print(self.translate_text(f"Here is what I got: {web_answer_trans}", user_lang))
                    self.learn_answer(user_input_def_trans, web_answer_trans)
                else:
                    self.speak(self.learn_answer(user_input_def_trans, user_answer_trans))

    def firstprompt(self):
        user_input_None_trans = self.translate_text("You can type it here instead", user_lang)
        firstprompt = f"What's on your mind, tell me... Let's talk"
        self.speak(firstprompt)
        print(f"{firstprompt}")

        user_firstprompt = self.listen()

        if user_firstprompt is None:
            user_firstprompt = input(f"{user_input_None_trans}\n")

        user_firstprompt_def_trans = self.translate_text(user_firstprompt, 'en')
        response = self.ask_question(user_firstprompt_def_trans)
        response_trans = self.translate_text(response, user_lang)
        self.speak(response_trans)
        print(f"Chatbot: {response_trans}")
        

        if response == askmessage or response == askmessage2:
            i = "Or 'I don't know' for me to search on the web"
            i_trans = self.translate_text(i, user_lang)
            self.speak(i_trans)
            print(i_trans)
            user_answer = self.listen()

            if user_answer is None:
                user_answer = input(f"{user_input_None_trans}\n")

            if user_answer:
                user_answer_trans = self.translate_text(user_answer, 'en')

                if user_answer_trans.lower() in ["i don't know", "search it for me"]:
                    web_answer = self.search_web(user_firstprompt_def_trans)
                    web_answer_trans = self.translate_text(web_answer, 'en')
                    self.speak(self.translate_text(f"Here is what I found: {web_answer_trans}", user_lang))
                    print(self.translate_text(f"Here is what I found: {web_answer_trans}", user_lang))
                    self.learn_answer(user_firstprompt_def_trans, web_answer_trans)
                else:
                    self.speak(self.learn_answer(user_firstprompt_def_trans, user_answer_trans))

    def loop(self):
        user_input_None_trans = self.translate_text("You can type it here instead", user_lang)
        loop = f"Anything else..."
        self.speak(loop)
        print(f"{loop}")

        user_loop = self.listen()

        if user_loop is None:
            user_loop = input(f"{user_input_None_trans}\n")

        user_loop_def_trans = self.translate_text(user_loop, 'en')
        response = self.ask_question(user_loop_def_trans)
        response_trans = self.translate_text(response, user_lang)
        self.speak(response_trans)
        print(f"Chatbot: {response_trans}")
        

        if response == askmessage or response == askmessage2:
            l = "Or 'I don't know' for me to search on the web"
            l_trans = self.translate_text(l, user_lang)
            self.speak(l_trans)
            print(l_trans)
            user_answer = self.listen()

            if user_answer is None:
                user_answer = input(f"{user_input_None_trans}\n")

            if user_answer:
                user_answer_trans = self.translate_text(user_answer, 'en')

                if user_answer_trans.lower() in ["i don't know", "search it for me"]:
                    web_answer = self.search_web(user_loop_def_trans)
                    web_answer_trans = self.translate_text(web_answer, 'en')
                    self.speak(self.translate_text(f"Here is what I found: {web_answer_trans}", user_lang))
                    print(self.translate_text(f"Here is what I found: {web_answer_trans}", user_lang))
                    self.learn_answer(user_loop_def_trans, web_answer_trans)
                else:
                    self.speak(self.learn_answer(user_loop_def_trans, user_answer_trans))
                
    def run(self):
        self.intro()
        self.firstprompt()
        while True:
            self.loop()
        
if __name__ == "__main__":
    chatbot = HeyrronChatbot()
    chatbot.run()