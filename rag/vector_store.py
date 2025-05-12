import os
import time
import chromadb
from tqdm import tqdm
from rag.embedder import GeminiEmbeddingFunction
from rag.loader import extract_text_from_pdf
from rag.splitter import split_text

DB_PATH = "./chroma_db"
DOC_FOLDER = "context_docs"

embedding_fn = GeminiEmbeddingFunction()

def get_chroma_db(name):
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    db = chroma_client.get_or_create_collection(name=name, embedding_function=embedding_fn)

    if db.count() == 0:
        print("Indexing documents...")

        for filename in os.listdir(DOC_FOLDER):
            if filename.endswith(".pdf"):
                file_path = os.path.join(DOC_FOLDER, filename)
                print(f"\nProcessing {filename}...")

                starting_page = 1 if "[WEB]" in filename else 5
                text = extract_text_from_pdf(file_path, starting_page=starting_page)
                chunks = split_text(text)
                base_id = os.path.splitext(filename)[0]

                for i, chunk in tqdm(enumerate(chunks), total=len(chunks), desc=f"Indexing {filename}"):
                    db.add(
                        documents=chunk,
                        ids=f"{base_id}_{i}"
                    )
                    time.sleep(1)

    return db

def search_similar(db, query):
    result = db.query(query_texts=[query], n_results=5)
    return result["documents"][0]
