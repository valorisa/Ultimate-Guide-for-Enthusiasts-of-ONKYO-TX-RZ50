# 🐍 Scripts Python - Documentation technique

> 📋 Guide d'utilisation des 6 scripts de contrôle du ONKYO TX-RZ50

## 📋 Vue d'ensemble

| Script | Protocole | Usage principal | Fichier |
|--------|-----------|----------------|---------|
| RS-232 Controller | Série (ISCP) | Contrôle filaire complet | `rs232_control.py` |
| HTTP API Wrapper | HTTP/REST | Contrôle réseau sans fil | `http_api_wrapper.py` |
| MQTT Bridge | MQTT + HTTP | Intégration Home Assistant temps réel | `mqtt_bridge.py` |
| Web Dashboard | FastAPI + HTTP | Interface Web de contrôle | `web_dashboard.py` |
| Log Parser | Analyse de fichiers | Diagnostic et audit | `log_parser.py` |
| Firmware Checker | HTTP/REST | Vérification mises à jour | `firmware_checker.py` |

---

## 🔧 Installation des dépendances

```bash
# Environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows

# Installation
pip install -r scripts/requirements.txt
```

### Dépendances par script

| Script | Dépendances |
|--------|-------------|
| `rs232_control.py` | `pyserial` |
| `http_api_wrapper.py` | `requests`, `urllib3` |
| `log_parser.py` | Aucune (stdlib uniquement) |
| `firmware_checker.py` | `requests`, `packaging` |

---

## 1️⃣ RS-232 Controller (`rs232_control.py`)

### Principe

Communique avec le TX-RZ50 via un câble USB-RS232 en utilisant le protocole ISCP (Integra Serial Control Protocol). Idéal pour les installations fixes où le réseau n'est pas fiable.

### Prérequis matériels

- Adaptateur USB-RS232 (FTDI FT232 recommandé)
- Câble RS-232 DB9 (croisé si nécessaire)
- Port RS-232 du TX-RZ50 (panneau arrière)

### Commandes supportées

#### Alimentation

```bash
# Allumer
python rs232_control.py --port COM3 --command "POWER ON"

# Mettre en veille
python rs232_control.py --port COM3 --command "POWER STANDBY"

# Vérifier l'état
python rs232_control.py --port COM3 --command "POWER QUERY"
```

#### Volume

```bash
# Monter le volume
python rs232_control.py --port COM3 --command "VOLUME UP"

# Descendre le volume
python rs232_control.py --port COM3 --command "VOLUME DOWN"

# Régler à un niveau précis (0-80)
python rs232_control.py --port COM3 --command "VOLUME SET 50"
```

#### Sources

```bash
# Sources courantes
python rs232_control.py --port COM3 --command "SOURCE NET"
python rs232_control.py --port COM3 --command "SOURCE BLUETOOTH"
python rs232_control.py --port COM3 --command "SOURCE TV"
python rs232_control.py --port COM3 --command "SOURCE BD/DVD"
python rs232_control.py --port COM3 --command "SOURCE PHONO"
python rs232_control.py --port COM3 --command "SOURCE TUNER"
```

#### Modes d'écoute

```bash
python rs232_control.py --port COM3 --command "LISTENING_MODE STEREO"
python rs232_control.py --port COM3 --command "LISTENING_MODE DIRECT"
python rs232_control.py --port COM3 --command "LISTENING_MODE PURE_AUDIO"
python rs232_control.py --port COM3 --command "LISTENING_MODE DOLBY_ATMOS"
python rs232_control.py --port COM3 --command "LISTENING_MODE DTS_X"
python rs232_control.py --port COM3 --command "LISTENING_MODE THX_CINEMA"
```

#### ZONE 2

```bash
# Allumer ZONE 2
python rs232_control.py --port COM3 --command "ZONE2 POWER_ON"

# Éteindre ZONE 2
python rs232_control.py --port COM3 --command "ZONE2 POWER_OFF"

# Changer la source de ZONE 2
python rs232_control.py --port COM3 --command "ZONE2 SOURCE BLUETOOTH"

# Régler le volume de ZONE 2
python rs232_control.py --port COM3 --command "ZONE2 VOLUME 30"
```

### Options de ligne de commande

| Option | Description | Défaut |
|--------|-------------|--------|
| `--port`, `-p` | Port série (COM3, /dev/ttyUSB0) | **Requis** |
| `--command`, `-c` | Commande à envoyer | **Requis** |
| `--baudrate`, `-b` | Vitesse (9600, 19200, 38400, 57600, 115200) | 9600 |
| `--timeout`, `-t` | Timeout en secondes | 5.0 |
| `--verbose`, `-v` | Mode debug | Off |

### Codes sources ISCP complets

| Code | Source | Code | Source |
|------|--------|------|--------|
| `00` | BD/DVD | `26` | TUNER |
| `01` | GAME | `27` | NET |
| `02` | CBL/SAT | `28` | USB |
| `03` | STRM BOX | `29` | BLUETOOTH |
| `04` | PC | | |
| `05` | AUX | | |
| `06` | CD | | |
| `07` | TV | | |
| `08` | PHONO | | |

