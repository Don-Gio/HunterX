# modules/cors.py

from typing import Optional


EVIL_ORIGIN = "https://evil.com"


def check(endpoint: str, client) -> Optional[dict]:

    headers = {
        "Origin": EVIL_ORIGIN
    }

    response = client.get(endpoint, headers=headers)

    if not response:
        return None

    acao = response.headers.get("Access-Control-Allow-Origin")
    acc = response.headers.get("Access-Control-Allow-Credentials")

    if not acao:
        return None

    # Wildcard
    if acao == "*":
        return {
            "type": "CORS_WILDCARD",
            "endpoint": endpoint,
            "description": "Access-Control-Allow-Origin set to wildcard (*)"
        }

    # Reflection
    if acao == EVIL_ORIGIN:
        if acc == "true":
            return {
                "type": "CORS_CREDENTIALS_REFLECTION",
                "endpoint": endpoint,
                "description": "CORS reflects arbitrary origin with credentials enabled"
            }
        return {
            "type": "CORS_REFLECTION",
            "endpoint": endpoint,
            "description": "CORS reflects arbitrary origin"
        }

    return None