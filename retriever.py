import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma



retriever = None
llm = None


def init_retriever():
    """Initializes Chroma retriever and OpenAI model once."""
    global retriever, llm

    if retriever is not None and llm is not None:
        print("Retriever and model already initialized.")
        return retriever, llm

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file!")

    # Load Chroma DB
    persist_dir = "chroma_db_bge"
    print("🔍 Loading Chroma database...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    print("Chroma retriever initialized.")

    # Initialize OpenAI model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        openai_api_key=api_key
    )
    print("OpenAI model ready.")

    return retriever, llm


def ask_query(query: str):
    """Takes a question, retrieves context, and generates an answer."""
    global retriever, llm
    if retriever is None or llm is None:
        raise RuntimeError("Retriever not initialized. Call init_retriever() first.")

    # Retrieve context
    docs = retriever.invoke(query)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template("""
    You are a helpful assistant. Use the provided context to answer the question accurately.

    Context:
    {context}

    Question:
    {question}

    Answer concisely in 3–5 sentences.
    """)
    prompt = prompt_template.format(context=context_text, question=query)

    # Generate answer
    response = llm.invoke(prompt)
    return response.content
