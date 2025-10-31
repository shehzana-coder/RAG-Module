import os
from markitdown import MarkItDown
from langchain_community.document_loaders import TextLoader 


# Directory containing all the text files
text_directory = "Textfiles"  

# Define the text files you want to combine
pdf_text_path = os.path.join(text_directory, "Pdfcontent.txt")
web_text_path = os.path.join(text_directory, "Webcontents.txt")

# Read contents from both files
with open(pdf_text_path, "r", encoding="utf-8") as f:
    pdf_text = f.read()

with open(web_text_path, "r", encoding="utf-8") as f:
    web_text = f.read()

# Combine both contents
combined_text = f"# PDF Content\n\n{pdf_text}\n\n# Web Content\n\n{web_text}"

# Save combined text to a temporary file
combined_text_path = os.path.join(text_directory, "combined_content.txt")
with open(combined_text_path, "w", encoding="utf-8") as f:
    f.write(combined_text)

# Convert the combined text into Markdown format
markitdown = MarkItDown()
result = markitdown.convert(combined_text_path)

# Access the Markdown text
markdown_text = result.text_content

# Write the Markdown output to a file
md_output_path = os.path.join(text_directory, "combined_content.md")
with open(md_output_path, "w", encoding="utf-8") as f:
    f.write(markdown_text)

print(f"Markdown file created: {md_output_path}")

