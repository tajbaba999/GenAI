from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_classic.retrievers import EnsembleRetriever
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Neural networks and deep learning models process data using layers.", metadata={"id": 1}),
    Document(page_content="Error code ERR-9021 happens when the server times out.", metadata={"id": 2}),
    Document(page_content="Python and Pandas are primary tools used for data analysis.", metadata={"id": 3}),
    Document(page_content="Product SKU-4829 is currently out of stock.", metadata={"id": 4}),
]

embedding_model = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embedding_model)
dense_vector = vectorstore.as_retriever(search_kwargs={"k": 2})

spare_vector = BM25Retriever.from_documents(docs)
spare_vector.k = 2;

hybrid_retriver = EnsembleRetriever(
    retrievers=[dense_vector, spare_vector],
    weights=[0.5, 0.5]
)

print("--- Query 1: Exact Match (Sparse handles this best) ---")
results = hybrid_retriver.invoke("ERR-9021")
for doc in results:
    print(doc.page_content)

print("\n--- Query 2: Conceptual/Semantic (Dense handles this best) ---")
results = hybrid_retriver.invoke("How do AI algorithms process information?")
for doc in results:
    print(doc.page_content)

