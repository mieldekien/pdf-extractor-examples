"""PDF → RAG pipeline using the PDF Text Extractor API + LangChain.

A minimal RAG-over-PDFs example. Replace the URL with your own PDFs to index.

Install:
    pip install requests langchain langchain-openai langchain-community chromadb

Run:
    export RAPIDAPI_KEY="your_rapidapi_key"
    export OPENAI_API_KEY="your_openai_key"
    python examples/rag-langchain.py
"""

import os
import sys
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA


PDF_URLS = [
    # Replace with your own PDFs
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
]

QUESTION = "What is this document about?"


def fetch_pdf_text(url: str, api_key: str) -> dict:
    """Call the PDF Text Extractor API and return the parsed response."""
    r = requests.post(
        "https://pdf-text-extractor5.p.rapidapi.com/api/extract",
        json={"url": url},
        headers={
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "pdf-text-extractor5.p.rapidapi.com",
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def main():
    rapid_key = os.environ.get("RAPIDAPI_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not rapid_key or not openai_key:
        print("Set RAPIDAPI_KEY and OPENAI_API_KEY.")
        sys.exit(1)

    # 1. Fetch + extract each PDF
    docs = []
    for url in PDF_URLS:
        print(f"Extracting {url} …")
        data = fetch_pdf_text(url, rapid_key)
        if not data.get("success"):
            print(f"  failed: {data.get('error')}")
            continue
        docs.append(Document(page_content=data["text"], metadata={"source": url}))

    # 2. Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"Indexed {len(chunks)} chunks from {len(docs)} PDF(s)")

    # 3. Embed + store
    vectordb = Chroma.from_documents(
        chunks,
        embedding=OpenAIEmbeddings(),
        collection_name="pdf-rag-demo",
    )

    # 4. Query
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
    )
    answer = qa.invoke({"query": QUESTION})
    print(f"\nQ: {QUESTION}")
    print(f"A: {answer['result']}")


if __name__ == "__main__":
    main()
