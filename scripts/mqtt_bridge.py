#!/usr/bin/env python3
"""
Pont MQTT pour ONKYO TX-RZ50 - Intégration Home Assistant.

Ce script fait le lien entre les commandes MQTT reçues de Home Assistant
et l'API HTTP du TX-RZ50. Il publie également l'état actuel du récepteur.

Dépendances:
    pip install paho-mqtt requests

Usage:
    python mqtt_bridge.py --host 192.168.1.100 --mqtt-broker 192.168.1.50

Configuration Home Assistant (MQTT):
    mqtt:
      - media_player:
          name: "ONKYO TX-RZ50"
          command_topic: "onkyo/tx-rz50/power/set"
          state_topic: "onkyo/tx-rz50/power/state"
          source_command_topic: "onkyo/tx-rz50/source/set"
          source_state_topic: "onkyo/tx-rz50/source/state"
"""

import argparse
import logging
import sys
import time

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, RequestException, Timeout

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("Erreur: paho-mqtt n'est pas installé.")
    print("Installer avec: pip install paho-mqtt")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Mappage des sources ISCP -> noms lisibles
SOURCE_MAP = {
    "00": "BD/DVD",
    "01": "GAME",
    "02": "CBL/SAT",
    "03": "STRM BOX",
    "04": "PC",
    "05": "AUX",
    "06": "CD",
    "07": "TV",
    "08": "PHONO",
    "26": "TUNER",
    "27": "NET",
    "28": "USB",
    "29": "BLUETOOTH",
}

REVERSE_SOURCE_MAP = {v: k for k, v in SOURCE_MAP.items()}


