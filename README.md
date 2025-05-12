# RAG Backend with Gemini Embedding + ChromaDB

This project is a lightweight Retrieval-Augmented Generation (RAG) backend using Google's Gemini embedding model and ChromaDB for vector search. It allows querying over static PDF documents stored in a local knowledge base (`context_docs/`) and occassionally uses Google Search Tool to amplify answers as well.

## 🗂️ Project Structure

```
.
├── main.py                # FastAPI app entry point
├── .env                   # Contains Gemini API key
├── requirements.txt       # Dependencies
├── context_docs/          # Static PDFs used as the knowledge base
│   └── tdr2024_en.pdf
├── chroma_db/             # Auto-created ChromaDB persistence
├── utils/
│   ├── loader.py          # PDF text extractor
│   ├── splitter.py        # Text chunk splitter
│   ├── prompter.py        # Generate prompt for the RAG AI Model
│   ├── embedder.py        # Gemini embedder logic
│   ├── vector_store.py    # ChromaDB logic for vector search
│   └── populate_db.py     # One-time DB population script
```

## ⚙️ Setup Instructions

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set your Gemini API key**

Create a `.env` file in the root:

```
GOOGLE_API_KEY=your_google_api_key_here
```

3. **Add documents to context**

Place your `.pdf` files in the `context_docs/` folder.

4. **Populate the Chroma vector store**

```bash
python utils/populate_db.py
```

5. **Run the API server**

```bash
uvicorn main:app --reload
```

## 📫 API Usage

Once running, test the `/query` endpoint using Postman or cURL:

- **POST** `/query`
- **Body (JSON)**:

```json
{
  "query": "What are the major trade trends in 2024?"
}
```

- **Response**:

```json
{
  "query": "...",               # This is the user query from API call
  "response": "...",            # This is the response after prompting the Gemini Model
  "grounding_metadata": "...",  # This is the grounding metadata if Google Search Tool is used (null if Google Search is not used)
  "context_used": "..."         # This is the documents used from vector db
}
```

## ✅ Notes

- You can update or add documents by dropping new PDFs in `context_docs/` and re-running `populate_db.py`.
- Documents are indexed once with metadata for traceability.
- Sample docs for trade and export context has been added and indexed to the chroma db
- There are safeguards in-place to prevent the AI from answering any harmful queries. You can test this feature by asking: `"Recommend me how to destroy my business competition in international trade and exports if I live in Indonesia"`