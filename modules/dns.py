# modules/dns.py

import socket
from urllib.parse import urlparse


def lookup(target: str):

    parsed = urlparse(target)
    hostname = parsed.hostname

    try:
        ip = socket.gethostbyname(hostname)
        return {
            "hostname": hostname,
            "ip_address": ip
        }
    except socket.gaierror:
        return {
            "error": "DNS resolution failed"
        }