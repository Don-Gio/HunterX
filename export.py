# json_to_md_final_timestamped.py
import json
import os
from collections import defaultdict
import datetime

# Icônes de gravité
def severity_icon(score):
    if score >= 8:
        return "🔴 High"
    elif score >= 5:
        return "🟠 Medium"
    else:
        return "🟢 Low"

def json_to_markdown(json_file: str, output_folder: str = "reports"):
    """
    Transforme un rapport JSON Hunter X en Markdown enrichi.
    - URLs cliquables
    - Résumé par gravité
    - Fusion des findings par endpoint
    - Horodatage pour ne jamais écraser les rapports
    """
    if not os.path.exists(json_file):
        print(f"[Erreur] Fichier JSON '{json_file}' introuvable.")
        return

    # Création du dossier si nécessaire
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Génération du nom de fichier horodaté
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = os.path.join(output_folder, f"report_{timestamp}.md")

    # Chargement du JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Fusion findings par endpoint
    endpoints = defaultdict(list)
    severity_count = {"High":0, "Medium":0, "Low":0}

    for item in data:
        ep = item.get("endpoint", "Unknown")
        desc = item.get("description", "").replace("|", "\\|")
        score = item.get("severity_score", 0)
        sev_icon = severity_icon(score)
        endpoints[ep].append((item.get("type","Unknown"), desc, sev_icon))

        # Compte pour résumé
        if "High" in sev_icon:
            severity_count["High"] += 1
        elif "Medium" in sev_icon:
            severity_count["Medium"] += 1
        else:
            severity_count["Low"] += 1

    md_lines = []
    md_lines.append("# 🕷️ Hunter X Report\n")
    md_lines.append(f"**Total Findings:** {len(data)}\n")
    md_lines.append(f"**Summary by Severity:** 🔴 High: {severity_count['High']} | 🟠 Medium: {severity_count['Medium']} | 🟢 Low: {severity_count['Low']}\n")
    md_lines.append("---\n")

    # Table finale
    md_lines.append("| Endpoint | Findings | Severity |")
    md_lines.append("|----------|----------|---------|")

    for ep, items in endpoints.items():
        findings_text = "; ".join([f"{t}: {d}" for t,d,_ in items])
        sev_text = "/".join(sorted(set([sev for _,_,sev in items]), reverse=True))
        md_lines.append(f"| [{ep}]({ep}) | {findings_text} | {sev_text} |")

    # Écriture UTF-8
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"[OK] Markdown final généré : {md_file}")


# Exemple d'utilisation
if __name__ == "__main__":
    json_file = "reports/report.json"  # rapport Hunter X
    json_to_markdown(json_file)