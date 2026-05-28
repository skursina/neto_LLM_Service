import asyncio
import logging

from openai import AsyncOpenAI
from openai._exceptions import APITimeoutError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import settings
from llm.prompts import SYSTEM_PROMPT
from llm.exceptions import (LLMTimeoutError, LLMConnectionError, InvalidLLMResponseError)


logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    base_url = settings.llm_base_url, 
    api_key=settings.openai_api_key
    )

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((LLMTimeoutError, LLMConnectionError)))
async def generate_summary(text: str) -> str:
    logger.info("Sending request to OpenAI")
    
    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=settings.llm_temperature,
                timeout=settings.request_timeout
            ),
            timeout=settings.request_timeout    
        )

    except APITimeoutError as e:
        logger.error(f"OpenAI timeout: {e}")
        raise LLMTimeoutError("Превышено время ожидания ответа от LLM") from e

    except APIConnectionError as e:
        logger.error(f"OpenAI connection error: {e}")
        raise LLMConnectionError("Ошибка соединения с LLM провайдером") from e

    except Exception as e:
        logger.exception(f"Unexpected OpenAI error: {e}")
        raise

    try:
        result = response.choices[0].message.content
        if not result:
            raise InvalidLLMResponseError("Получен пустой ответ от LLM")
        logger.info("OpenAI response received")
        return result.strip()

    except (IndexError, AttributeError) as e:
        logger.error(f"Invalid LLM response structure: {e}")
        raise InvalidLLMResponseError("Некорректная структура ответа LLM") from e