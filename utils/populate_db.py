import os
from tqdm import tqdm
import chromadb
import time

from loader import extract_text_from_pdf
from splitter import split_text
from embedder import GeminiEmbeddingFunction

DOC_FOLDER = "../context_docs"
DB_PATH = "../chroma_db"
embedding_fn = GeminiEmbeddingFunction()

def populate_db(name):
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    db = chroma_client.get_or_create_collection(name=name, embedding_function=embedding_fn)

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
                
if __name__ == "__main__":
    populate_db(input("Input the name of the db you want to populate: "))