# hunterx.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install

from core.config import Config
from core.logger import setup_logger
from core.recon_engine import ReconEngine
from core.attack_surface import AttackSurfaceAnalyzer
from core.vulnerability_engine import VulnerabilityEngine
from core.http_client import HTTPClient
from core.report_engine import ReportEngine
from modules import idor, jwt, debug, ratelimit
from modules import xss, sqli

import sys

console = Console()
install()

BANNER = """
[bold red]
██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗  ██╗  ██╗
██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗ ╚██╗██╔╝
███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝  ╚███╔╝ 
██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗  ██╔██╗ 
██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║ ██╔╝ ██╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═╝  ╚═╝
[/bold red]
[bold]Hunter X – Offensive Bug Bounty Framework[/bold]
"""

def main():
    console.print(Panel(BANNER, expand=False))

    try:
        config = Config()
        logger = setup_logger(config)

        table = Table(title="Scan Configuration", show_lines=True)
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Target", config.target)
        table.add_row("Threads", str(config.threads))
        table.add_row("Deep Recon", str(config.deep))
        table.add_row("Output", config.output)

        console.print(table)

        # Phase 1 – Recon
        recon = ReconEngine(config, logger)
        recon_data = recon.run()

        # Phase 2 – Attack Surface
        surface = AttackSurfaceAnalyzer(recon_data).map()

        # Phase 3 – Vulnerability Engine
        client = HTTPClient(threads=config.threads)
        vuln_engine = VulnerabilityEngine(surface, client, logger)
        findings = vuln_engine.scan()

        # IDOR
        for ep in surface.get("idor_candidates", []):
            idor_result = idor.test(ep, client)
            if idor_result:
                findings.append(idor_result)
                logger.warning(f"IDOR candidate found on {ep}")

        # JWT
        for ep in surface.get("all_endpoints", []):
            jwt_findings = jwt.check(ep, client)
            if jwt_findings:
                findings.extend(jwt_findings)

        # Debug endpoints
        for ep in surface.get("all_endpoints", []):
            debug_result = debug.check(ep, client)
            if debug_result:
                findings.append(debug_result)

        # Rate-limit
        for ep in surface.get("all_endpoints", []):
            rl_result = ratelimit.check(ep, client)
            if rl_result:
                findings.append(rl_result)

        # XSS simulé
        for ep in surface.get("all_endpoints", []):
            xss_findings = xss.test(ep, client)
            if xss_findings:
                findings.extend(xss_findings)
                logger.info(f"Simulated XSS findings on {ep}")

        # SQLi simulé
        for ep in surface.get("all_endpoints", []):
            sqli_findings = sqli.test(ep, client)
            if sqli_findings:
                findings.extend(sqli_findings)
                logger.info(f"Simulated SQLi findings on {ep}")

        # GraphQL
        for ep in surface.get("graphql_endpoints", []):
            findings.append({
                "type": "GRAPHQL_ENDPOINT",
                "endpoint": ep,
                "description": "Potential GraphQL endpoint detected"
            })

        console.print("\n[bold yellow]Findings:[/bold yellow]")
        console.print(findings if findings else "No immediate issues detected.")

        # Report
        reporter = ReportEngine(findings, config.output)
        reporter.generate()

        logger.info("Hunter X execution finished successfully.")

    except Exception as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()