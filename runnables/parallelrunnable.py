from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda


load_dotenv()

model = ChatMistralAI(model="mistral-small-2506")
parser = StrOutputParser()

# short_prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in 1-2 lines"
# )

# detailed_prompt = ChatPromptTemplate.from_template(
#     "Explain the concept in detail"
# )

# topic = "Machine learning"

# chain  = {
#    "short" : short_prompt | model | parser,
#    "detailed" : detailed_prompt | model | parser
# }

# result = chain.invoke({"topic" : "Machine Learning"})

# print(result)

# chain = RunnableParallel({
#     "short" : RunnableLambda(lambda x: {'topic': x['topic']}) | short_prompt | model | parser,
#     "detailed" : RunnableLambda(lambda x: {'topic': x['topic']}) | detailed_prompt | model | parser
# })

# result = chain.invoke({"topic" : "Machine Learnings"})

# print(f"Short prompt answer : {result['short']}\n")
# print(f"Long prompt answer : {result['detailed']}")


code_prompt = ChatPromptTemplate.from_messages({
    ("system", "You are a code genrator"),
    ("human", "{topic}")
})

explain_prompt = ChatPromptTemplate.from_messages({
    ("system", "You are a helpful coding assitent who explain coding in simple terms"),
     ("human", "Explain the following code in simple words:\n{code}")
})

seq = code_prompt | model | parser

seq2 = RunnableParallel(
    {"code" : RunnableParallel(),
    "explanation" : explain_prompt | model | parser
    }
  )

chain = seq | seq2

result = chain.invoke({"topic" : "please write a code of palindrome in python"})

print(result['code'])
print(result['explanation'])