---

## 2️⃣ HTTP API Wrapper (`http_api_wrapper.py`)

### Principe

Interroge et contrôle le TX-RZ50 via son interface web intégrée (Web Setup). Nécessite que le TX-RZ50 soit connecté au réseau local (Wi-Fi ou Ethernet).

### Prérequis

- TX-RZ50 sur le même réseau que la machine exécutant le script
- Contrôle réseau activé : `Setup → Hardware → Network → Network Control = On`
- Identifiants Web Setup (par défaut : `admin`/`admin`)

### Commandes

```bash
# État complet
python http_api_wrapper.py --host 192.168.1.100 status

# Informations réseau
python http_api_wrapper.py --host 192.168.1.100 network

# Version du firmware
python http_api_wrapper.py --host 192.168.1.100 firmware

# Alimentation
python http_api_wrapper.py --host 192.168.1.100 power --on
python http_api_wrapper.py --host 192.168.1.100 power --off

# Volume (0-100)
python http_api_wrapper.py --host 192.168.1.100 volume --set 45

# Source
python http_api_wrapper.py --host 192.168.1.100 source --name NET
```

### Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--host` | Adresse IP du TX-RZ50 | **Requis** |
| `--user` | Identifiant Web Setup | admin |
| `--pass` | Mot de passe Web Setup | admin |
| `--timeout` | Timeout en secondes | 10.0 |
| `--verbose`, `-v` | Mode debug | Off |

### Utilisation en tant que module Python

```python
from http_api_wrapper import OnkyoHTTPClient

with OnkyoHTTPClient("192.168.1.100") as client:
    # État complet
    status = client.get_status()
    print(status)

    # Allumer et régler le volume
    client.set_power(True)
    client.set_volume(40)
    client.set_source("NET")
```

---

## 3️⃣ Log Parser (`log_parser.py`)

### Principe

Analyse les fichiers de logs générés par les scripts `rs232_control.py` et `http_api_wrapper.py`. Identifie les événements, traduit les codes d'erreur et exporte en CSV/JSON.

### Formats supportés

- **serial_iscp** : Logs du contrôleur RS-232 (commandes ISCP)
- **http_request** : Logs du wrapper HTTP (requêtes REST)
- **error** : Codes d'erreur détectés automatiquement
- **status** : Événements de statut (succès, complétion)

### Commandes

```bash
# Analyse complète avec export JSON
python log_parser.py --input rs232_control.log --format serial --output report.json

# Filtrer uniquement les erreurs
python log_parser.py --input http_api.log --format http --filter Error --output errors.csv

# Analyse automatique avec double export
python log_parser.py --input mixed.log --format auto --export both --output rapport
```

### Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--input`, `-i` | Chemin du fichier de log | **Requis** |
| `--format`, `-f` | Format attendu (serial, http, auto) | auto |
| `--filter` | Filtrer par type (Error, Warning, Info, Command) | Aucun |
| `--output`, `-o` | Fichier de sortie | Console |
| `--export` | Format d'export (csv, json, both) | csv |

### Codes d'erreur détectés

| Code | Signification | Sévérité |
|------|--------------|----------|
| `**-01` | Câble Ethernet déconnecté | Warning |
| `**-05` | Fichier firmware manquant | Warning |
| `**-10` | Périphérique USB non reconnu | Warning |
| `**-13` | Fichier firmware incompatible | Warning |
| `CH SP WIRE` | Court-circuit bornes enceintes | Critical |
| `AMP Diag Mode` | Mode diagnostic amplificateur | Critical |
| `NG:` | Défaillance matérielle | Critical |
| `Resolution Error` | Résolution vidéo non supportée | Warning |
| `Noise Error` | Bruit pendant calibrage AccuEQ | Warning |

---

## 4️⃣ Firmware Checker (`firmware_checker.py`)

### Principe

Vérifie la version du firmware actuel du TX-RZ50 et la compare avec une version de référence pour détecter les mises à jour disponibles.

### Commandes

```bash
# Vérification simple
python firmware_checker.py --host 192.168.1.100

# Avec URL de référence distante
python firmware_checker.py --host 192.168.1.100 \
    --latest-url https://example.com/tx-rz50-latest.json

# Export du rapport en JSON
python firmware_checker.py --host 192.168.1.100 --output report.json

# Définir manuellement la version de référence
python firmware_checker.py --host 192.168.1.100 --set-latest 1.1.0

# Mode verbeux
python firmware_checker.py --host 192.168.1.100 --verbose
```

### Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--host` | Adresse IP du TX-RZ50 | **Requis** |
| `--user` | Identifiant Web Setup | admin |
| `--pass` | Mot de passe Web Setup | admin |
| `--latest-url` | URL vers JSON de référence | Local |
| `--output`, `-o` | Fichier de sortie JSON | Console |
| `--set-latest` | Version de référence manuelle | - |
| `--verbose`, `-v` | Mode debug | Off |

