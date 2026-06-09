from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

OPENWEATHER_API_KEY=os.getenv("WEATHER_API_KEY")

@tool
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

agent = create_agent(
    model=llm,
    system_prompt="You are an AI weather assistant who only responds to the query about weather information. You call tools to access latest weather information. DO NOT respond to any other questions which is not about weather forecast. Maintain a friendly tone with a bit of humour. Add emojis if required to make your responses looks good. If the question is being asked about weather based other than city name, simply say that you need a city name to be mentioned to get an accurate information. Do not respond or make up any response if city name is not mentioned in user query.",
    tools=[getWeatherInfo]
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })
    print(f"AI: {response['messages'][-1].content}")
