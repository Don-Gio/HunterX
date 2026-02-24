# core/http_client.py

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional


class HTTPClient:

    def __init__(self, threads: int = 10, timeout: int = 10):
        self.session = requests.Session()
        self.timeout = timeout
        self._configure_retries()
        self.session.headers.update({
            "User-Agent": "HunterX-Offensive-Framework/1.0"
        })

    def _configure_retries(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url: str, headers: Optional[dict] = None):
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            return response
        except requests.RequestException:
            return None

    def options(self, url: str, headers: Optional[dict] = None):
        try:
            response = self.session.options(
                url,
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.RequestException:
            return None