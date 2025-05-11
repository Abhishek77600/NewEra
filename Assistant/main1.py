import cohere
import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from youtubesearchpython import VideosSearch
import yt_dlp

# Initialize Cohere API
cohere_api_key = "YhTh8w4gexlbValOY90lm0GyV1y2awNzpnGJHVkO"  # Replace with your Cohere API Key
co = cohere.Client(cohere_api_key)

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to set a female voice
def set_female_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Index 1 is usually a female voice

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to play music from YouTube
def play_music(song_name):
    try:
        search_query = f"ytsearch:{song_name}"
        ydl_opts = {"format": "bestaudio", "noplaylist": True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if "entries" in info:
                video_url = info["entries"][0]["webpage_url"]
                webbrowser.open(video_url)
                print(f"Playing: {video_url}")
                speak(f"Playing {song_name} on YouTube.")
            else:
                speak("Sorry, I couldn't find that song.")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while trying to play the song.")

# Function to open apps
def open_app(app_name):
    if "chrome" in app_name.lower():
        os.system("start chrome")
    elif "notepad" in app_name.lower():
        os.system("notepad")
    elif "calculator" in app_name.lower():
        os.system("calc")
    else:
        speak("Sorry, I don't know how to open that app.")

# Function to answer questions using Cohere AI
def answer_question(question):
    try:
        response = co.generate(
            model="command",  # Use Cohere's "command" model for answering
            prompt=question,
            max_tokens=100
        )
        answer = response.generations[0].text.strip()
        speak(answer)
    except Exception as e:
        speak("I couldn't process that request.")
        print(f"Error: {e}")

# Function to process commands
def process_command(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "play" in command.lower():
        song_name = command.lower().replace("play", "").strip()
        play_music(song_name)
    elif "open" in command.lower():
        app_name = command.lower().replace("open", "").strip()
        open_app(app_name)
    elif "what" in command.lower() or "who" in command.lower() or "how" in command.lower():
        answer_question(command)
    else:
        speak("Sorry, I don't understand that command.")

# Main function to run the virtual assistant
def virtual_assistant():
    set_female_voice()
    speak("Initializing Kavita..........")
    while True:
        with sr.Microphone() as source:
            print("Calibrating for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening......")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing.....")
                word = recognizer.recognize_google(audio)
                print(f"You said: {word}")
                if word.lower() == "kavita":
                    speak("Yes, how can I help you?")
                    with sr.Microphone() as source:
                        print("Kavita Active")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        process_command(command)
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except Exception as e:
                print(f"Error: {e}")

# Run the virtual assistant
if __name__ == "__main__":
    virtual_assistant()
