import pytest
from unittest.mock import AsyncMock, patch
from openai._exceptions import APITimeoutError, APIConnectionError
from tenacity import RetryError

from llm.exceptions import LLMTimeoutError, LLMConnectionError, InvalidLLMResponseError
from llm.client import generate_summary

@pytest.mark.asyncio
async def test_generate_summary_success():
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock(message=AsyncMock(content="Test summary"))]
    
    with patch("llm.client.client") as mock_client:
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        result = await generate_summary("Test text")
        assert result == "Test summary"

@pytest.mark.asyncio
async def test_generate_summary_timeout():
    with patch("llm.client.client") as mock_client:
        # Создаем полноценный объект ошибки
        mock_client.chat.completions.create = AsyncMock(side_effect=APITimeoutError(request=None))
        with pytest.raises(RetryError) as exc_info:
            await generate_summary("Test text")
        # Проверяем, что исходное исключение (APITimeoutError) находится в цепочке
        assert isinstance(exc_info.value.__cause__, LLMTimeoutError)

@pytest.mark.asyncio
async def test_generate_summary_connection_error():
    with patch("llm.client.client") as mock_client:
        # Создаем полноценный объект ошибки
        mock_client.chat.completions.create = AsyncMock(side_effect=APIConnectionError(request=None))
        with pytest.raises(RetryError) as exc_info:
            await generate_summary("Test text")
        # Проверяем, что исходное исключение (APIConnectionError) находится в цепочке
        assert isinstance(exc_info.value.__cause__, LLMConnectionError)

@pytest.mark.asyncio
async def test_generate_summary_invalid_response():
    mock_response = AsyncMock()
    mock_response.choices = []
    
    with patch("llm.client.client") as mock_client:
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        with pytest.raises(InvalidLLMResponseError):
            await generate_summary("Test text")