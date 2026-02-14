import os
import sys
from loguru import logger

# Add current directory to path
sys.path.append(os.getcwd())

from config.settings import settings
from utils.llm_factory import LLMFactory
from retriever.builder import RetrieverBuilder

def test_watsonx():
    logger.info("--- Testing WatsonX ---")
    logger.info(f"API KEY (first 5): {settings.WATSONX_APIKEY[:5]}...")
    logger.info(f"PROJECT ID: {settings.WATSONX_PROJECT_ID}")
    
    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
        from langchain_ibm import WatsonxEmbeddings
        
        logger.info("Initializing WatsonX Model...")
        model = LLMFactory.get_llm(model_id="meta-llama/llama-3-2-90b-vision-instruct")
        logger.info("Model initialization success!")
        
        logger.info("Testing Model Chat...")
        resp = model.chat([{"role": "user", "content": "Hello"}])
        logger.info(f"Chat response success: {resp['choices'][0]['message']['content'][:50]}...")
        
        logger.info("Initializing WatsonX Embeddings...")
        builder = RetrieverBuilder()
        # force provider to watsonx for this test
        settings.LLM_PROVIDER = "watsonx"
        builder.__init__()
        logger.info("Embeddings initialization success!")
        
    except Exception as e:
        logger.error(f"WatsonX Test Failed: {e}")

def test_deepseek():
    logger.info("--- Testing DeepSeek ---")
    logger.info(f"API KEY (first 5): {settings.DEEPSEEK_API_KEY[:5]}...")
    
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        
        logger.info("Initializing DeepSeek Model...")
        settings.LLM_PROVIDER = "deepseek"
        model = LLMFactory.get_llm()
        logger.info("Model initialization success!")
        
        logger.info("Testing Model Chat...")
        resp = model.chat([{"role": "user", "content": "Hello"}])
        logger.info(f"Chat response success: {resp['choices'][0]['message']['content'][:50]}...")
        
        logger.info("Initializing DeepSeek Embeddings...")
        builder = RetrieverBuilder()
        builder.__init__()
        logger.info("Embeddings initialization success!")
        
    except Exception as e:
        logger.error(f"DeepSeek Test Failed: {e}")

if __name__ == "__main__":
    logger.info("Starting Diagnostics...")
    test_watsonx()
    print("\n" + "="*50 + "\n")
    test_deepseek()
    logger.info("Diagnostics Complete.")
