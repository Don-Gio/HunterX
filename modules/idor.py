# modules/idor.py

import re
from urllib.parse import urlparse, parse_qs, urljoin

# Patterns ID-like
ID_PATTERNS = [
    r"id=\d+",
    r"user=\d+",
    r"account=\d+",
    r"uid=\d+",
    r"/user/\d+",
]


def test(endpoint: str, client):
    """
    Test léger IDOR en détectant des patterns paramétriques simples.
    Ne fait pas de brute-force, juste détection.
    """

    response = client.get(endpoint)
    if not response:
        return None

    for pattern in ID_PATTERNS:
        if re.search(pattern, endpoint):
            return {
                "type": "IDOR_CANDIDATE",
                "endpoint": endpoint,
                "description": f"Endpoint appears to accept ID-like parameter matching {pattern}"
            }

    return None