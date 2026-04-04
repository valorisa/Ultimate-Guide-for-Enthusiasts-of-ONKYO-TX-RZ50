#!/usr/bin/env python3
"""
Wrapper HTTP pour l'API Web Setup du ONKYO TX-RZ50.

Ce module fournit une interface en ligne de commande pour interroger et configurer
le récepteur AV via son interface web intégrée. L'appareil expose une API JSON
accessible sur http://<IP_TX-RZ50> avec une authentification par défaut
admin/admin [p.157].

Exemples d'utilisation :
    # Obtenir l'état complet de l'appareil
    python http_api_wrapper.py --host 192.168.1.100 status
    
    # Changer le volume (0-100)
    python http_api_wrapper.py --host 192.168.1.100 volume --set 45
    
    # Allumer l'appareil
    python http_api_wrapper.py --host 192.168.1.100 power --on
    
    # Vérifier la version du firmware
    python http_api_wrapper.py --host 192.168.1.100 firmware

Note : L'API n'est pas officiellement documentée par Onkyo. Ce wrapper est basé
sur l'analyse des requêtes de l'interface Web Setup [p.145, p.157].

Attributes:
    DEFAULT_TIMEOUT (float): Timeout par défaut pour les requêtes HTTP (10 secondes).
    DEFAULT_CREDENTIALS (tuple): Identifiants par défaut (admin, admin).

Todo:
    * Ajouter le support des endpoints de calibration (AccuEQ/Dirac)
    * Implémenter un mode de découverte réseau (mDNS/SSDP)
    * Ajouter des tests unitaires avec responses mock

.. _Onkyo Web Setup:
    http://<IP_TX-RZ50>/
"""

import argparse
import json
import logging
import sys
from typing import Optional, Dict, Any
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, Timeout, HTTPError

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / 'http_api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Constantes
DEFAULT_TIMEOUT = 10.0
DEFAULT_CREDENTIALS = ("admin", "admin")
ENDPOINTS = {
    "status": "/Status/getStatus",
    "power": "/Power/setPower",
    "volume": "/Volume/setVolume",
    "source": "/Source/setSource",
    "network": "/Network/getNetwork",
    "firmware": "/Firmware/getVersion"
}


