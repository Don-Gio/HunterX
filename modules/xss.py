# modules/xss.py
from core.http_client import HTTPClient

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>"
]

def test(endpoint: str, client: HTTPClient):
    """
    Test XSS simulé sur un endpoint donné.
    Retourne une finding si le payload est reflété.
    """
    findings = []
    for payload in XSS_PAYLOADS:
        params = {"input": payload}  # paramètre simulé
        try:
            response = client.get(endpoint, params=params)
            if payload in response.text:
                findings.append({
                    "type": "SIMULATED_XSS",
                    "endpoint": endpoint,
                    "description": f"Payload reflected: {payload}",
                    "severity_score": 7
                })
        except Exception:
            continue
    return findings