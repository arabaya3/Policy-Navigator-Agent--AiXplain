import aixplain

def aixplain_embed(text):
    try:
        raise NotImplementedError
    except Exception as e:
        print("aiXplain embedding unavailable, using fallback.")
        return [float(ord(c)) for c in text[:384]] + [0.0]*(384-len(text))
def aixplain_summarize(text):
    try:
        raise NotImplementedError
    except Exception as e:
        print("aiXplain summarization unavailable, using fallback.")
        import re
        sentences = re.split(r'(?<=[.!?]) +', text)
        return ' '.join(sentences[:2]) 