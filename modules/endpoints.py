# modules/endpoints.py

import re
from urllib.parse import urljoin


ENDPOINT_REGEX = re.compile(
    r"""(?:"|')(
        (?:\/[a-zA-Z0-9_\-\/\?=&\.]+)
    )(?:"|')""",
    re.VERBOSE
)


def extract(target: str, client):

    discovered = set()

    response = client.get(target)
    if not response:
        return []

    # Extract from main HTML
    matches = ENDPOINT_REGEX.findall(response.text)
    for match in matches:
        full_url = urljoin(target, match)
        discovered.add(full_url)

    # Extract JS files
    js_files = re.findall(r'src=["\'](.*?\.js)["\']', response.text)

    for js in js_files:
        js_url = urljoin(target, js)
        js_response = client.get(js_url)

        if js_response:
            js_matches = ENDPOINT_REGEX.findall(js_response.text)
            for match in js_matches:
                full_url = urljoin(target, match)
                discovered.add(full_url)

    return list(discovered)