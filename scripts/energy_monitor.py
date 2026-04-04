#!/usr/bin/env python3
"""
Moniteur de consommation électrique pour ONKYO TX-RZ50.

Surveille l'état du récepteur et alerte si celui-ci reste allumé
sans activité pendant une période prolongée.

Dépendances:
    pip install requests

Usage:
    python energy_monitor.py --host 192.168.1.100 --max-idle 120
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, Timeout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Consommation typique du TX-RZ50 (watts)
POWER_CONSUMPTION = {
    "on": 380,
    "standby_network": 2.0,
    "standby": 0.1,
}


class EnergyMonitor:
    """Surveille la consommation du TX-RZ50."""

    def __init__(
        self,
        host: str,
        max_idle_minutes: int = 120,
        username: str = "admin",
        password: str = "admin",
        log_file: Path | None = None,
    ):
        self.base_url = f"http://{host}"
        self.auth = HTTPBasicAuth(username, password)
        self.max_idle = timedelta(minutes=max_idle_minutes)
        self.log_file = log_file
        self.last_active = datetime.now()
        self.last_power_state = None
        self.total_kwh = 0.0

    def _get_status(self) -> dict | None:
        """Récupère l'état du récepteur."""
        try:
            r = requests.get(
                f"{self.base_url}/Status/getStatus",
                auth=self.auth,
                timeout=5,
            )
            r.raise_for_status()
            return r.json()
        except Timeout:
            logger.warning("Timeout lors de la récupération du statut")
            return None
        except RequestException as e:
            logger.error("Erreur réseau: %s", e)
            return None

    def _log_consumption(self, power: str, watts: float):
        """Log la consommation dans un fichier."""
        if not self.log_file:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "power": power,
            "watts": watts,
            "total_kwh": round(self.total_kwh, 4),
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _check_idle_timeout(self, power: str):
        """Vérifie si le récepteur est inactif trop longtemps."""
        if power == "on":
            if self.last_power_state != "on":
                self.last_active = datetime.now()
            return

        idle_time = datetime.now() - self.last_active
        if idle_time > self.max_idle and self.last_power_state == "on":
            logger.warning(
                "⚠️ TX-RZ50 inactif depuis %s (max: %s)",
                idle_time,
                self.max_idle,
            )
            logger.warning(
                "💡 Considérez l'extinction automatique ou le Network Standby"
            )

    def poll(self) -> dict:
        """Interroge l'état et calcule la consommation."""
        status = self._get_status()
        if status is None:
            return {"error": "unreachable"}

        power = status.get("power", "unknown")
        watts = POWER_CONSUMPTION.get(power, 0)

        # Estimation kWh (sur intervalle de polling)
        hours = 1.0 / 3600  # 1 seconde en heures
        self.total_kwh += (watts * hours) / 1000

        self._log_consumption(power, watts)
        self._check_idle_timeout(power)

        self.last_power_state = power

        return {
            "power": power,
            "watts": watts,
            "total_kwh": round(self.total_kwh, 4),
            "timestamp": datetime.now().isoformat(),
        }

    def run(self, interval: int = 60):
        """Boucle principale de monitoring."""
        logger.info(
            "Démarrage du monitoring (intervalle: %ss, max idle: %s min)",
            interval,
            self.max_idle.total_seconds() / 60,
        )

        try:
            while True:
                result = self.poll()
                if "error" not in result:
                    logger.info(
                        "État: %s | %.1f W | Total: %.4f kWh",
                        result["power"],
                        result["watts"],
                        result["total_kwh"],
                    )
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Monitoring arrêté.")


def main():
    parser = argparse.ArgumentParser(
        description="Moniteur de consommation ONKYO TX-RZ50"
    )
    parser.add_argument("--host", required=True, help="IP du TX-RZ50")
    parser.add_argument("--user", default="admin", help="Identifiant Web Setup")
    parser.add_argument(
        "--pass", dest="password", default="admin", help="Mot de passe Web Setup"
    )
    parser.add_argument(
        "--max-idle",
        type=int,
        default=120,
        help="Minutes max d'inactivité avant alerte (défaut: 120)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Intervalle de polling en secondes (défaut: 60)",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Fichier de log JSON pour la consommation",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode debug")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    log_path = Path(args.log_file) if args.log_file else None

    monitor = EnergyMonitor(
        host=args.host,
        max_idle_minutes=args.max_idle,
        username=args.user,
        password=args.password,
        log_file=log_path,
    )
    monitor.run(interval=args.interval)


if __name__ == "__main__":
    main()
