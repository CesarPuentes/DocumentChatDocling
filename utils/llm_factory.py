from typing import List, Dict, Any, Union
import os
from config.settings import settings
from langchain_openai import ChatOpenAI
from utils.logging import logger

class LLMInterface:
    """Standard interface for all LLM providers."""
    def chat(self, messages: List[Dict[str, str]], **params) -> Dict[str, Any]:
        """
        Sends a chat request and returns a response in OpenAI-compatible format.
        Expected return structure:
        {
            'choices': [
                {
                    'message': {
                        'content': '...',
                        'role': 'assistant'
                    }
                }
            ]
        }
        """
        raise NotImplementedError

class WatsonXWrapper(LLMInterface):
    def __init__(self, model_id: str, **params):
        try:
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai import Credentials
        except ImportError:
            logger.error("ibm-watsonx-ai not installed. Please install it to use WatsonX.")
            raise ImportError("ibm-watsonx-ai not installed.")

        credentials = Credentials(
            url="https://us-south.ml.cloud.ibm.com",
            api_key=settings.WATSONX_APIKEY
        )
        self.model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=settings.WATSONX_PROJECT_ID,
            params=params
        )

    def chat(self, messages: List[Dict[str, str]], **params) -> Dict[str, Any]:
        # WatsonX ModelInference.chat expects exactly what we receive and returns what we expect
        return self.model.chat(messages=messages, **params)

class OpenAICompatibleWrapper(LLMInterface):
    def __init__(self, provider: str, model_name: str, **params):
        api_key = settings.DEEPSEEK_API_KEY if provider == "deepseek" else settings.OPENAI_API_KEY
        base_url = "https://api.deepseek.com/v1" if provider == "deepseek" else None
        
        if not api_key:
            logger.warning(f"API key for {provider} is missing.")

        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=params.get("temperature", 0.3),
            max_tokens=params.get("max_tokens", 300)
        )

    def chat(self, messages: List[Dict[str, str]], **params) -> Dict[str, Any]:
        # Convert messages to langchain format
        from langchain.schema import HumanMessage, SystemMessage, AIMessage
        
        lc_messages = []
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        response = self.llm.invoke(lc_messages)
        
        # Wrap in OpenAI-compatible dict
        return {
            "choices": [
                {
                    "message": {
                        "content": response.content,
                        "role": "assistant"
                    }
                }
            ]
        }

class OllamaWrapper(LLMInterface):
    def __init__(self, model_name: str, **params):
        # Ollama's local API usually runs at http://localhost:11434/v1 for OpenAI compatibility
        self.llm = ChatOpenAI(
            model=model_name,
            api_key="ollama", # Placeholder for local use
            base_url=settings.OLLAMA_BASE_URL,
            temperature=params.get("temperature", 0.3),
            max_tokens=params.get("max_tokens", 300)
        )

    def chat(self, messages: List[Dict[str, str]], **params) -> Dict[str, Any]:
        # Reuse logic from OpenAICompatibleWrapper or implement directly
        from langchain.schema import HumanMessage, SystemMessage, AIMessage
        lc_messages = []
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        response = self.llm.invoke(lc_messages)
        return {
            "choices": [
                {"message": {"content": response.content, "role": "assistant"}}
            ]
        }

class LLMFactory:
    @staticmethod
    def get_llm(model_id: str = None, **params) -> LLMInterface:
        provider = settings.LLM_PROVIDER.lower()
        logger.info(f"Initializing LLM with provider: {provider}")

        if provider == "watsonx":
            return WatsonXWrapper(model_id=model_id or "meta-llama/llama-3-2-90b-vision-instruct", **params)
        elif provider == "deepseek":
            return OpenAICompatibleWrapper("deepseek", settings.DEEPSEEK_MODEL_NAME, **params)
        elif provider == "openai":
            return OpenAICompatibleWrapper("openai", settings.OPENAI_MODEL_NAME, **params)
        elif provider == "ollama":
            return OllamaWrapper(settings.OLLAMA_MODEL_NAME, **params)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