### Format du fichier de référence local

```json
{
  "latest_version": "1.1.0",
  "updated_at": "2024-04-01T12:00:00"
}
```

### Format du fichier de référence distant (URL)

Le fichier JSON distant doit avoir la même structure :

```json
{
  "latest_version": "1.1.0"
}
```

---

## 🔗 Combinaison de scripts : Exemple d'automatisation

```bash
#!/bin/bash
# Script de maintenance quotidienne pour le TX-RZ50

ONKYO_IP="192.168.1.100"
SERIAL_PORT="COM3"
LOG_DIR="./logs"
DATE=$(date +%Y%m%d)

# 1. Vérifier le firmware
python firmware_checker.py --host $ONKYO_IP --output "$LOG_DIR/fw_$DATE.json"

# 2. Allumer et tester la connexion
python http_api_wrapper.py --host $ONKYO_IP status > "$LOG_DIR/status_$DATE.json"

# 3. Parser les logs de la veille
python log_parser.py --input rs232_control.log --format auto \
    --filter Error --output "$LOG_DIR/errors_$DATE.csv"

# 4. Éteindre
python http_api_wrapper.py --host $ONKYO_IP power --off
```

---

## 5️⃣ MQTT Bridge (`mqtt_bridge.py`)

### Principe

Fait le lien entre un broker MQTT (ex: Mosquitto) et l'API HTTP du TX-RZ50. Permet une intégration temps réel avec Home Assistant sans polling REST.

### Commandes

```bash
# Démarrage basique
python mqtt_bridge.py --host 192.168.1.100 --mqtt-broker 192.168.1.50

# Avec authentification MQTT
python mqtt_bridge.py --host 192.168.1.100 --mqtt-broker 192.168.1.50 \
    --mqtt-user mqtt_user --mqtt-pass mqtt_pass

# Polling toutes les 10 secondes
python mqtt_bridge.py --host 192.168.1.100 --mqtt-broker 192.168.1.50 \
    --poll-interval 10
```

### Topics MQTT publiés/consommés

| Topic | Direction | Description |
|-------|-----------|-------------|
| `onkyo/tx-rz50/power/set` | Consommé | Allumer/éteindre |
| `onkyo/tx-rz50/power/state` | Publié | État actuel |
| `onkyo/tx-rz50/volume/set` | Consommé | Régler volume (0-80) |
| `onkyo/tx-rz50/volume/state` | Publié | Volume actuel |
| `onkyo/tx-rz50/source/set` | Consommé | Changer source |
| `onkyo/tx-rz50/source/state` | Publié | Source actuelle |
| `onkyo/tx-rz50/listening_mode/set` | Consommé | Mode d'écoute |
| `onkyo/tx-rz50/mute/set` | Consommé | Mute on/off |
| `onkyo/tx-rz50/zone2/power/set` | Consommé | ZONE 2 on/off |
| `onkyo/tx-rz50/availability` | Publié | online/offline |

---

## 6️⃣ Web Dashboard (`web_dashboard.py`)

### Principe

Serveur Web léger (FastAPI) offrant une interface de contrôle du TX-RZ50 accessible depuis un navigateur. Dashboard responsive avec contrôle du volume, des sources, des modes d'écoute et de ZONE 2.

### Commandes

```bash
# Démarrer sur le port par défaut (8080)
python web_dashboard.py --host 192.168.1.100

# Port personnalisé
python web_dashboard.py --host 192.168.1.100 --port 9090

# Avec authentification
python web_dashboard.py --host 192.168.1.100 --user admin --pass mon_mot_de_passe
```

### API REST du dashboard

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface Web |
| `/status` | GET | État actuel du récepteur |
| `/power` | POST | `{"on": true/false}` |
| `/volume` | POST | `{"level": 0-80}` |
| `/source` | POST | `{"code": "27"}` |
| `/mode` | POST | `{"code": "LMDA"}` |
| `/zone2/power` | POST | `{"on": true/false}` |
| `/zone2/source` | POST | `{"code": "27"}` |

---

## ⚠️ Notes importantes

- **RS-232 vs HTTP** : Les deux protocoles ne doivent pas être utilisés simultanément. Privilégier HTTP pour le contrôle réseau et RS-232 pour les installations fixes.
- **Network Standby** : Pour que le TX-RZ50 reste joignable via HTTP en veille, activer `Setup → Hardware → Network → Network Standby = On`.
- **Sécurité** : Changer le mot de passe par défaut du Web Setup (`admin`/`admin`) dans un environnement de production.
- **Timeouts** : Augmenter le timeout (`--timeout`) si le récepteur est lent à répondre sur le réseau.
- **MQTT Bridge** : Nécessite un broker MQTT (Mosquitto recommandé). Le bridge publie l'état toutes les 30s par défaut.
- **Web Dashboard** : Le serveur est conçu pour un usage local. Ne pas exposer directement sur Internet sans reverse proxy avec authentification.