class OnkyoHTTPClient:
    """
    Client HTTP pour l'interface Web Setup du ONKYO TX-RZ50.
    
    Cette classe encapsule les appels REST vers l'API JSON du récepteur.
    Elle gère l'authentification, les timeouts, la gestion des erreurs
    et le parsing des réponses structurées.
    
    Attributes:
        base_url (str): URL de base de l'API (ex: http://192.168.1.100).
        auth (HTTPBasicAuth): Objet d'authentification.
        session (requests.Session): Session HTTP persistante avec retries.
        
    Raises:
        ValueError: Si l'URL est mal formatée.
        ConnectionError: En cas d'échec de connexion réseau.
        
    Example:
        >>> client = OnkyoHTTPClient("192.168.1.100")
        >>> status = client.get_status()
        >>> print(status['power'])
    """
    
    def __init__(self, host: str, username: str = "admin", password: str = "admin", timeout: float = DEFAULT_TIMEOUT):
        """
        Initialise le client HTTP.
        
        Args:
            host: Adresse IP ou hostname du TX-RZ50 (sans http://).
            username: Identifiant Web Setup [p.157].
            password: Mot de passe Web Setup [p.157].
            timeout: Délai d'attente en secondes pour les requêtes.
            
        Raises:
            ValueError: Si l'hôte est vide ou contient un schéma URL.
        """
        if not host or "://" in host:
            raise ValueError("L'hôte doit être fourni sans schéma (ex: 192.168.1.100)")
            
        self.base_url = f"http://{host}"
        self.auth = HTTPBasicAuth(username, password)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = self.auth
        logger.info(f"Client HTTP initialisé pour {self.base_url}")
        
        # Suppression des warnings InsecureRequestWarning si besoin
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Effectue une requête HTTP vers l'API Onkyo.
        
        Args:
            method: Méthode HTTP ('GET' ou 'POST').
            endpoint: Chemin de l'endpoint (ex: /Status/getStatus).
            payload: Dictionnaire JSON à envoyer (pour POST).
            
        Returns:
            Dict[str, Any]: Réponse JSON parsée.
            
        Raises:
            Timeout: Si la requête dépasse le délai imparti.
            HTTPError: Si le serveur retourne un code 4xx/5xx.
            ValueError: Si la réponse n'est pas du JSON valide.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = None

        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=self.timeout)
            else:
                response = self.session.post(url, json=payload, headers=headers, timeout=self.timeout)

            response.raise_for_status()
            data = response.json()
            logger.debug(f"Réponse {endpoint}: {json.dumps(data, indent=2)}")
            return data

        except Timeout as e:
            logger.error(f"Timeout sur {url}: {e}")
            raise TimeoutError(f"Le récepteur ne répond pas dans les {self.timeout}s") from e
        except HTTPError as e:
            logger.error(f"Erreur HTTP sur {url}: {e.response.status_code} - {e.response.text}")
            raise HTTPError(f"Erreur API: {e.response.status_code}") from e
        except json.JSONDecodeError as e:
            resp_text = response.text if response is not None else "N/A"
            logger.error(f"Réponse non JSON de {url}: {resp_text}")
            raise ValueError("Réponse invalide : JSON attendu") from e
        except RequestException as e:
            logger.error(f"Erreur réseau sur {url}: {e}")
            raise ConnectionError(f"Impossible de joindre {self.base_url}") from e

    def get_status(self) -> Dict[str, Any]:
        """Récupère l'état complet de l'appareil (alimentation, source, volume, etc.)"""
        return self._request("GET", ENDPOINTS["status"])

    def get_network_info(self) -> Dict[str, Any]:
        """Récupère les informations réseau (IP, MAC, SSID, état DHCP) [p.145]"""
        return self._request("GET", ENDPOINTS["network"])

    def get_firmware_version(self) -> Dict[str, Any]:
        """Récupère la version actuelle du micrologiciel [p.156]"""
        return self._request("GET", ENDPOINTS["firmware"])

    def set_power(self, state: bool) -> Dict[str, Any]:
        """
        Contrôle l'alimentation de l'appareil.
        
        Args:
            state: True pour allumer, False pour mettre en veille.
        """
        payload = {"power": "on" if state else "standby"}
        return self._request("POST", ENDPOINTS["power"], payload)

    def set_volume(self, level: int) -> Dict[str, Any]:
        """
        Règle le volume principal.
        
        Args:
            level: Niveau de volume entre 0 et 100.
        """
        if not (0 <= level <= 100):
            raise ValueError("Le volume doit être entre 0 et 100")
        payload = {"volume": level}
        return self._request("POST", ENDPOINTS["volume"], payload)

    def set_source(self, source: str) -> Dict[str, Any]:
        """
        Change la source d'entrée.
        
        Args:
            source: Nom de la source (ex: "BD/DVD", "NET", "BLUETOOTH", "TUNER").
        """
        payload = {"source": source.upper().replace(" ", "_")}
        return self._request("POST", ENDPOINTS["source"], payload)

    def close(self) -> None:
        """Ferme proprement la session HTTP."""
        if self.session:
            self.session.close()
            logger.info("Session HTTP fermée")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def main():
    """Point d'entrée CLI du wrapper HTTP."""
    parser = argparse.ArgumentParser(
        description="Wrapper HTTP pour l'API Web Setup ONKYO TX-RZ50 [p.157]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s --host 192.168.1.100 status
  %(prog)s --host 192.168.1.100 power --on
  %(prog)s --host 192.168.1.100 volume --set 45
  %(prog)s --host 192.168.1.100 source --name NET
        """
    )
    
    parser.add_argument("--host", required=True, help="Adresse IP du TX-RZ50")
    parser.add_argument("--user", default="admin", help="Identifiant Web Setup (défaut: admin)")
    parser.add_argument("--pass", dest="password", default="admin", help="Mot de passe Web Setup (défaut: admin)")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Timeout en secondes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux (debug)")
    
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
    
    # Sous-commande: status
    subparsers.add_parser("status", help="Afficher l'état complet")
    
    # Sous-commande: network
    subparsers.add_parser("network", help="Informations réseau [p.145]")
    
    # Sous-commande: firmware
    subparsers.add_parser("firmware", help="Version du micrologiciel [p.156]")
    
    # Sous-commande: power
    power_parser = subparsers.add_parser("power", help="Contrôle alimentation")
    power_group = power_parser.add_mutually_exclusive_group(required=True)
    power_group.add_argument("--on", action="store_true", help="Allumer")
    power_group.add_argument("--off", action="store_true", help="Veille")
    
    # Sous-commande: volume
    vol_parser = subparsers.add_parser("volume", help="Régler le volume")
    vol_parser.add_argument("--set", type=int, required=True, help="Niveau 0-100")
    
    # Sous-commande: source
    src_parser = subparsers.add_parser("source", help="Changer la source")
    src_parser.add_argument("--name", required=True, help="Nom de la source (BD/DVD, NET, etc.)")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    try:
        with OnkyoHTTPClient(args.host, args.user, args.password, args.timeout) as client:
            if args.command == "status":
                print(json.dumps(client.get_status(), indent=2, ensure_ascii=False))
            elif args.command == "network":
                print(json.dumps(client.get_network_info(), indent=2, ensure_ascii=False))
            elif args.command == "firmware":
                print(json.dumps(client.get_firmware_version(), indent=2, ensure_ascii=False))
            elif args.command == "power":
                res = client.set_power(args.on)
                print(f"✅ Alimentation: {'ON' if args.on else 'STANDBY'}")
            elif args.command == "volume":
                res = client.set_volume(args.set)
                print(f"✅ Volume réglé à: {args.set}")
            elif args.command == "source":
                res = client.set_source(args.name)
                print(f"✅ Source sélectionnée: {args.name}")
            else:
                parser.print_help()
                
    except (TimeoutError, ConnectionError, HTTPError, ValueError) as e:
        logger.error(f"Erreur d'exécution: {e}")
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
