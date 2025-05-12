from chromadb.utils.embedding_functions import EmbeddingFunction
import google.generativeai as genai

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input):
        model = "models/text-embedding-004"
        title = "Trade and Exports Reports"
        return genai.embed_content(
            model=model,
            content=input,
            task_type="retrieval_document",
            title=title
        )["embedding"]