from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

template = PromptTemplate(
    template="""
    You are an expert content writer who writes technical article with professional tone. Write an article on the topic of {topic}. Create the content with {number} words.
    """, input_variables=["topic", "number"], validate_template=True)

model = ChatOpenAI(model="gpt-4o-mini")

prompt = template.invoke({'topic': 'Impact of AI in tech industry', 'number': '100'})

prompt2 = template.invoke({'topic': 'Current GDP of India', 'number': '300'})

response = model.invoke(prompt)

print(response.content)