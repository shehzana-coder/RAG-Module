import os
from langchain_community.document_loaders import PyMuPDFLoader
import pprint

# Directory containing all the PDF files
pdf_directory = "PDF"  

# Collect all PDF files in the directory
pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.lower().endswith(".pdf")]

all_docs = []  # This will store all documents from all PDFs

# Load and read each PDF file
for pdf_file in pdf_files:
    print(f"\nLoading: {pdf_file}")
    loader = PyMuPDFLoader(pdf_file, mode="page")
    docs = loader.load()
    all_docs.extend(docs)  # Combine pages from all PDFs

print(f"\nTotal pages extracted from all PDFs: {len(all_docs)}")

# Pretty print the first page for a quick check
if all_docs:
    pprint.pp(all_docs[0].page_content)

# Print each page's text (optional)
for i, doc in enumerate(all_docs):
    print(f"\n===== PAGE {i+1} =====")
    print(doc.page_content)

output_dir = "Textfiles"
output_file_path = os.path.join(output_dir, "Pdfcontent.txt")

# Save all content into one text file
with open(output_file_path, "w", encoding="utf-8") as f:
    for doc in all_docs:
        f.write(doc.page_content + "\n")

print("\nAll PDF content has been saved to 'Pdfcontent.txt'.")
