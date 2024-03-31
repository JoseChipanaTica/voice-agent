from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from scripts.speak import Speak
import webbrowser


@tool
async def open_a_linkedin() -> str:
    """Open a LinkedIn Profile"""
    webbrowser.open("https://www.linkedin.com/in/jchipana/")
    return "LinkedIn opened"


class Agent:
    def __init__(self, speak: Speak):
        print("")
        self.speak = speak

    async def streaming(self, query: str):
        prompt = hub.pull("hwchase17/openai-tools-agent")
        tools = [open_a_linkedin]

        chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", streaming=True)

        agent = create_openai_functions_agent(
            chat, tools, prompt
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools)

        async for chunk in agent_executor.astream({"input": query}):
            if "output" in chunk:
                self.speak.speak(chunk["output"])
