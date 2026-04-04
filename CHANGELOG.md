# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `scripts/energy_monitor.py` - Script de monitoring de consommation électrique
- `custom_component/onkyo_tx_rz50/` - Custom Component Home Assistant natif
- `docs/guides/accueq_deep_dive.md` - Guide AccuEQ vs Dirac Live
- `docs/guides/security.md` - Guide de sécurité réseau
- `config/node_red_flows.json` - Flows Node-RED prêts à importer
- `CHANGELOG.md` - Journal des modifications
- `CONTRIBUTING.md` - Guide de contribution

## [1.1.0] - 2026-04-04

### Added
- `scripts/mqtt_bridge.py` - Pont MQTT autonome pour Home Assistant
- `scripts/web_dashboard.py` - Dashboard Web FastAPI pour contrôle du TX-RZ50
- `docs/guides/rew_dirac.md` - Guide REW + Dirac Live (calibration avancée)
- `docs/guides/multizone.md` - Guide Multizone ZONE 2 & ZONE 3
- `scripts/README.md` - Documentation technique des scripts
- `config/home_assistant.yaml` - Configuration Home Assistant (REST + MQTT)
- `scripts/health_check.py` - Script de santé pour Docker HEALTHCHECK
- `ruff.toml` - Configuration du linter Ruff
- `Makefile` - Commandes courantes (test, lint, docs, docker)
- `docs/Makefile` - Makefile Sphinx pour build local
- 91 tests unitaires pytest pour les scripts Python

### Changed
- CI/CD : pipeline complet lint → test → docs → deploy
- CI/CD : Node.js 24 forcé pour GitHub Actions
- Documentation Sphinx complète avec 6 guides
- README.md mis à jour avec l'état du projet

### Fixed
- `log_parser.py` : correction bug syntaxe for/elif (ligne 115)
- `http_api_wrapper.py` : correction variable response non liée (ligne 162)
- `rs232_control.py` : correction ValueError sur VOLUME SET et ZONE2 SOURCE
- `scripts/requirements.txt` : ajout des dépendances manquantes (packaging, pytest)

### Removed
- `docs/index.rst` : doublon inutilisé (remplacé par `docs/source/index.rst`)

## [1.0.0] - 2026-04-03

### Added
- Structure initiale du projet
- 4 scripts Python fonctionnels (rs232_control, http_api_wrapper, log_parser, firmware_checker)
- Documentation de base (installation, configuration, modes_ecoute, depannage)
- Configuration Docker (Dockerfile, docker-compose.yml)
- CI/CD GitHub Actions pour Sphinx docs
- Templates d'issues GitHub

[Unreleased]: https://github.com/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/valorisa/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50/releases/tag/v1.0.0
