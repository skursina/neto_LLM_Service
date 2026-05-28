import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from services.summarizer_service import summarize_text
import logging

# Используем TestClient для интеграционного теста
client = TestClient(app)

# Захватываем логи для анализа
@pytest.fixture(autouse=True)
def capture_logs(caplog):
    caplog.set_level(logging.INFO)
    return caplog


@patch("services.summarizer_service.generate_summary")
@patch("services.summarizer_service.fallback_summary")
@pytest.mark.asyncio
async def test_cache_hit_on_repeat_request(mock_fallback, mock_llm_generate, caplog):
    """
    Проверяет, что повторные запросы с одинаковым текстом приводят к cache hit
    и вызов LLM-модуля происходит только один раз.
    """
    # Подготавливаем моки
    mock_llm_generate.return_value = "This is a test summary."
    mock_fallback.return_value = "Fallback summary: ..."

    # Текст для тестирования
    test_text = "This is a long text for summarization that meets the minimum length requirement."

    # Первый запрос
    with caplog.at_level(logging.INFO):
        caplog.clear()
        response1 = client.post("/summarize", json={"text": test_text})
        
    # Проверяем первый ответ и логи
    assert response1.status_code == 200
    assert "summary" in response1.json()
    assert "Cache miss" in caplog.text  # Должно быть в логах
    
    # Убеждаемся, что был вызов к LLM
    mock_llm_generate.assert_called_once()

    # Второй запрос с тем же текстом
    with caplog.at_level(logging.INFO):
        caplog.clear()
        response2 = client.post("/summarize", json={"text": test_text})
        
    # Проверяем второй ответ и логи
    assert response2.status_code == 200
    assert "summary" in response2.json()
    assert "Cache hit" in caplog.text  # Должно быть в логах
    
    # Убеждаемся, что LLM не был вызван повторно
    mock_llm_generate.assert_called_once()  # Количество вызовов не изменилось

    # Проверяем, что оба ответа одинаковы
    assert response1.json() == response2.json()


@pytest.mark.asyncio
async def test_cache_hit_direct_service_call():
    """
    Альтернативный тест, который проверяет кэш на уровне сервиса.
    """
    test_text = "Another test text for caching."
    
    # Первый вызов
    with patch("services.summarizer_service.generate_summary") as mock_gen:
        mock_gen.return_value = "Service summary."
        
        result1 = await summarize_text(test_text)
        assert isinstance(result1, str)  # Убеждаемся, что результат - строка
        
    # Второй вызов (должен быть cache hit)
    with patch("services.summarizer_service.generate_summary") as mock_gen:
        # Мок не должен быть вызван
        result2 = await summarize_text(test_text)
        mock_gen.assert_not_called()
        assert isinstance(result2, str)  # Убеждаемся, что результат - строка
        
    # Проверяем, что результаты одинаковы
    assert result1 == result2
    
    # Проверка логов не уместна в этом тесте, так как они не возвращаются как результат.