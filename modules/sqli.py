# modules/sqli.py
from core.http_client import HTTPClient

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' UNION SELECT NULL--"
]

def test(endpoint: str, client: HTTPClient):
    """
    Test SQLi simulé sur un endpoint donné.
    Retourne une finding si payload est reflété.
    """
    findings = []
    for payload in SQLI_PAYLOADS:
        params = {"id": payload}  # paramètre simulé
        try:
            response = client.get(endpoint, params=params)
            if payload in response.text:
                findings.append({
                    "type": "SIMULATED_SQLI",
                    "endpoint": endpoint,
                    "description": f"Payload reflected: {payload}",
                    "severity_score": 8
                })
        except Exception:
            continue
    return findings