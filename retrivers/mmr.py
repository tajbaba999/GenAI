from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]

embeddings = HuggingFaceEmbeddings()

vectorstore = Chroma.from_documents(docs, embedding=embeddings)

similarity_retriver = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k" : 3}
)

print("\n===== Similarity Search Results =====\n")

similarity_docs = similarity_retriver.invoke("What is gradient descent?")

# print(similarity_docs)
for i in similarity_docs:
    print(i.page_content)

print("\n===== mmr Search Results =====\n")

mmr_retriver = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k" : 3}
)

mmr_docs = mmr_retriver.invoke("What is gradient descent?")

# print(mmr_docs)

for i in mmr_docs:
    print(i.page_content)




