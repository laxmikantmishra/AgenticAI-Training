from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

prompt = load_prompt('travel_planner_template.json')

model = ChatOpenAI(model="gpt-4o-mini")

st.header('Travel Planner')
username = st.text_input("Name")
destination = st.text_input("Destination")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
budget = st.slider("Select Budget", 10000, 1000000)
interest = st.multiselect("Interests", ["Adventure", "Beaches", "Nature", "Shopping"])
travel_style = st.multiselect("Travel Style", ["Luxury", "Solo", "Group", "Family"])
dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Non-Vegetarian", "Vegan"])

prompt = load_prompt('travel_planner_template.json')

chain = prompt | model | StrOutputParser() #LCEL


if st.button("Submit"):
    st.write_stream(chain.stream({'username': username, 'destination': destination, 'start_date':start_date, 'end_date':end_date,'interests':interest,'travel_style':travel_style,'dietary_preferences':dietary_preferences, 'budget': budget}))