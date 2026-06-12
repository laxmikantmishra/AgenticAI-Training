from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

# Specialist Agent
specialist = AssistantAgent(
    name="specialist",
    model_client=llm,
    system_message="You are a brand strategist. Propose a single marketing direction. After you speak, wait for the director's feedback",
    model_client_stream=True
)

# Human Agent - You
human_director = UserProxyAgent(name="director")

team = RoundRobinGroupChat(
    participants=[specialist, human_director],
    termination_condition=TextMentionTermination("Approved")
)

async def main():
    await Console(team.run_stream(task="Propose a brand identity for a high end electric bike called 'Electrica'"))

asyncio.run(main())