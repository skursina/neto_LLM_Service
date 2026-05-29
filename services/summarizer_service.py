import hashlib
import logging

from llm.client import generate_summary

from services.cache_service import (get_cached, set_cache)
from services.fallback_service import (fallback_summary)
from llm.exceptions import LLMServiceError

logger = logging.getLogger(__name__)


def build_cache_key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


async def summarize_text(text: str) -> str:
    logger.info("Summarization started")

    cache_key = build_cache_key(text)
    cached = await get_cached(cache_key)

    if cached:
        return cached

    try:
        summary = await generate_summary(text)
        summary = clean_summary(summary)
        await set_cache(cache_key, summary)
        logger.info("Summarization completed")
        return summary

    except LLMServiceError:
        logger.warning("LLM unavailable, using fallback")
        return fallback_summary(text)

    except Exception as e:
        logger.exception(f"Unexpected service error: {e}")
        return fallback_summary(text)


def clean_summary(summary: str) -> str:
    return (summary.replace("\n", " ").strip())