import os
import time
import chromadb
from tqdm import tqdm
from utils.embedder import GeminiEmbeddingFunction
from utils.loader import extract_text_from_pdf
from utils.splitter import split_text

DB_PATH = "./chroma_db"
DOC_FOLDER = "context_docs"

embedding_fn = GeminiEmbeddingFunction()

def get_chroma_db(name):
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    db = chroma_client.get_or_create_collection(name=name, embedding_function=embedding_fn)

    if db.count() == 0: # Just in case db is empty on startup
        print("Indexing documents...")

        current_data = db.peek(db.count())
        sources = {meta.get("source") for meta in current_data["metadatas"] if meta}
        print(f"Currently Indexed Sources: {sources}")
        for filename in os.listdir(DOC_FOLDER):
            if filename.endswith(".pdf") and filename not in list(sources):
                file_path = os.path.join(DOC_FOLDER, filename)
                print(f"\nProcessing {filename}...")
                
                
                starting_page = 1 if "[WEB]" in filename else 5
                text = extract_text_from_pdf(file_path, starting_page=starting_page)
                chunks = split_text(text)
                base_id = os.path.splitext(filename)[0]

                for i, chunk in tqdm(enumerate(chunks), total=len(chunks), desc=f"Indexing {filename}"):
                    db.add(
                        documents=chunk,
                        ids=f"{base_id}_{i}",
                        metadatas={"source": filename}
                    )
                    time.sleep(1)
                print(f"\Processing {filename} Done ✅")
                time.sleep(10) # add this to avoid spamming / overloading the google text embedding model

    return db

def search_similar(db, query, n_results=5, threshold=0.65):
    result = db.query(query_texts=[query], n_results=n_results)
    documents = result["documents"][0]
    scores = result["distances"][0]

    # Filter docs by threshold
    relevant_docs = [
        doc for doc, score in zip(documents, scores) if score <= threshold
    ]

    return relevant_docs if relevant_docs else None
