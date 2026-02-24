# modules/ssl.py

import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse


def inspect(target: str):

    parsed = urlparse(target)
    hostname = parsed.hostname
    port = 443

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                tls_version = ssock.version()

        expires = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

        return {
            "tls_version": tls_version,
            "issuer": dict(x[0] for x in cert["issuer"]),
            "expires": expires.isoformat(),
            "expired": expires < datetime.utcnow()
        }

    except Exception as e:
        return {
            "error": str(e)
        }