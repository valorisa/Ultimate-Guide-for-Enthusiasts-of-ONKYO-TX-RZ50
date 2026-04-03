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


## 📚 Documentation technique

| Guide | Description | Pages du manuel |
|-------|-------------|----------------|
| [🔧 Installation & Branchement](docs/guides/installation.md) | Sécurité, câblage enceintes, HDMI, consommation | p.7-77 |
| [⚙️ Configuration & Calibration](docs/guides/configuration.md) | AccuEQ, Dirac Live, réglages audio avancés | p.124-167 |
| [🎧 Modes d'écoute](docs/guides/modes_ecoute.md) | Dolby Atmos, DTS:X, THX, effets par usage | p.89, 183-198 |
| [🛠️ Dépannage & Codes erreur](docs/guides/depannage.md) | FAQ, messages d'erreur, solutions | p.169-181 |

---

## 📊 État du projet

| Composant | Statut | Dernière mise à jour |
|-----------|--------|---------------------|
| 📚 Documentation | 🟡 En cours (PHASE 1/2) | 2024-04 |
| 🐍 Scripts Python | 🟢 Fonctionnels (4/4) | 2024-04 |
| 🐳 Docker | 🟢 Ready | 2024-04 |
| 🤖 CI/CD | 🟡 GitHub Actions (Sphinx) | 2024-04 |

---

## 🗓️ Roadmap

- [ ] PHASE 2 : Génération auto des fichiers `.md` via IA (AccuEQ, Dirac, Multizone)
- [ ] Tests unitaires pour les scripts Python (`pytest`)
- [ ] Intégration Home Assistant complète (MQTT + REST)
- [ ] Traduction EN/FR de la documentation
---

## 🔧 Installation détaillée

### Prérequis système
| Composant | Version requise | Notes |
|-----------|----------------|-------|
| Windows 11 / Linux / macOS | - | PowerShell 7+ recommandé sur Windows |
| Python | ≥ 3.11 | [Télécharger](https://www.python.org/downloads/) |
| Git | ≥ 2.40 | [Installer](https://git-scm.com/downloads) |
| Docker (optionnel) | ≥ 24.0 | [Docker Desktop](https://www.docker.com/products/docker-desktop) |

### Installation pas-à-pas
```powershell
# 1. Cloner le dépôt
git clone https://github.com/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50.git
cd Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50

# 2. Créer et activer un environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r scripts/requirements.txt
pip install -r requirements-docs.txt

# 4. Configurer les paramètres du TX-RZ50
cp config/example.env config/.env
# Éditer config/.env avec l'adresse IP de ton TX-RZ50
```

### Vérification
```powershell
# Tester la connexion au TX-RZ50
python scripts/rs232_control.py --host 192.168.1.100 --command "PWR?QSTN"

# Vérifier la version du firmware
python scripts/firmware_checker.py --host 192.168.1.100
```

> ℹ️ **Note** : Assure-toi que le TX-RZ50 est sur le même réseau et que le contrôle réseau est activé dans `Setup → Hardware → Network`.

---

## 🐍 Scripts Python fonctionnels

| Script | Description | Commande d'exemple |
|--------|-------------|-------------------|
| `rs232_control.py` | Contrôle série RS-232 (allumage, source, volume, modes) | `python rs232_control.py --host 192.168.1.100 --volume 40` |
| `http_api_wrapper.py` | Wrapper API HTTP/Web Setup du TX-RZ50 | `python http_api_wrapper.py --host 192.168.1.100 --action get_status` |
| `log_parser.py` | Analyseur de logs série/HTTP, export CSV/JSON | `python log_parser.py --input rs232.log --output report.json` |
| `firmware_checker.py` | Vérification version firmware via réseau | `python firmware_checker.py --host 192.168.1.100 --verbose` |

### Architecture
```text
scripts/
├── rs232_control.py      # Gestion ISCP via pyserial
├── http_api_wrapper.py   # Requêtes HTTP vers /goform/formMainZone
├── log_parser.py         # Parsing logs + mapping codes erreur [p.9-10, p.171-181]
├── firmware_checker.py   # Vérif version via /Status/getStatus
├── requirements.txt      # Dépendances Python
└── README.md             # Documentation technique des scripts
```

### Exemple : Automatisation Home Assistant
```yaml
# config/home_assistant.yaml
rest_command:
  onkyo_power_on:
    url: "http://{{ states('input_text.onkyo_ip') }}/goform/formMainZone"
    method: "post"
    payload: "ctl00=PWON"
    headers:
      Authorization: "Basic {{ states('input_text.onkyo_auth') }}"
```

---

## 🐳 Déploiement Docker

### Structure
```text
docker/
├── Dockerfile           # Python 3.11-slim, non-root, HEALTHCHECK
├── docker-compose.yml   # Services: onkyo-control + onkyo-docs
└── .dockerignore        # Exclusions de build
```

### Lancer avec Docker Compose
```powershell
# Build et démarrage
docker-compose -f docker/docker-compose.yml up -d

# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f onkyo-control

# Arrêter
docker-compose -f docker/docker-compose.yml down
```

### Variables d'environnement
| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `TX_RZ50_IP` | `192.168.1.100` | Adresse IP du récepteur |
| `RS232_PORT` | `/dev/ttyUSB0` | Port série (Linux) ou `COM3` (Windows) |
| `LOG_LEVEL` | `INFO` | Niveau de logging (`DEBUG`, `INFO`, `WARNING`) |

---

## 📖 Documentation Sphinx

### Générer localement
```powershell
.\.venv\Scripts\Activate.ps1
cd docs && make html
Start-Process "_build/html/index.html"
```

### Structure
```text
docs/
├── source/
│   ├── installation.rst    # Branchement, sécurité
│   ├── configuration.rst   # AccuEQ, Dirac Live
│   ├── modes_ecoute.rst    # Dolby Atmos, DTS:X, THX
│   ├── depannage.rst       # FAQ, codes erreur
│   └── scripts_api.rst     # Docs auto-générées des scripts
├── conf.py                 # Configuration Sphinx
├── index.rst               # Page d'accueil
└── Makefile                # Commandes de build
```

### Extensions activées
- `sphinx.ext.autodoc` : Documentation auto depuis les docstrings
- `sphinx.ext.napoleon` : Support docstrings Google/NumPy
- `sphinx.ext.viewcode` : Liens vers le code source
- `myst_parser` : Support Markdown dans les `.rst`

---

## 🤝 Contribution

### Comment contribuer ?
1. Fork le dépôt
2. Crée une branche feature : `git checkout -b feat/ma-fonctionnalite`
3. Commit : `git commit -m 'feat: ajout de ma fonctionnalité'`
4. Push : `git push origin feat/ma-fonctionnalite`
5. Ouvre une Pull Request 🎉

### Guidelines
- ✅ Respecter PEP 8 pour Python
- ✅ Ajouter des tests pour les nouvelles fonctionnalités
- ✅ Mettre à jour la documentation si nécessaire
- ✅ Utiliser les templates d'issues (`.github/ISSUE_TEMPLATE/`)

### Templates disponibles
- 🐛 [Rapport de Bug](.github/ISSUE_TEMPLATE/bug_report.md)
- 📚 [Suggestion Documentation](.github/ISSUE_TEMPLATE/doc_suggestion.md)
- 🚀 [Demande de Fonctionnalité](.github/ISSUE_TEMPLATE/feature_request.md)

---

## ⚖️ Licence & Attribution

### Licence du projet
Ce projet est distribué sous licence **MIT**. Voir [LICENSE](LICENSE).

### Attribution
- **ONKYO TX-RZ50** : Produit et manuel © Onkyo Home Entertainment Corporation. Extraits inclus en fair use à des fins éducatives.
- **Dirac Live®** : Technologie © Dirac Research.
- **Dolby, DTS, THX** : Marques déposées de leurs propriétaires respectifs.

### Crédits
- Scripts Python inspirés des protocoles ISCP et Web Setup d'Onkyo
- Documentation structurée avec [Sphinx](https://www.sphinx-doc.org/)
- Templates GitHub basés sur [opensource.guide](https://opensource.guide/)

---

## 🙏 Remerciements

- 🎧 Aux passionnés d'audio qui partagent leurs connaissances
- 🔧 À la communauté open source pour `pyserial`, `requests`, etc.
- 📚 À Onkyo pour la qualité technique du TX-RZ50
- 💡 À toi, contributeur, pour faire vivre ce projet !

---

> 🌟 **Projet maintenu par** [@valorisa](https://github.com/valorisa)  
> 📬 **Contact** : Via les [GitHub Issues](https://github.com/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50/issues)  
> 🔄 **Dernière mise à jour** : 04 Avril 2026
