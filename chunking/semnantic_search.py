import os
from dotenv import load_dotenv
from pypdf import PdfReader
import re
from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

load_dotenv();

pdf_file_path = os.path.join(os.path.dirname(__file__), "Cloud_Computing.pdf")

print(f"Loading PDF from : {pdf_file_path}")


with open(pdf_file_path, 'rb') as file:
    pdf_reader = PdfReader(file)
    
    total_pages = len(pdf_reader.pages)
    print(f"PDF contains {total_pages} pages")

    raw_text = ""
    for page_num in range(total_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        raw_text += page_text + "\n"

print(f"PDF processing completed")
print(f"Total extacted text length : {len(raw_text):,} characters")

print("Cleaning extracted text...")

cleaned_text = re.sub(r' +', ' ', raw_text)

cleaned_text = re.sub(r'\n+', '\n\n', cleaned_text)

lines = [line.strip() for line in cleaned_text.split('\n')]
final_text = '\n'.join(lines)

print(f"Text cleaning completed. Final length: {len(final_text):,} characters")


print("Creating semantic characters.....")

# embeddings_model = OpenAIEmbeddings()
embeddings_model = MistralAIEmbeddings(model="mistral-embed")

chunker = SemanticChunker(
    embeddings_model,
    breakpoint_threshold_type='percentile',
    breakpoint_threshold_amount=90
)

print("Semantic chunker created sucessfully")

print("Startring the semantic chunking process...")
print(f"Original text length : {len(final_text)} characters")

documents_chunks = chunker.create_documents([final_text])

print(f"Semantic chucking completed")
print(f"Number of chunks are created: {len(documents_chunks)}")

# print(f"\nPreviewing random 3 chunks:")
# print("=" * 60)


# for i, chunk in enumerate(documents_chunks):
#     print(f"\nCHUNK {i + 1} (Length: {len(chunk.page_content)} characters):")
#     print("-" * 40) 
#     preview_text = chunk.page_content[:200] + "..." if len(chunk.page_content) > 200 else chunk.page_content
#     print(preview_text)
#     print("-" * 40) 


print("Creating vector Datbase")
print(f"Processing {len(documents_chunks)} chunks")

# embeddings_model = OpenAIEmbeddings()
embeddings_model = MistralAIEmbeddings(model="mistral-embed")

print("Genrating embeddings and buildings FAISS index... ")
vector_database = FAISS.from_documents(documents_chunks, embeddings_model)


print("Vector database created successfully!")
print(f"Database contains {len(documents_chunks)} searchable chunks")


print("Creating basic similariy retriver....")

basic_retriver = vector_database.as_retriever(
   search_kwargs={"k": 3}
)

# print(basic_retriver)
print("Basic retriever created - returns top 3 similar chunks")

query = "What is cloud computing?"
results = basic_retriver.invoke(query)

print(f"\nQuery: {query}")
print(f"Found {len(results)} relevant chunks:\n")

for i, doc in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(doc.page_content[:300])
    print()
