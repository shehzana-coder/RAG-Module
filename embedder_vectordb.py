import os
import json
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_community.vectorstores import Chroma

# ===== Step 1: Load JSON chunks =====
textfile_dir = "Textfiles"
json_path = os.path.join(textfile_dir, "split_chunks.json")

with open(json_path, "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

docs = [Document(page_content=chunk["content"]) for chunk in chunks_data]
print(f"Loaded {len(docs)} chunks (no metadata) from '{json_path}'")

# ===== Step 2: Initialize the embedding model =====
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# ===== Step 3: Create Chroma database with streamed embedding =====
persist_dir = "chroma_db_bge"
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# Process and add embeddings with progress bar
print("\nGenerating embeddings and storing in Chroma...\n")
for i in tqdm(range(0, len(docs), 50), desc="Embedding chunks", unit="batch"):
    batch = docs[i:i + 50]  # process in small batches to avoid memory spikes
    db.add_documents(batch)

# Persist the Chroma DB
db.persist()
print(f"\nStored {len(docs)} chunks in Chroma vector database at '{persist_dir}'")
