# core/attack_surface.py

from modules import js_analysis
from core.http_client import HTTPClient

class AttackSurfaceAnalyzer:

    def __init__(self, recon_data):
        self.recon = recon_data

    def map(self):
        surface = {
            "all_endpoints": [],
            "auth_endpoints": [],
            "admin_endpoints": [],
            "idor_candidates": [],
            "graphql_endpoints": []
        }

        endpoints = self.recon.get("endpoints", [])
        client = HTTPClient()  # Client centralisé

        for ep in endpoints:
            surface["all_endpoints"].append(ep)

            if any(x in ep.lower() for x in ["login", "auth", "signin", "token"]):
                surface["auth_endpoints"].append(ep)

            if any(x in ep.lower() for x in ["admin", "dashboard", "manage"]):
                surface["admin_endpoints"].append(ep)

            if any(x in ep.lower() for x in ["id=", "user=", "account=", "/user/", "/api/"]):
                surface["idor_candidates"].append(ep)

        # GraphQL detection
        graphql_candidates = js_analysis.extract_graphql_endpoints(
            self.recon.get("target", ""), client
        )
        surface["graphql_endpoints"].extend(graphql_candidates)

        return surface