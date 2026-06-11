from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import requests

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

OPENWEATHER_API_KEY="0466cbde7c464dd7f56717dc5a926737"

def getWeatherInfo(city: str):
    """
    Get the current weather for a city using openweathermap api
    """
    url="https://api.openweathermap.org/data/2.5/weather"
    params={
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params)
    
    if response.status_code != 200:
        return "Unable to fetch data from API"
    
    return response.json()


agent = AssistantAgent(
    name="WeatherAgent",
    model_client=llm,
    system_message="You are a helpful AI weather assistant who answers user queries based on weather information. You are calling tools to gather weather data, interpret the data and show this in meaningful format",
    tools=[getWeatherInfo],
    reflect_on_tool_use=True
)

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower()=="exit":
            break
        result = await agent.run(task=user_input)
        print(f"AI: {result.messages[-1].content}")
    
asyncio.run(main())