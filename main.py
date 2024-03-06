import sounddevice as sd
import numpy as np
import wavio
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
from playsound import playsound
from pathlib import Path


# OpenAI API Key
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
model = "gpt-3.5-turbo"
temperature = 0.7
max_tokens = 150
 

def chatGpt(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print("GPT Response: ", response.choices[0].message.content)
    text_to_speech(response.choices[0].message.content)

def record_audio(filename, duration=5, fs=44100, channels=1):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype=np.int16)
    sd.wait()
    print("Finished recording.")
    wavio.write(filename, recording, fs, sampwidth=2)

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="tr-TR")
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def text_to_speech(text):
    speech_file_path = Path("speech.mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  #voices = alloy, echo, fable, onyx, nova, and shimmer
        input=text
    )
    #to do: fix get and play response
    response.stream_to_file(speech_file_path)
    playsound(speech_file_path)

    
def main():
    audio_file = 'recording.wav'
    record_audio(audio_file)
    text = speech_to_text(audio_file)
    print("Converted Text: ", text)
    chatGpt(text)

if __name__ == "__main__":
    main()
    