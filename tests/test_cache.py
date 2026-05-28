import pytest
from services.cache_service import get_cached, set_cache

@pytest.mark.asyncio
async def test_cache_set_and_get():
    await set_cache("key1", "val1")
    assert await get_cached("key1") == "val1"


@pytest.mark.asyncio
async def test_cache_miss():
    assert await get_cached("non_existent") is None
