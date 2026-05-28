from services.fallback_service import fallback_summary

def test_basic_fallback():
    text = "First sentence. Second sentence! Third one?"
    result = fallback_summary(text)
    assert result.startswith("Fallback summary: ")
    assert "First sentence" in result
    assert len(result) > 0

def test_empty_text_fallback():
    result = fallback_summary("   .  ?  ")
    assert result == "Fallback summary: ..."