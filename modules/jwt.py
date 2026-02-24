# modules/jwt.py

import requests

def check(endpoint: str, client) -> dict:
    """
    Vérifie la présence de JWT mal configurés.
    - Tokens exposés dans headers ou cookies
    - Algorithmes faibles (HS256 par défaut)
    """

    response = client.get(endpoint)
    if not response:
        return {}

    findings = []

    # Exemple simplifié : détection de token dans cookies ou headers
    cookies = response.cookies.get_dict()
    auth_header = response.headers.get("Authorization", "")

    if "jwt" in cookies:
        findings.append({
            "type": "JWT_EXPOSED_COOKIE",
            "endpoint": endpoint,
            "description": "JWT token exposed in cookie"
        })

    if auth_header.lower().startswith("bearer "):
        findings.append({
            "type": "JWT_AUTH_HEADER",
            "endpoint": endpoint,
            "description": "JWT token present in Authorization header"
        })

    return findings