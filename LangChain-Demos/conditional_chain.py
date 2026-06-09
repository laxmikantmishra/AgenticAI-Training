from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class Feedback(BaseModel):
    sentiment: Literal['positive','negative']=Field("Give the sentiment of the feedback")

pyparser = PydanticOutputParser(pydantic_object=Feedback)

template = PromptTemplate(
    template="""
    Analyze the sentiment of the following feedback and classify it into negative or positive \n {feedback} \n {format_instructions}
    """,
    input_variables=["feedback"],
    partial_variables={'format_instructions': pyparser.get_format_instructions()}
)

chain1 = template | model | pyparser

positive_email_template = PromptTemplate(
    template="""
    Write a thank you email to the cutomer for giving the positive feedback about his recent purchase of IPhone 17. \n {feedback}
    """,
    input_variables=["feedback"]
)

negative_email_template = PromptTemplate(
    template="""
    Write an apology email to the cutomer for giving the negative feedback about his recent purchase of IPhone 17. \n {feedback}
    """,
    input_variables=["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', positive_email_template | model | StrOutputParser()),
    (lambda x:x.sentiment == 'negative', negative_email_template | model | StrOutputParser()),
    (lambda x: "Not able to analyze the sentiment")
)

main_chain = chain1 | branch_chain

# print(main_chain.invoke({'feedback': 'The phone is really good with advanced AI features. I like the phone.'}))
print(main_chain.invoke({'feedback': 'The phone is really not meeting my expectations. I am disappointed.'}))