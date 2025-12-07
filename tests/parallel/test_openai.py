import os
import pytest
from pydantic import BaseModel

from scikufu.parallel.openai import Client

MODEL = "gpt-4.1-nano"


@pytest.fixture
def api_key():
    """Get API key from environment variable"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set in environment variables")
    return api_key


@pytest.fixture
def base_url():
    """Get base URL from environment variable"""
    return os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


@pytest.fixture
def client(api_key, base_url):
    """Create a Client instance for testing"""
    return Client(api_key=api_key, base_url=base_url)


class TestClient:
    """Test suite for OpenAI Client"""

    def test_client_initialization(self, api_key, base_url):
        """Test that Client initializes correctly with provided parameters"""
        client = Client(api_key=api_key, base_url=base_url)
        assert client.api_key == api_key
        assert client.base_url == base_url
        assert client.OpenAI is not None

    def test_client_initialization_default_base_url(self, api_key):
        """Test that Client uses default base_url when not provided"""
        client = Client(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://api.openai.com/v1"

    def test_client_openai_client_created(self, client):
        """Test that AsyncOpenAI client is created"""
        assert client.OpenAI is not None
        assert hasattr(client.OpenAI, "chat")

    def test_chat_completion_single_message(self, client):
        """Test chat_completion with a single message"""
        messages = [
            [
                {"role": "user", "content": "What is 2+2?"},
            ]
        ]
        model = MODEL

        result = client.chat_completion(
            messages=messages,
            model=model,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 1

    def test_chat_completion_with_custom_parameters(self, client):
        """Test chat_completion with custom parameters like temperature"""
        messages = [
            [{"role": "user", "content": "What is 1+1?"}],
        ]
        model = MODEL

        result = client.chat_completion(
            messages=messages,
            model=model,
            temperature=0.5,
            max_tokens=50,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 1

    def test_chat_completion_parse_with_valid_model(self, client):
        """Test chat_completion_parse with a valid Pydantic model"""

        class MathAnswer(BaseModel):
            answer: int
            explanation: str

        messages = [
            [
                {
                    "role": "user",
                    "content": "What is 2+2? Reply in JSON format with fields 'answer' and 'explanation'.",
                }
            ],
        ]
        model = MODEL

        result = client.chat_completion_parse(
            messages=messages,
            model=model,
            response_format=MathAnswer,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 1

    def test_chat_completion_parse_multiple_messages(self, client):
        """Test chat_completion_parse with multiple messages"""

        class SimpleResponse(BaseModel):
            response: str

        messages = [
            [
                {
                    "role": "user",
                    "content": "Say hello. Reply as JSON with field 'response'.",
                }
            ],
            [
                {
                    "role": "user",
                    "content": "Say goodbye. Reply as JSON with field 'response'.",
                }
            ],
        ]
        model = MODEL

        result = client.chat_completion_parse(
            messages=messages,
            model=model,
            response_format=SimpleResponse,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 2

    def test_chat_completion_with_retries(self, client):
        """Test chat_completion with retry parameters"""
        messages = [
            [{"role": "user", "content": "What is 5+5?"}],
        ]
        model = MODEL

        result = client.chat_completion(
            messages=messages,
            model=model,
            retries=1,
            retry_delay=0.5,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 1

    def test_chat_completion_with_cache_dir(self, client, tmp_path):
        """Test chat_completion with cache directory"""
        messages = [
            [{"role": "user", "content": "What is 10+10?"}],
        ]
        model = MODEL
        cache_dir = str(tmp_path / "cache")

        result = client.chat_completion(
            messages=messages,
            model=model,
            cache_dir=cache_dir,
            n_jobs=1,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 1

    def test_chat_completion_parallel_execution(self, client):
        """Test chat_completion with parallel execution (n_jobs > 1)"""
        messages = [[{"role": "user", "content": f"Question {i}?"}] for i in range(3)]
        model = MODEL

        result = client.chat_completion(
            messages=messages,
            model=model,
            n_jobs=3,
            with_tqdm=False,
        )

        assert result is not None
        assert len(result) == 3
