import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

def ingest_pdf():
    for key in (PDF_PATH, GOOGLE_API_KEY, DATABASE_URL):
        if not key:
            raise RuntimeError(f"Environment variable {key} is not defined")
    
    docs = PyPDFLoader(PDF_PATH).load()

    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(docs)
    if not splits:
        raise SystemExit("No splits found")

    enriched = [
        Document(
            page_content=doc.page_content,
            metadata=doc.metadata
        )
        for doc in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

    store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    print(f"Ingested {len(enriched)} documents into {COLLECTION_NAME} collection")

if __name__ == "__main__":
    ingest_pdf()

    print("Ingestion completed successfully")