from dotenv import load_dotenv

import asyncio
from scripts.transcription import TranscriptCollector, DeepGramTranscription
from scripts.llm import Agent
from scripts.speak import DeepGramSpeak
from utils.colors import Colors

load_dotenv()

speak = DeepGramSpeak()
agent = Agent(speak)

collector = TranscriptCollector()
transcriptAgent = DeepGramTranscription(collector)


class ConversationManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = agent

    async def main(self):
        print(Colors.CYAN + f"\n Start recording" + Colors.CYAN)

        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        while True:
            await transcriptAgent.transcribe(handle_full_sentence)
            print(Colors.GREEN + f"\n {self.transcription_response}" + Colors.GREEN)
            await self.llm.streaming(self.transcription_response)

            self.transcription_response = ""


if __name__ == "__main__":
    manager = ConversationManager()
    asyncio.run(manager.main())
