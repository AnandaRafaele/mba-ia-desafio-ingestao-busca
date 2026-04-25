from search import search_prompt
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

def get_context(results):
    context = []
    for i, (doc, score) in enumerate(results, start=1):
        context.append(f"[Trecho {i} | score={score:.4f}]\n{doc.page_content.strip()}")
    return "\n\n---\n\n".join(context)



def main():
    for key in (GOOGLE_API_KEY, DATABASE_URL, COLLECTION_NAME, MODEL_NAME):
        if not key:
            raise RuntimeError(f"Environment variable {key} is not defined")

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY, temperature=0.5)

    while True:
        query = input("Faça sua pergunta: ")
        
        if query.lower() in ["sair", "exit", "quit", ""]:
            break

        embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

        store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )

        results = store.similarity_search_with_score(query, k=10)
        context = get_context(results)

        response = llm.invoke(search_prompt(context=context, question=query))
        print(response.content)

if __name__ == "__main__":
    main()