import requests
from config import COURTLISTENER_API_KEY
def query_caselaw_api(query: str, statute=None, party=None, keyword=None, from_date=None, to_date=None, per_page=1) -> str:
    url = "https://www.courtlistener.com/api/rest/v3/opinions/"
    params = {"search": query, "page_size": per_page}
    if statute:
        params["statutes"] = statute
    if party:
        params["party"] = party
    if keyword:
        params["search"] = keyword
    if from_date:
        params["date_filed_min"] = from_date
    if to_date:
        params["date_filed_max"] = to_date
    headers = {'Authorization': f'Token {COURTLISTENER_API_KEY}'}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('results', [])
            if results:
                opinion = results[0]
                case_name = (
                    opinion.get('caseName') or
                    opinion.get('case_name') or
                    opinion.get('name_abbreviation') or
                    "Unknown Case"
                )
                ql = query.lower()
                if not any(kw in case_name.lower() for kw in ["roommates.com", "fair housing", "license", "court", "decision"] + ql.split()):
                    return "No relevant court opinions found."
                cite = (
                    opinion.get('cite') or
                    (opinion.get('citations') and opinion.get('citations')[0].get('cite')) or
                    "No citation"
                )
                url = opinion.get('absolute_url') or opinion.get('resource_uri') or ""
                summary = opinion.get('plain_text', '').strip()
                if not summary:
                    summary = "[No summary available]"
                snippet = summary[:300].replace('\n', ' ')
                if case_name == "Unknown Case" and cite == "No citation" and url:
                    return f"{snippet}... [See opinion]({url})"
                else:
                    return f"{case_name} ({cite}): {snippet}..."
            else:
                return "No relevant court opinions found."
        else:
            return f"CourtListener: API error (status {resp.status_code})."
    except Exception as e:
        return f"CourtListener: Error fetching data: {e}" 