class OnkyoMQTTBridge:
    """Pont entre MQTT et l'API HTTP du TX-RZ50."""

    def __init__(
        self,
        onkyo_host: str,
        mqtt_broker: str,
        mqtt_port: int = 1883,
        mqtt_user: str | None = None,
        mqtt_password: str | None = None,
        username: str = "admin",
        password: str = "admin",
        poll_interval: int = 30,
    ):
        self.onkyo_url = f"http://{onkyo_host}"
        self.auth = HTTPBasicAuth(username, password)
        self.poll_interval = poll_interval

        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.on_disconnect = self._on_disconnect

        if mqtt_user and mqtt_password:
            self.mqtt_client.username_pw_set(mqtt_user, mqtt_password)

        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.base_topic = "onkyo/tx-rz50"

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info("Connecté au broker MQTT")
            client.subscribe(f"{self.base_topic}/power/set")
            client.subscribe(f"{self.base_topic}/volume/set")
            client.subscribe(f"{self.base_topic}/source/set")
            client.subscribe(f"{self.base_topic}/listening_mode/set")
            client.subscribe(f"{self.base_topic}/mute/set")
            client.subscribe(f"{self.base_topic}/zone2/power/set")
            client.subscribe(f"{self.base_topic}/zone2/source/set")
            client.subscribe(f"{self.base_topic}/zone2/volume/set")
            client.publish(f"{self.base_topic}/availability", "online", retain=True)
            self._poll_status()
        else:
            logger.error(f"Échec connexion MQTT, code: {rc}")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        logger.warning(f"Déconnecté du broker MQTT, code: {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode().strip()
            logger.info(f"Message sur {msg.topic}: {payload}")

            if msg.topic.endswith("/power/set"):
                self._handle_power(payload)
            elif msg.topic.endswith("/volume/set"):
                self._handle_volume(payload)
            elif msg.topic.endswith("/source/set"):
                self._handle_source(payload)
            elif msg.topic.endswith("/listening_mode/set"):
                self._handle_listening_mode(payload)
            elif msg.topic.endswith("/mute/set"):
                self._handle_mute(payload)
            elif msg.topic.endswith("/zone2/power/set"):
                self._handle_zone2_power(payload)
            elif msg.topic.endswith("/zone2/source/set"):
                self._handle_zone2_source(payload)
            elif msg.topic.endswith("/zone2/volume/set"):
                self._handle_zone2_volume(payload)
        except Exception as e:
            logger.error(f"Erreur traitement message: {e}")

    def _http_post(self, endpoint: str, payload: dict) -> bool:
        """Envoie une requête POST à l'API HTTP du TX-RZ50."""
        url = f"{self.onkyo_url}{endpoint}"
        try:
            resp = requests.post(url, json=payload, auth=self.auth, timeout=5)
            resp.raise_for_status()
            return True
        except Timeout:
            logger.error(f"Timeout sur {url}")
            return False
        except HTTPError as e:
            logger.error(f"Erreur HTTP {e.response.status_code} sur {url}")
            return False
        except RequestException as e:
            logger.error(f"Erreur réseau sur {url}: {e}")
            return False

    def _handle_power(self, state: str):
        state_lower = state.lower()
        if state_lower in ("on", "true", "1"):
            success = self._http_post("/Power/setPower", {"power": "on"})
            if success:
                self.mqtt_client.publish(
                    f"{self.base_topic}/power/state", "ON", retain=True
                )
        elif state_lower in ("off", "standby", "false", "0"):
            success = self._http_post("/Power/setPower", {"power": "standby"})
            if success:
                self.mqtt_client.publish(
                    f"{self.base_topic}/power/state", "STANDBY", retain=True
                )

    def _handle_volume(self, payload: str):
        try:
            level = int(payload)
        except ValueError:
            logger.error(f"Volume invalide: {payload}")
            return

        level = max(0, min(80, level))
        success = self._http_post("/Volume/setVolume", {"volume": level})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/volume/state", level, retain=True
            )

    def _handle_source(self, source_name: str):
        code = REVERSE_SOURCE_MAP.get(source_name.upper())
        if not code:
            logger.warning(f"Source inconnue: {source_name}")
            return

        success = self._http_post("/Source/setSource", {"source": code})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/source/state", source_name, retain=True
            )

    def _handle_listening_mode(self, mode: str):
        mode_map = {
            "STEREO": "LMST",
            "DIRECT": "LMDIR",
            "PURE_AUDIO": "LMPDA",
            "DOLBY_ATMOS": "LMDA",
            "DTS_X": "LMDTS",
            "THX_CINEMA": "LMTHX",
            "THX_MUSIC": "LMTHXM",
            "THX_GAMES": "LMTHXG",
        }
        code = mode_map.get(mode.upper())
        if not code:
            logger.warning(f"Mode d'écoute inconnu: {mode}")
            return

        success = self._http_post("/ListeningMode/setListeningMode", {"mode": code})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/listening_mode/state", mode, retain=True
            )

    def _handle_mute(self, state: str):
        state_lower = state.lower()
        if state_lower in ("on", "true", "1"):
            success = self._http_post("/Volume/setMute", {"mute": True})
            if success:
                self.mqtt_client.publish(
                    f"{self.base_topic}/mute/state", "ON", retain=True
                )
        elif state_lower in ("off", "false", "0"):
            success = self._http_post("/Volume/setMute", {"mute": False})
            if success:
                self.mqtt_client.publish(
                    f"{self.base_topic}/mute/state", "OFF", retain=True
                )

    def _handle_zone2_power(self, state: str):
        state_lower = state.lower()
        power = "on" if state_lower in ("on", "true", "1") else "standby"
        success = self._http_post("/Zone2/setPower", {"power": power})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/zone2/power/state", power.upper(), retain=True
            )

    def _handle_zone2_source(self, source_name: str):
        code = REVERSE_SOURCE_MAP.get(source_name.upper())
        if not code:
            logger.warning(f"Source ZONE2 inconnue: {source_name}")
            return
        success = self._http_post("/Zone2/setSource", {"source": code})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/zone2/source/state", source_name, retain=True
            )

    def _handle_zone2_volume(self, payload: str):
        try:
            level = int(payload)
        except ValueError:
            logger.error(f"Volume ZONE2 invalide: {payload}")
            return
        level = max(0, min(80, level))
        success = self._http_post("/Zone2/setVolume", {"volume": level})
        if success:
            self.mqtt_client.publish(
                f"{self.base_topic}/zone2/volume/state", level, retain=True
            )

    def _poll_status(self):
        """Interroge l'état du récepteur et publie sur MQTT."""
        try:
            resp = requests.get(
                f"{self.onkyo_url}/Status/getStatus",
                auth=self.auth,
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()

            power = data.get("power", "unknown")
            self.mqtt_client.publish(
                f"{self.base_topic}/power/state", power.upper(), retain=True
            )

            volume = data.get("volume", 0)
            self.mqtt_client.publish(
                f"{self.base_topic}/volume/state", volume, retain=True
            )

            src_code = str(data.get("source", "00"))
            src_name = SOURCE_MAP.get(src_code, "Unknown")
            self.mqtt_client.publish(
                f"{self.base_topic}/source/state", src_name, retain=True
            )

            self.mqtt_client.publish(
                f"{self.base_topic}/availability", "online", retain=True
            )
        except RequestException as e:
            logger.error(f"Erreur polling status: {e}")
            self.mqtt_client.publish(
                f"{self.base_topic}/availability", "offline", retain=True
            )

    def start(self):
        """Démarre le pont MQTT et la boucle de polling."""
        logger.info(
            f"Démarrage du pont MQTT: {self.mqtt_broker}:{self.mqtt_port} -> {self.onkyo_url}"
        )
        try:
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
            self.mqtt_client.loop_start()

            while True:
                time.sleep(self.poll_interval)
                self._poll_status()
        except KeyboardInterrupt:
            logger.info("Arrêt du pont MQTT...")
            self.mqtt_client.publish(
                f"{self.base_topic}/availability", "offline", retain=True
            )
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            logger.info("Pont MQTT arrêté.")
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
            self.mqtt_client.loop_stop()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Pont MQTT pour ONKYO TX-RZ50 - Intégration Home Assistant"
    )
    parser.add_argument("--host", required=True, help="Adresse IP du TX-RZ50")
    parser.add_argument("--mqtt-broker", required=True, help="Adresse du broker MQTT")
    parser.add_argument(
        "--mqtt-port", type=int, default=1883, help="Port MQTT (défaut: 1883)"
    )
    parser.add_argument(
        "--mqtt-user", default=None, help="Identifiant MQTT (optionnel)"
    )
    parser.add_argument(
        "--mqtt-pass", default=None, help="Mot de passe MQTT (optionnel)"
    )
    parser.add_argument(
        "--user", default="admin", help="Identifiant Web Setup (défaut: admin)"
    )
    parser.add_argument(
        "--pass",
        dest="password",
        default="admin",
        help="Mot de passe Web Setup (défaut: admin)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=30,
        help="Intervalle de polling en secondes (défaut: 30)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Mode verbeux (debug)"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    bridge = OnkyoMQTTBridge(
        onkyo_host=args.host,
        mqtt_broker=args.mqtt_broker,
        mqtt_port=args.mqtt_port,
        mqtt_user=args.mqtt_user,
        mqtt_password=args.mqtt_pass,
        username=args.user,
        password=args.password,
        poll_interval=args.poll_interval,
    )
    bridge.start()


if __name__ == "__main__":
    main()
