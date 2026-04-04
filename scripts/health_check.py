#!/usr/bin/env python3
"""
Script de vérification de santé pour le conteneur Docker ONKYO TX-RZ50.

Ce script vérifie que l'environnement est correctement configuré et que
les dépendances sont disponibles. Il est utilisé par le HEALTHCHECK du Dockerfile.

Usage:
    python health_check.py
"""

import sys
from pathlib import Path


def check_dependencies():
    """Vérifie que les modules Python requis sont importables."""
    missing = []
    for mod in ["serial", "requests", "packaging"]:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print(f"FAIL: Modules manquants: {', '.join(missing)}")
        return False
    return True


def check_scripts():
    """Vérifie que les scripts principaux sont présents."""
    scripts_dir = Path(__file__).parent
    required = [
        "rs232_control.py",
        "http_api_wrapper.py",
        "log_parser.py",
        "firmware_checker.py",
    ]
    missing = [s for s in required if not (scripts_dir / s).exists()]
    if missing:
        print(f"FAIL: Scripts manquants: {', '.join(missing)}")
        return False
    return True


def check_directories():
    """Vérifie que les répertoires de travail existent."""
    base = Path(__file__).parent.parent
    for d in ["config", "logs"]:
        p = base / d
        if not p.exists():
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError:
                print(f"FAIL: Impossible de créer {p}")
                return False
    return True


def main():
    checks = [check_dependencies(), check_scripts(), check_directories()]
    if all(checks):
        print("OK: Tous les contrôles sont passés.")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
