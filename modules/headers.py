# modules/headers.py

from typing import Dict


SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
]


def analyze(target: str, client) -> Dict:

    response = client.get(target)

    if not response:
        return {"error": "Target unreachable"}

    headers = response.headers
    missing = []

    for header in SECURITY_HEADERS:
        if header not in headers:
            missing.append(header)

    server = headers.get("Server", "Unknown")
    powered_by = headers.get("X-Powered-By", "Unknown")

    return {
        "status_code": response.status_code,
        "server": server,
        "powered_by": powered_by,
        "missing_security_headers": missing,
    }