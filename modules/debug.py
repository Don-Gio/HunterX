# modules/debug.py

from typing import Optional

DEBUG_KEYWORDS = ["debug", "phpinfo", "test", "status", "env"]

def check(endpoint: str, client) -> Optional[dict]:
    """
    Vérifie la présence d’endpoints de debug exposés.
    """

    response = client.get(endpoint)
    if not response:
        return None

    for keyword in DEBUG_KEYWORDS:
        if keyword in endpoint.lower():
            return {
                "type": "DEBUG_ENDPOINT",
                "endpoint": endpoint,
                "description": f"Debug-related endpoint detected: {keyword}"
            }

    return None