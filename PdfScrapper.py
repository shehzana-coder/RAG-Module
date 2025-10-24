
from langchain_community.document_loaders import PyMuPDFLoader 
import pprint
from markitdown import MarkItDown 
from langchain_community.document_loaders import TextLoader 
from langchain_text_splitters import MarkdownTextSplitter   
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain_mistralai import ChatMistralAI 
from langchain_core.messages import HumanMessage 
from langchain_core.prompts import ChatPromptTemplate

# PyMuPDFLoader library helps load and read PDF files page by page.
# Used to extract the text from each page of your PDF document.
loader = PyMuPDFLoader(
    "student_hand_book_2024_25_10.pdf",
    mode="page",
)
docs = loader.load()
print(len(docs))

# Pretty Print (pprint) makes printed output look neat and readable.
# Purpose: Used to display document content and results in a clean format.
pprint.pp(docs[0].page_content)



for i, doc in enumerate(docs):
    print(f"\n===== PAGE {i+1} =====")
    print(doc.page_content)



with open("pdf_content.txt", "w", encoding="utf-8") as f:
    for doc in docs:
        f.write(doc.page_content + "\n")

# MarkItDown
# Converts documents (like PDFs or text files) into Markdown format.
# Used to convert the extracted PDF text (pdf_content.txt) into a Markdown file.

markitdown = MarkItDown()
result = markitdown.convert("pdf_content.txt")

# Access the text part
markdown_text = result.text_content

# Now write it to a file
with open("pdf_content.md", "w", encoding="utf-8") as f:
    f.write(markdown_text)


# TextLoader
# Loads text files so they can be processed like documents.
# Used to load the converted Markdown file for further splitting.


loader = TextLoader("pdf_content.md", encoding="utf-8")
docs = loader.load()


# MarkdownTextSplitter

# Splits large Markdown documents into smaller chunks of text.
# It helps divide the document into parts that can be embedded easily and stored in a vector database.

splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)
print(f"Total chunks created: {len(split_docs)}")
pprint.pp(split_docs[2].page_content)


# HuggingFaceEmbeddings
# Converts text into numerical vectors (embeddings) for similarity search.
# Used to turn each chunk of the document into embeddings for storage and retrieval.

# Load BGE-base English model
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")



texts = [doc.page_content for doc in split_docs]
vectors = embeddings.embed_documents(texts)
print(f"Total chunks: {len(vectors)}")
print(f"Embedding dimension: {len(vectors[0])}")
print(f"First chunk sample:\n{texts[0][:200]}")
print(f"First vector sample:\n{vectors[0][:5]}")

# Chroma

# A local database that stores and retrieves text embeddings efficiently.
# Used to create and save a searchable database of the document chunks.


db = Chroma.from_texts(
    texts=texts,              
    embedding=embeddings,        
    persist_directory="./chroma_db_bge"  
)


db.persist()

print("✅ ChromaDB created and saved successfully!")
print("Total documents stored:", db._collection.count())


retriever = db.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke("What is this document about?")
for i, doc in enumerate(results):
    print(f"\n--- Chunk {i+1} ---\n{doc.page_content[:300]}")

# ChatMistralAI

# A powerful AI model that answers questions using given text context.
# Used to generate intelligent answers based on the document’s content.

llm = ChatMistralAI(
    model="mistral-large-latest",
    mistral_api_key="ntieqofTshmKXs2Njl9ImaHZDyanjIwS"
)



query = "Credit hours in scheme of study of Computer Science?"
relevant_docs = retriever.invoke(query)

# ChatPromptTemplate

# Helps structure and format prompts for the AI model.
# Used to create a clear question-answer format for the chatbot.

prompt = ChatPromptTemplate.from_template("""
You are an intelligent assistant.
Use the following context to answer the question.
If the answer is not in the context, say "I don’t know".

Context:
{context}

Question: {question}
""")

context = "\n\n".join([doc.page_content for doc in relevant_docs])
formatted_prompt = prompt.format(context=context, question=query)

# HumanMessage

# Wraps the user’s message so it can be processed by the AI model.
# Used to send the formatted prompt (context + question) to the model.

response = llm.invoke([HumanMessage(content=formatted_prompt)])
print(response.content)
