from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda


load_dotenv()

model = ChatMistralAI(model="mistral-small-2506")
parser = StrOutputParser()

short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines"
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain the concept in detail"
)

topic = "Machine learning"

# chain  = {
#    "short" : short_prompt | model | parser,
#    "detailed" : detailed_prompt | model | parser
# }

# result = chain.invoke({"topic" : "Machine Learning"})

# print(result)

chain = RunnableParallel({
    "short" : RunnableLambda(lambda x: {'topic': x['topic']}) | short_prompt | model | parser,
    "detailed" : RunnableLambda(lambda x: {'topic': x['topic']}) | detailed_prompt | model | parser
})

result = chain.invoke({"topic" : "Machine Learnings"})

print(f"Short prompt answer : {result['short']}\n")
print(f"Long prompt answer : {result['detailed']}")



