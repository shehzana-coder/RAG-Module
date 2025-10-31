import os
import json
from langchain_text_splitters import MarkdownTextSplitter  
from langchain_community.document_loaders import TextLoader  

# Directory containing the Markdown file
textfile_dir = "Textfiles"
md_file_path = os.path.join(textfile_dir, "combined_content.md")  

# Check if file exists before loading
if not os.path.exists(md_file_path):
    raise FileNotFoundError(f"Markdown file not found at: {md_file_path}")

# Load the Markdown file for further processing
loader = TextLoader(md_file_path, encoding="utf-8")
docs = loader.load()

print(f"Loaded {len(docs)} document(s) from Markdown file: {md_file_path}")

# Split Markdown content into smaller chunks
splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

print(f"Total chunks created: {len(split_docs)}")

# Save chunks to a JSON file
chunks_data = [
    {"content": doc.page_content, "metadata": doc.metadata} for doc in split_docs
]

output_json_path = os.path.join("Textfiles", "split_chunks.json")

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(chunks_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(chunks_data)} chunks to '{output_json_path}'")


