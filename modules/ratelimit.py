# modules/ratelimit.py

import time

def check(endpoint: str, client, attempts: int = 5) -> dict:
    """
    Test rapide de faille de rate-limit.
    Envoie plusieurs requêtes et vérifie la limitation.
    """

    success_count = 0
    for _ in range(attempts):
        resp = client.get(endpoint)
        if resp and resp.status_code < 400:
            success_count += 1
        time.sleep(0.1)  # court délai pour ne pas spammer

    if success_count == attempts:
        return {
            "type": "RATE_LIMIT_WEAK",
            "endpoint": endpoint,
            "description": f"No rate-limit detected after {attempts} requests"
        }

    return None