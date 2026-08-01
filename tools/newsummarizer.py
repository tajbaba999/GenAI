from dotenv import load_dotenv
load_dotenv()
from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearch(max_result=5)


llm = ChatMistralAI(model = "mistral-small-2506")

prompt = ChatPromptTemplate.from_template(
    """
    You are the helpful assistant

    summarize the follwing into clear bullet points.
    {news}
    """
)

chain = prompt | llm | StrOutputParser()

news_result = search_tool.run("Latest ai tool of 2026")

result = chain.invoke({"news" : news_result})

print(result)


