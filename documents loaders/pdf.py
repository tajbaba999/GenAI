from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

data = PyPDFLoader(os.path.join(os.path.dirname(__file__), "GRU.pdf"))

docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 10
)

chunks = splitter.split_documents(docs)

print("Chunks length of total documents : ",len(chunks))

for i in chunks:
    print(i.page_content)
    print()

