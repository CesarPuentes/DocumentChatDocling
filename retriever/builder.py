from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class RetrieverBuilder:
    def __init__(self):
        """Initialize the retriever builder with embeddings based on the selected provider."""
        provider = settings.LLM_PROVIDER.lower()
        logger.info(f"Initializing embeddings for provider: {provider}")

        if provider == "watsonx":
            from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
            from langchain_ibm import WatsonxEmbeddings
            
            embed_params = {
                EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
                EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
            }
            self.embeddings = WatsonxEmbeddings(
                model_id="ibm/slate-125m-english-rtrvr-v2",
                url="https://us-south.ml.cloud.ibm.com",
                project_id=settings.WATSONX_PROJECT_ID,
                apikey=settings.WATSONX_APIKEY,
                params=embed_params
            )
        elif provider == "deepseek":
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model="deepseek-embed", # or another DeepSeek embedding model if available
                api_key=settings.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com/v1"
            )
        elif provider in ["openai", "ollama"]:
            from langchain_openai import OpenAIEmbeddings
            model = "text-embedding-3-small" if provider == "openai" else settings.OLLAMA_MODEL_NAME
            api_key = settings.OPENAI_API_KEY if provider == "openai" else "ollama"
            base_url = None if provider == "openai" else settings.OLLAMA_BASE_URL
            
            self.embeddings = OpenAIEmbeddings(
                model=model,
                api_key=api_key,
                base_url=base_url
            )
        else:
            raise ValueError(f"Unsupported provider for embeddings: {provider}")
        
    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:
            # Create Chroma vector store
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=settings.CHROMA_DB_PATH
            )
            logger.info("Vector store created successfully.")
            
            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(docs)
            logger.info("BM25 retriever created successfully.")
            
            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(search_kwargs={"k": settings.VECTOR_SEARCH_K})
            logger.info("Vector retriever created successfully.")
            
            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise