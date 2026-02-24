import json
import os
from core.smart_scoring import score
from rich.console import Console

console = Console()

class ReportEngine:

    def __init__(self, findings, output_file="reports/report.json"):
        self.findings = findings
        self.output_file = output_file

        # Création automatique du dossier reports/
        folder = os.path.dirname(self.output_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

    def generate(self):
        formatted = []

        for f in self.findings:
            formatted.append({
                "type": f["type"],
                "description": f["description"],
                "endpoint": f.get("endpoint"),
                "severity_score": score(f["type"])
            })

        with open(self.output_file, "w") as file:
            json.dump(formatted, file, indent=4)

        console.print(f"[bold green]Report saved to {self.output_file}[/bold green]")