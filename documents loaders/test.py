from langchain_community.document_loaders import TextLoader
import os

from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator = "",
    chunk_size = 1000,
    chunk_overlap = 1
)

data = TextLoader(os.path.join(os.path.dirname(__file__), "notes.txt"))

docs = data.load();

chunks = splitter.split_documents(docs)

for i in chunks:
    print(i.page_content)
    print()
