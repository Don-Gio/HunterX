# modules/js_analysis.py

import re
from urllib.parse import urljoin
from core.http_client import HTTPClient

GRAPHQL_KEYWORDS = ["graphql", "query", "mutation", "gql"]

def extract_graphql_endpoints(target: str, client: HTTPClient) -> list:
    """
    Analyse les JS pour détecter les endpoints GraphQL.
    """
    discovered = set()

    response = client.get(target)
    if not response:
        return []

    # JS files
    js_files = re.findall(r'src=["\'](.*?\.js)["\']', response.text)
    for js in js_files:
        js_url = urljoin(target, js)
        js_resp = client.get(js_url)
        if not js_resp:
            continue

        for line in js_resp.text.splitlines():
            for keyword in GRAPHQL_KEYWORDS:
                if keyword in line.lower():
                    # Tentative d'extraction endpoint
                    url_match = re.search(r'https?://[^\s\'"]+', line)
                    if url_match:
                        discovered.add(url_match.group(0))

    return list(discovered)