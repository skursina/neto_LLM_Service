import re

def fallback_summary(text: str) -> str:
 
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
    short_summary = ". ".join(sentences[:2])
    if not short_summary:
        short_summary = text[:100]
        
    if not short_summary.strip():
        return "Fallback summary: ..."
    short_summary = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', short_summary)
    short_summary = re.sub(r'\s+', ' ', short_summary)
    return f"Fallback summary: {short_summary.strip()}..."