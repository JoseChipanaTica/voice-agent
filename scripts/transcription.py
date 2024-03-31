import os
from abc import ABC, abstractmethod

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions, Microphone,
)
import asyncio


class TranscriptCollector:
    def __init__(self):
        self.transcript_parts = None
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)


class Transcription(ABC):
    @abstractmethod
    def transcribe(self, text):
        pass


class DeepGramTranscription(Transcription):
    def __init__(self, transcript_collector: TranscriptCollector):
        self.transcript_collector = transcript_collector

    async def transcribe(self, callback):
        transcription_complete = asyncio.Event()

        try:
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"), config)
            dg_connection = deepgram.listen.asynclive.v("1")

            async def on_message(_self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript

                if not result.speech_final:
                    self.transcript_collector.add_part(sentence)

                else:
                    self.transcript_collector.add_part(sentence)
                    full_sentence = self.transcript_collector.get_full_transcript()

                    if len(full_sentence.strip()) > 0:
                        full_sentence = full_sentence.strip()
                        callback(full_sentence)

                        self.transcript_collector.reset()
                        transcription_complete.set()

            async def on_metadata(self, metadata, **kwargs):
                print(f"")

            async def on_error(self, error, **kwargs):
                print(f"")

            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)

            options = LiveOptions(
                model="nova-2",
                punctuate=True,
                language="en-US",
                encoding="linear16",
                channels=1,
                sample_rate=16000,
                endpointing=300,
                smart_format=True,
            )

            await dg_connection.start(options)
            microphone = Microphone(dg_connection.send)
            microphone.start()

            await transcription_complete.wait()

            microphone.finish()
            await dg_connection.finish()

        except Exception as e:
            print(f"Could not open socket: {e}")
            return
