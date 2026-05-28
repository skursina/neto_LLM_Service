import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
import os
# Добавляем путь к корню проекта, чтобы можно было импортировать модули
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_validation_error():
    response = client.post("/summarize", json={"text": "short"})
    assert response.status_code == 422

@pytest.mark.asyncio
@patch("services.summarizer_service.summarize_text", return_value="Mocked summary")
async def test_success_request(mock_summarize):
    response = client.post("/summarize", json={"text": "This is a valid text for testing purposes. It is long enough to meet the minimum length requirement of 50 characters that is defined in the Pydantic model for the API request."})
    assert response.status_code == 200
    assert "summary" in response.json()