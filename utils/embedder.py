from chromadb.utils.embedding_functions import EmbeddingFunction
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

class GeminiEmbeddingFunction(EmbeddingFunction):    
    def __call__(self, input):
        model = "text-embedding-004"
        result = client.models.embed_content(
            model=model,
            contents=input,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )
        
        return result.embeddings[0].values