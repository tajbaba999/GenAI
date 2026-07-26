from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

document = TextLoader(os.path.join(os.path.dirname(__file__), "notes.txt")).load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap=0)
texts = text_splitter.split_documents(document)

for i in texts:
    print(i.page_content)