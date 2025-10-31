from retriever import init_retriever, ask_query

init_retriever()

response = ask_query("What is the purpose of the student handbook?")
print(response)

