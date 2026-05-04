from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# model setup 
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# 1st agent 
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# 2nd agent
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


# Writter chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful report."),
    ("human", """
        Write a detailed research report on the topic below.
        Topic: {topic}

        Research Gathered:
        {research}

        Structure the report as:
        - Introduction
        - Key FIndings (minimum 3 well-explained points)
        - Conclusion
        - Sources (list all the URLs fount in the research)
     
     Be detailed, factful and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("Human", """
        Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in this exact format:

        Score: x/10
     
        Strenths:
        - .....
        - ....
     
        Area to improve:
        - ....
        - ....

        One line verdict:
        .....
        """),
])


critic_chain = critic_prompt | llm | StrOutputParser()