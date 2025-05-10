from urllib.parse import urlparse

def url_to_dict(url: str) -> dict:
    parsed = urlparse(url)
    return {
        "netloc": parsed.netloc,
        "path": " ".join([str(s) for s in parsed.path.split("/")]),
        "query": parsed.query
    }