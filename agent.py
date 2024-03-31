from dotenv import load_dotenv
import asyncio
from scripts.transcription import TranscriptCollector, DeepGramTranscription
from scripts.llm import Agent
from scripts.speak import DeepGramSpeak
from utils.colors import Colors

load_dotenv()


class ConversationManager:
    def __init__(self, llm_agent, transcriber):
        self.transcription_response = ""
        self.llm = llm_agent
        self.transcriber = transcriber

    async def main(self):
        print(Colors.CYAN + f"\n Start recording" + Colors.CYAN)

        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        while True:
            await self.transcriber.transcribe(handle_full_sentence)
            print(Colors.GREEN + f"\n {self.transcription_response}" + Colors.GREEN)
            await self.llm.streaming(self.transcription_response)

            self.transcription_response = ""


if __name__ == "__main__":
    speaker = DeepGramSpeak()
    openai_llm_agent = Agent(speaker)

    collector = TranscriptCollector()
    dg_transcriber = DeepGramTranscription(collector)

    manager = ConversationManager(openai_llm_agent, dg_transcriber)
    asyncio.run(manager.main())
