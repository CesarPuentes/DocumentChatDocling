import unittest
from unittest.mock import MagicMock, patch
from utils.llm_factory import LLMFactory, WatsonXWrapper, OpenAICompatibleWrapper
from config.settings import settings

class TestLLMFactory(unittest.TestCase):

    @patch('utils.llm_factory.WatsonXWrapper')
    def test_get_llm_watsonx(self, MockWatsonX):
        settings.LLM_PROVIDER = "watsonx"
        llm = LLMFactory.get_llm()
        MockWatsonX.assert_called_once()
        self.assertIsInstance(llm, MagicMock)

    @patch('utils.llm_factory.OpenAICompatibleWrapper')
    def test_get_llm_deepseek(self, MockOpenAI):
        settings.LLM_PROVIDER = "deepseek"
        llm = LLMFactory.get_llm()
        MockOpenAI.assert_called_with("deepseek", "deepseek-chat")
        self.assertIsInstance(llm, MagicMock)

    @patch('utils.llm_factory.OpenAICompatibleWrapper')
    def test_get_llm_openai(self, MockOpenAI):
        settings.LLM_PROVIDER = "openai"
        llm = LLMFactory.get_llm()
        MockOpenAI.assert_called_with("openai", "gpt-4o-mini")
        self.assertIsInstance(llm, MagicMock)

    @patch('utils.llm_factory.OllamaWrapper')
    def test_get_llm_ollama(self, MockOllama):
        settings.LLM_PROVIDER = "ollama"
        llm = LLMFactory.get_llm()
        MockOllama.assert_called_with("llama3")
        self.assertIsInstance(llm, MagicMock)

    def test_invalid_provider(self):
        settings.LLM_PROVIDER = "invalid"
        with self.assertRaises(ValueError):
            LLMFactory.get_llm()

class TestOpenAICompatibleWrapper(unittest.TestCase):
    @patch('utils.llm_factory.ChatOpenAI')
    @patch('utils.llm_factory.settings')
    def test_openai_wrapper_chat(self, mock_settings, MockChatOpenAI):
        mock_settings.OPENAI_API_KEY = "test_key"
        mock_settings.OPENAI_MODEL_NAME = "gpt-4"
        
        # Setup mock response
        mock_instance = MockChatOpenAI.return_value
        mock_response = MagicMock()
        mock_response.content = "Hello world"
        mock_instance.invoke.return_value = mock_response

        wrapper = OpenAICompatibleWrapper("openai", "gpt-4")
        messages = [{"role": "user", "content": "Hi"}]
        response = wrapper.chat(messages)

        self.assertEqual(response['choices'][0]['message']['content'], "Hello world")
        self.assertEqual(response['choices'][0]['message']['role'], "assistant")

if __name__ == '__main__':
    unittest.main()
