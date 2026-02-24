# core/smart_scoring.py

SEVERITY_MATRIX = {
    "CORS_WILDCARD": 6.5,
    "CORS_REFLECTION": 7.5,
    "CORS_CREDENTIALS_REFLECTION": 9.0,
    "IDOR_CANDIDATE": 8.5,
}


def score(finding_type: str) -> float:
    return SEVERITY_MATRIX.get(finding_type, 3.0)