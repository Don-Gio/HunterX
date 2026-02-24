# core/recon_engine.py

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from modules import headers, ssl, dns, endpoints
from core.http_client import HTTPClient


console = Console()


class ReconEngine:

    def __init__(self, config, logger):
        self.target = config.target
        self.deep = config.deep
        self.logger = logger
        self.client = HTTPClient(threads=config.threads)
        self.data = {}

    def run(self):

        console.print("\n[bold cyan]Phase 1 – Deep Recon[/bold cyan]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:

            task_headers = progress.add_task("Analyzing HTTP headers...", total=None)
            self.data["headers"] = headers.analyze(self.target, self.client)
            progress.update(task_headers, completed=1)

            task_ssl = progress.add_task("Inspecting SSL/TLS...", total=None)
            self.data["ssl"] = ssl.inspect(self.target)
            progress.update(task_ssl, completed=1)

            task_dns = progress.add_task("Resolving DNS...", total=None)
            self.data["dns"] = dns.lookup(self.target)
            progress.update(task_dns, completed=1)

            if self.deep:
                task_endpoints = progress.add_task("Harvesting endpoints...", total=None)
                self.data["endpoints"] = endpoints.extract(self.target, self.client)
                progress.update(task_endpoints, completed=1)

        self.logger.info("Recon phase completed.")

        return self.data