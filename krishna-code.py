import pyttsx3
import pyaudio
import webbrowser
import datetime
from tkinter import *
from vosk import Model, KaldiRecognizer

#Commands for assistant (ALL LOWERCASE)
openyoutube = ["you tube","open you tube dot com", "open youtube", "open youtube.com", "open you tube"]
telltime = ["tell me the time", "tell time", "what is the time", "what's the time", "what time is it", "what time"]

#Necessary Variables
current_input = ""
speaking = False

#Initialization
model = Model(r"vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

#Speak input sentences out loud
def speak(text):
    stream.stop_stream()
    global speaking
    speaking = True
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    speaking = False

#cleaning other links
def clean(text):
    text = text.replace("dot", ".")
    text = text.replace(" ", "")
    return text

#Get audio from user and process it
def get_user_input():
    global current_input
    data = stream.read(2048, exception_on_overflow = False)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        current_input = text[14:-3]
        print(f"' {current_input} '")

#Program Start function
def start():
    global current_input
    print("\n\n\nVoice Assistant has started listening...\n")
    while True:
        current_input = ""
        while speaking:
            pass
        stream.start_stream()
        get_user_input()
        if current_input in openyoutube:
            speak("Opening youtube...")
            webbrowser.open("youtube.com", new=0, autoraise=True)
            current_input = ""
        elif current_input in telltime:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
            current_input = ""
        elif "open" in current_input:
            temp = clean(current_input)[4:]
            speak("Opening "+temp)
            webbrowser.open(temp, new=0, autoraise=True)
            current_input = ""

def start_listening():
    start_button.config(state=DISABLED)
    root.update()
    start()

root = Tk()
root.title("Voice Assistant")
root.geometry("300x100")

start_button = Button(root, text="Start", command=start_listening)
start_button.pack(pady=20)

root.mainloop()
