# 🕷️ Hunter X

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/HunterX)

**Hunter X** est un framework modulaire pour la recherche de vulnérabilités dans un environnement légal (Bug Bounty, lab personnel, API autorisées).  

Il automatise la détection de vulnérabilités et génère des rapports JSON et Markdown horodatés.

---

## 🎯 Objectif

- Automatiser le workflow Bug Bounty : Recon → Surface → Vulnerabilities → Reports  
- Détecter des vulnérabilités exploitables légalement  
- Générer des rapports lisibles et historisés  
- Fournir un environnement légal pour **XSS et SQLi simulés**

---

## ⚠️ Disclaimer

Utilisez Hunter X **uniquement** sur :

- Environnements autorisés  
- Laboratoires de test personnels  
- Programmes Bug Bounty (ex : [HackerOne](https://www.hackerone.com))  

Toute utilisation non autorisée est **illégale**.

---

## 🏗️ Architecture complète

```text
HunterX/
│
├── hunterx.py              # CLI principal
│
├── core/
│   ├── config.py
│   ├── logger.py
│   ├── http_client.py
│   ├── recon_engine.py
│   ├── attack_surface.py
│   ├── vulnerability_engine.py
│   ├── smart_scoring.py
│   └── report_engine.py
│
├── modules/
│   ├── headers.py
│   ├── ssl.py
│   ├── dns.py
│   ├── endpoints.py
│   ├── cors.py
│   ├── idor.py
│   ├── jwt.py
│   ├── debug.py
│   ├── ratelimit.py
│   ├── js_analysis.py
│   ├── xss.py                # Injection simulée XSS
│   ├── sqli.py               # Injection simulée SQLi
│
├── reports/
│   ├── report_20260224_153210.json
│   ├── report_20260224_153210.md
│
├── export.py                # JSON → Markdown
│
└── README.md
```
## 🚀 Installation
  1️⃣ Cloner le projet
```bash
git clone https://github.com/yourusername/HunterX.git
cd HunterX
```
  2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```
  3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```
## 🧪 Utilisation
Scan simple
```bash
python hunterx.py https://target.com
```
Export Markdown
```bash
python export.py
```
Les rapports sont générés dans reports/ avec horodatage, aucun écrasement.

## 🔍 Vulnérabilités détectées

* CORS Misconfiguration
* Rate Limit Weakness
* Security Headers
* IDOR
* JWT misconfiguration
* Debug endpoints exposés
* JS Analysis / Sensitive endpoints
* Injection simulée (XSS & SQLi) – environnement légal uniquement

## 📄 Rapports

> JSON structuré → lecture machine
> Markdown lisible → partage et suivi humain
> Historisation horodatée → pas d’écrasement

Exemple :
```text
reports/report_20260224_153210.json
reports/report_20260224_153210.md
```

## 🧠 Philosophie

* Simplicité : pipeline clair Recon → Surface → Vulnerabilities → Reports
* Lisibilité : modules et rapports clairs
* Évolutivité : ajout facile de modules supplémentaires

## 🛣️ Roadmap
**Version actuelle**

* Modules : headers, SSL, DNS, endpoints, CORS, IDOR, JWT, Debug, Rate-limit, JS Analysis, XSS, SQLi
* Reporting JSON et Markdown horodaté

**Futures évolutions**

* Multi-thread / Async pour scans rapides
* Analyse SSL avancée et WAF detection
* Export CSV / PDF
* Filtres CLI par module ou gravité
* Mode stealth / pentest professionnel

## 📊 Schéma d’architecture (ASCII simplifié)
```text
+--------------------+
|    hunterx.py CLI  |
+--------------------+
           |
           v
+--------------------+
|       core/        |
| Recon, Vuln, Logger|
+--------------------+
           |
           v
+--------------------+
|     modules/       |
| headers, cors, ... |
+--------------------+
           |
           v
+--------------------+
|     reports/       |
| JSON + Markdown    |
+--------------------+
```
## 👨‍💻 Auteur

Don-Gio
Bug Bounty & Offensive Security 
