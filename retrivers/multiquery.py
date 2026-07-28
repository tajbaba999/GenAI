from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms."),
    Document(page_content="India is best country")
]


embeddings = HuggingFaceEmbeddings()

vectorstore = Chroma.from_documents(docs, embedding=embeddings)

retriver = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

llm = ChatMistralAI(model="mistral-small-latest")

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriver,
    llm=llm
)

print("Multi query retriver",multi_query_retriever)

query = "What is gradient descent?"

dcos = multi_query_retriever.invoke(query)

for doc in dcos:
    print(doc.page_content)



