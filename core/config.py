# core/config.py

import argparse
import re
from urllib.parse import urlparse


class Config:

    def __init__(self):
        self.args = self._parse_args()

        self.target = self._validate_target(self.args.target)
        self.threads = self.args.threads
        self.deep = self.args.deep
        self.output = self.args.output

    def _parse_args(self):
        parser = argparse.ArgumentParser(
            description="Hunter X - Offensive Bug Bounty CLI"
        )

        parser.add_argument(
            "target",
            help="Target domain or URL"
        )

        parser.add_argument(
            "--threads",
            type=int,
            default=10,
            help="Number of concurrent threads"
        )

        parser.add_argument(
            "--deep",
            action="store_true",
            help="Enable deep reconnaissance"
        )

        parser.add_argument(
            "--output",
            default="reports/report.json",
            help="Output report file"
        )

        return parser.parse_args()

    def _validate_target(self, target):
        parsed = urlparse(target)

        if not parsed.scheme:
            target = "https://" + target
            parsed = urlparse(target)

        if not parsed.netloc:
            raise ValueError("Invalid target format.")

        if not re.match(r"^[a-zA-Z0-9\.\-:]+$", parsed.netloc):
            raise ValueError("Target contains invalid characters.")

        return target