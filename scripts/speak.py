import requests
import io
from pydub import AudioSegment
from pydub.playback import play
import os
from abc import ABC, abstractmethod
from utils.colors import Colors


class Speak(ABC):
    @abstractmethod
    def speak(self, text):
        pass


class DeepGramSpeak(Speak):
    def __init__(self):
        self.token = os.getenv("DEEPGRAM_API_KEY")

    def speak(self, text):
        print(Colors.PURPLE + f"\n {text}" + Colors.PURPLE)

        DEEPGRAM_URL = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

        audio_buffer = io.BytesIO()

        with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    audio_buffer.write(chunk)

        audio_buffer.seek(0)
        audio = AudioSegment.from_mp3(audio_buffer)
        play(audio)
