#!/usr/bin/env python3
"""
Vérificateur de version du micrologiciel pour le ONKYO TX-RZ50.

Ce script interroge l'interface Web Setup du récepteur pour récupérer la version
actuelle du firmware, la compare avec une version de référence (locale ou distante),
et génère une notification claire en cas de mise à jour disponible.

Il s'appuie sur la documentation officielle [p.8-10, p.156] concernant les
procédures de mise à jour et la vérification de version via le menu Setup
("7. Miscellaneous" -> "Firmware Update" -> "Version").

Exemples d'utilisation :
    python firmware_checker.py --host 192.168.1.100
    python firmware_checker.py --host 192.168.1.100 --latest-url https://example.com/tx-rz50-latest.json
    python firmware_checker.py --host 192.168.1.100 --output firmware_status.json --verbose

Attributes:
    DEFAULT_VERSION_FILE (Path): Chemin par défaut pour stocker la version locale.
    VERSION_PATTERN (re): Regex pour extraire les numéros de version (ex: 1.0.0).

Todo:
    * Ajouter le support du parsing HTML de la page DeviceInformation si le JSON n'est pas dispo
    * Intégrer un webhook Discord/Slack pour les alertes automatiques
    * Supporter le téléchargement direct du fichier .zip via l'API
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from requests.auth import HTTPBasicAuth
from packaging.version import Version, InvalidVersion

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / 'firmware_checker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_VERSION_FILE = Path(__file__).parent / "current_fw_version.json"
VERSION_PATTERN = re.compile(r"(\d+\.\d+\.\d+)")


class FirmwareChecker:
    """
    Vérificateur et comparateur de micrologiciel TX-RZ50.
    
    Cette classe gère la récupération de la version actuelle via l'API Web,
    le stockage local, la comparaison sémantique et la génération de rapports.
    
    Attributes:
        host (str): Adresse IP du TX-RZ50.
        auth (HTTPBasicAuth): Identifiants d'accès Web Setup [p.157].
        session (requests.Session): Session HTTP réutilisable.
        
    Raises:
        ValueError: Si l'hôte est invalide.
        ConnectionError: En cas d'échec de connexion au récepteur.
        
    Example:
        >>> checker = FirmwareChecker("192.168.1.100")
        >>> status = checker.check_update()
        >>> print(status["message"])
    """
    
    def __init__(self, host: str, username: str = "admin", password: str = "admin"):
        """
        Initialise le vérificateur de firmware.
        
        Args:
            host: Adresse IP ou hostname du TX-RZ50.
            username: Identifiant Web Setup (défaut: admin).
            password: Mot de passe Web Setup (défaut: admin).
        """
        if not host or "://" in host:
            raise ValueError("L'hôte doit être fourni sans schéma (ex: 192.168.1.100)")
            
        self.base_url = f"http://{host}"
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        logger.info(f"FirmwareChecker initialisé pour {self.base_url}")

    def _fetch_page(self, endpoint: str) -> Optional[str]:
        """Récupère le contenu brut d'une page Web Setup."""
        try:
            url = f"{self.base_url}{endpoint}"
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.error(f"Échec de récupération {endpoint}: {e}")
            return None

    def get_current_version(self) -> Optional[str]:
        """
        Extrait la version actuelle du firmware depuis le récepteur.
        
        Returns:
            str: Numéro de version (ex: "1.1.0") ou None si indisponible.
            
        Note:
            L'API Web Setup d'Onkyo n'est pas officiellement documentée.
            Cette méthode tente de parser la réponse JSON de /Status/getStatus
            ou fallback sur le parsing HTML de /DeviceInformation [p.157].
        """
        # Tentative via endpoint JSON (souvent présent sur les modèles récents)
        try:
            data = self._fetch_json("/Status/getStatus")
            if data and "firmware" in data:
                ver_match = VERSION_PATTERN.search(str(data["firmware"]))
                if ver_match:
                    return ver_match.group(1)
        except Exception:
            logger.debug("Parsing JSON échoué, tentative fallback HTML...")

        # Fallback parsing HTML (structure courante Onkyo)
        html = self._fetch_page("/DeviceInformation")
        if html:
            ver_match = VERSION_PATTERN.search(html)
            if ver_match:
                return ver_match.group(1)
                
        logger.warning("Impossible d'extraire la version actuelle. Vérifiez la connexion réseau.")
        return None

    def _fetch_json(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Helper pour parser une réponse JSON."""
        text = self._fetch_page(endpoint)
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return None
        return None

    def get_latest_reference(self, source_url: Optional[str] = None) -> Optional[str]:
        """
        Récupère la version de référence la plus récente.
        
        Args:
            source_url: URL vers un fichier JSON contenant {"latest_version": "x.y.z"}.
                       Si None, lit DEFAULT_VERSION_FILE.
                       
        Returns:
            str: Version de référence ou None.
        """
        if source_url:
            try:
                resp = requests.get(source_url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                ver_match = VERSION_PATTERN.search(str(data.get("latest_version", "")))
                if ver_match:
                    return ver_match.group(1)
            except Exception as e:
                logger.error(f"Échec récupération URL distante: {e}")
        elif DEFAULT_VERSION_FILE.exists():
            try:
                data = json.loads(DEFAULT_VERSION_FILE.read_text(encoding="utf-8"))
                return data.get("latest_version")
            except Exception as e:
                logger.error(f"Échec lecture fichier local: {e}")
        return None

    def check_update(self, latest_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Compare la version actuelle avec la version de référence.
        
        Args:
            latest_url: URL optionnelle vers le fichier de référence.
            
        Returns:
            Dict[str, Any]: Rapport structuré {current, latest, update_available, message, timestamp}
        """
        current = self.get_current_version()
        if not current:
            return {"current": None, "latest": None, "update_available": False, "message": "❌ Impossible de lire la version actuelle.", "timestamp": datetime.now().isoformat()}

        latest = self.get_latest_reference(latest_url) or current
        
        try:
            is_update = Version(latest) > Version(current)
            msg = f"✅ Firmware à jour ({current})." if not is_update else f"🔔 Mise à jour disponible : {current} -> {latest} [p.8-10]"
        except InvalidVersion:
            is_update = False
            msg = f"⚠️ Versions non comparables (actuelle: {current}, référence: {latest})."

        result = {
            "current": current,
            "latest": latest,
            "update_available": is_update,
            "message": msg,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Résultat vérification: {result['message']}")
        return result

    def save_version(self, version: str) -> None:
        """Enregistre la version de référence localement pour usage futur."""
        DEFAULT_VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_VERSION_FILE.write_text(
            json.dumps({"latest_version": version, "updated_at": datetime.now().isoformat()}, indent=2),
            encoding="utf-8"
        )
        logger.info(f"Version {version} enregistrée dans {DEFAULT_VERSION_FILE}")


def main():
    """Point d'entrée CLI du vérificateur de firmware."""
    parser = argparse.ArgumentParser(
        description="Vérificateur de firmware ONKYO TX-RZ50 [p.8-10, p.156]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s --host 192.168.1.100
  %(prog)s --host 192.168.1.100 --latest-url https://raw.githubusercontent.com/valorisa/tx-rz50-firmware/main/latest.json
  %(prog)s --host 192.168.1.100 --output report.json --set-latest 1.1.0
        """
    )
    parser.add_argument("--host", required=True, help="Adresse IP du TX-RZ50")
    parser.add_argument("--user", default="admin", help="Identifiant Web Setup")
    parser.add_argument("--pass", dest="password", default="admin", help="Mot de passe Web Setup")
    parser.add_argument("--latest-url", default=None, help="URL vers un JSON contenant la dernière version")
    parser.add_argument("--output", "-o", default=None, help="Fichier de sortie JSON")
    parser.add_argument("--set-latest", default=None, help="Force et enregistre manuellement la version de référence")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    try:
        checker = FirmwareChecker(args.host, args.user, args.password)
        
        if args.set_latest:
            checker.save_version(args.set_latest)
            print(f"💾 Version de référence définie sur : {args.set_latest}")
            return

        result = checker.check_update(args.latest_url)
        print(result["message"])
        
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"📄 Rapport sauvegardé : {args.output}")
            
    except (ValueError, ConnectionError) as e:
        logger.error(f"Erreur d'exécution: {e}")
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
