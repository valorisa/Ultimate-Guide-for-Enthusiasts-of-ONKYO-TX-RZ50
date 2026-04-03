<!-- markdownlint-disable MD013 MD041 -->
# Ultimate Guide for Enthusiasts of ONKYO TX-RZ50

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50)
![GitHub last commit](https://img.shields.io/github/last-commit/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Sphinx](https://img.shields.io/badge/Docs-Sphinx-green)

> 🎯 **Objectif** : Ce dépôt constitue la ressource ultime, exhaustive et pédagogique pour les passionnés, audiophiles, intégrateurs domotiques et développeurs souhaitant exploiter le plein potentiel du récepteur AV **ONKYO TX-RZ50**. Il combine documentation technique détaillée, scripts fonctionnels prêts à l'emploi, et architecture open source professionnelle.

---

## 📋 Table des matières

- [🎯 Présentation du projet](#-présentation-du-projet)
- [👥 Public cible](#-public-cible)
- [📦 Contenu du dépôt](#-contenu-du-dépôt)
- [🚀 Démarrage rapide](#-démarrage-rapide)
- [🔧 Installation détaillée](#-installation-détaillée)
- [📚 Documentation technique](#-documentation-technique)
- [🐍 Scripts Python fonctionnels](#-scripts-python-fonctionnels)
- [🐳 Déploiement Docker](#-déploiement-docker)
- [📖 Documentation Sphinx](#-documentation-sphinx)
- [🤝 Contribution](#-contribution)
- [⚖️ Licence & Attribution](#-licence--attribution)
- [🙏 Remerciements](#-remerciements)

---

## 🎯 Présentation du projet

Le **ONKYO TX-RZ50** est un récepteur AV haut de gamme 9.2 canaux, compatible Dolby Atmos, DTS:X, THX Certified, et équipé de fonctionnalités réseau avancées (AirPlay 2, Spotify Connect, Chromecast built-in, Roon Ready). Ce projet vise à :

1. **Documenter de manière exhaustive** chaque fonctionnalité du manuel officiel, avec une approche pédagogique à deux niveaux :
   - 🟢 **Pour les débutants** : explications simplifiées, analogies, checklists pas-à-pas.
   - 🔵 **Pour les experts** : spécifications techniques brutes, pièges de configuration, optimisations avancées.

2. **Fournir des outils fonctionnels** pour l'automatisation domotique (Home Assistant, Node-RED, etc.) via des scripts Python bien documentés.

3. **Structurer un dépôt open source professionnel** avec CI/CD, documentation auto-générée, et bonnes pratiques de développement.

> ℹ️ **Note juridique** : Ce projet contient des extraits du manuel ONKYO TX-RZ50, © Onkyo Home Entertainment Corporation. Leur inclusion relève du fair use à des fins éducatives et de documentation technique. Le code et la structure du projet sont sous licence MIT.

---

## 👥 Public cible

| Profil | Bénéfices attendus |
|--------|-------------------|
| 🟢 **Débutant en audio** | Comprendre les bases du branchement, configuration initiale, utilisation quotidienne sans jargon technique. |
| 🔵 **Audiophile mélomane** | Optimiser la calibration Dirac Live, comprendre les modes d'écoute THX, exploiter les formats lossless. |
| ⚙️ **Intégrateur domotique** | Automatiser le TX-RZ50 via RS-232/HTTP, intégrer avec Home Assistant, créer des scénarios multizone. |
| 💻 **Développeur open source** | Contribuer au projet, améliorer les scripts, étendre la documentation, proposer des fonctionnalités. |

---

## 📦 Contenu du dépôt

```text
Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50/
├── 📁 docs/
│   ├── 📁 source/                 # Fichiers Sphinx (.rst/.md)
│   ├── 📄 conf.py                 # Configuration Sphinx
│   └── 📄 index.rst               # Page d'accueil de la doc
├── 📁 scripts/
│   ├── 📄 rs232_control.py        # Contrôle série RS-232 (allumage, source, volume)
│   ├── 📄 http_api_wrapper.py     # Wrapper API HTTP/Web Setup du TX-RZ50
│   ├── 📄 log_parser.py           # Analyseur de logs série/HTTP, export CSV/JSON
│   ├── 📄 firmware_checker.py     # Vérification version firmware via réseau
│   └── 📄 requirements.txt        # Dépendances Python
├── 📁 docker/
│   ├── 📄 Dockerfile              # Image Python 3.11-slim, non-root, HEALTHCHECK
│   └── 📄 docker-compose.yml      # Services onkyo-control + onkyo-docs
├── 📁 config/
│   └── 📄 home_assistant.yaml     # Exemple d'intégration HA (MQTT/HTTP)
├── 📁 .github/
│   └── 📁 ISSUE_TEMPLATE/
│       ├── 📄 bug_report.md
│       ├── 📄 doc_suggestion.md
│       └── 📄 feature_request.md
├── 📄 README.md
├── 📄 LICENSE
├── 📄 ATTRIBUTION.md
├── 📄 CONTRIBUTING.md
└── 📄 requirements-docs.txt
```

---

## 🚀 Démarrage rapide

### Prérequis
- ✅ Windows 11 Enterprise / PowerShell 7.6+
- ✅ Git, GitHub CLI (`gh`), Python 3.11+
- ✅ Docker Desktop (optionnel pour la conteneurisation)
- ✅ Accès réseau au TX-RZ50 (Wi-Fi ou Ethernet)

### Commandes essentielles
```powershell
# 1. Environnement virtuel Python
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Installation des dépendances
pip install -r scripts/requirements.txt
pip install -r requirements-docs.txt

# 3. Tester un script
python scripts/rs232_control.py --help

# 4. Générer la documentation locale (Sphinx)
cd docs && make html
```

> 📖 **Note** : La documentation technique détaillée (Installation, Raccordements, Calibration, Modes d'écoute, Multizone, Dépannage) sera peuplée automatiquement via l'assistant IA calibré sur le manuel officiel. Consultez `/docs/source/` après clonage.



