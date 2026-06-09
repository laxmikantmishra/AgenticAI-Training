from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = load_prompt('travel_planner_template.json')

model = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | model | StrOutputParser() #LCEL

# print(chain.invoke({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date':'25-01-2026', 'end_date':'30-01-2026','interests':'Adventure','travel_style':'Solo','dietary_preferences':'Non-Vegetarian', 'budget': '100000'}))

for chunk in chain.stream({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date':'25-01-2026', 'end_date':'30-01-2026','interests':'Adventure','travel_style':'Solo','dietary_preferences':'Non-Vegetarian', 'budget': '100000'}):
    print(chunk, end="", flush=True)