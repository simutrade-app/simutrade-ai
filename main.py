import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from utils.vector_store import get_chroma_db, search_similar
import utils.prompter as prompter

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")

# Set the key for the Gemini API
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
client = genai.Client(api_key=GOOGLE_API_KEY)
model_id = "gemini-2.0-flash"

search_tool = Tool(google_search=GoogleSearch())

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str

# Initialize Chroma DB (done once at startup)
db = get_chroma_db(name="trade_exports_db")

@app.get("/")
def read_root():
    return {"message": "RAG backend is running."}

# @app.post("/query")
# def handle_query(request: QueryRequest):
#     try:
#         results = search_similar(db, request.query)
#         return {"results": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query")
def generate_rag_answer(request: QueryRequest):
    try:
        # Step 1: Search similar documents
        top_docs = search_similar(db, request.query)
        
        if not top_docs:
            # fallback to empty string
            top_docs = ""

        # Step 2: Format context
        prompt = prompter.make_prompt(request.query, "\n".join(top_docs))

        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=GenerateContentConfig(
                tools=[search_tool],
                response_modalities=["TEXT"],
            )
        )

        return {
            "query": request.query,
            "response": response.candidates[0].content.parts,
            "grounding_metadata": response.candidates[0].grounding_metadata.search_entry_point,
            "context_used": top_docs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

