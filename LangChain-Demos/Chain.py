from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

template = PromptTemplate(
    template="""
    You are an expert content writer who writes technical article with professional tone. Write an article on the topic of {topic}
    """, input_variables=["topic"], validate_template=True)

template2 = PromptTemplate(
    template="""
    Create 5 multiple choice questions with answers based on the following article:\n
    {article}. Complexity level must be {level}.
    """, input_variables=["article", "level"], validate_template=True)

model = ChatOpenAI(model="gpt-4o-mini")

# prompt = template.invoke({'topic': 'Impact of AI in tech industry'})
# response = model.invoke(prompt)
# prompt2 = template2.invoke({'article': response.content})
# response2 = model.invoke(prompt2)

chain = template | model | StrOutputParser() | (lambda article: {"article": article, "level": RunnablePassthrough()}) | template2 | model | StrOutputParser()

print(chain.invoke({'topic': 'Impact of AI in tech industry',"level": "intermediate"}))