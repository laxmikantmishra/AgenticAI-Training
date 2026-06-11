from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

agent = AssistantAgent(
    name="chatbot",
    model_client=llm,
    system_message="You are a helpful AI assistant who answers user queries with professional tone.",
    model_client_stream=True
)

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower()=="exit":
            break
        # result = await agent.run(task=user_input)
        # print(f"AI: {result.messages[-1].content}")
        await Console(
            agent.run_stream(task=user_input)
        )
        # async for message in agent.run_stream(task=user_input):
        #     if isinstance(message, ModelClientStreamingChunkEvent):
        #         print(message.content, end="", flush=True)
        
    
asyncio.run(main())