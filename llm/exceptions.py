class LLMServiceError(Exception):
    """Base LLM exception"""


class LLMTimeoutError(LLMServiceError):
    """LLM timeout"""


class LLMConnectionError(LLMServiceError):
    """LLM connection error"""


class InvalidLLMResponseError(LLMServiceError):
    """Invalid LLM response"""