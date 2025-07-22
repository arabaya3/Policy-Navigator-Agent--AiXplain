import requests

def query_federal_register_api(query: str, from_date=None, to_date=None, agency=None, doc_type=None, per_page=1) -> str:
    url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "per_page": per_page,
        "order": "newest",
        "conditions[term]": query
    }
    if from_date:
        params["conditions[publication_date][gte]"] = from_date
    if to_date:
        params["conditions[publication_date][lte]"] = to_date
    if agency:
        params["conditions[agency_names][]"] = agency
    if doc_type:
        params["conditions[type][]"] = doc_type
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                doc = results[0]
                title = doc.get("title", "")
                ql = query.lower()
                if not any(kw in title.lower() for kw in ["executive order", "regulation", "notice"] + ql.split()):
                    return "No relevant federal register documents found."
                summary = doc.get("abstract", "No summary available.")
                pub_date = doc.get("publication_date", "?")
                return f"{title} (Published: {pub_date}): {summary}"
            else:
                return "No relevant federal register documents found."
        else:
            return f"Federal Register: API error (status {resp.status_code})."
    except Exception as e:
        return f"Federal Register: Error fetching data: {e}" 