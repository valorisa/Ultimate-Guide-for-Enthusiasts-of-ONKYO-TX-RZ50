#!/usr/bin/env python3
"""
Contrôle RS-232 du ONKYO TX-RZ50 via le protocole ISCP.

Ce module fournit une interface en ligne de commande pour envoyer des commandes
série au récepteur AV ONKYO TX-RZ50 via un adaptateur USB-RS232 ou un port COM natif.

Le protocole ISCP (Integra Serial Control Protocol) est documenté par Onkyo
et permet le contrôle complet de l'appareil : alimentation, sélection de source,
volume, modes d'écoute, multizone, etc. [p.75-76]

Exemples d'utilisation :
    # Allumer l'appareil
    python rs232_control.py --port COM3 --command "POWER ON"
    
    # Régler le volume à 50
    python rs232_control.py --port COM3 --command "VOLUME SET 50"
    
    # Sélectionner la source NET
    python rs232_control.py --port COM3 --command "SOURCE NET"
    
    # Activer ZONE 2 avec source BLUETOOTH
    python rs232_control.py --port COM3 --command "ZONE2 SOURCE BLUETOOTH"

Documentation complète des commandes ISCP :
https://github.com/Onkyo/onkyo-iscp-protocol

Attributes:
    DEFAULT_TIMEOUT (int): Timeout par défaut pour les opérations série (5 secondes).
    DEFAULT_BAUDRATE (int): Vitesse de transmission par défaut (9600 bauds).

Todo:
    * Ajouter le support des commandes de retour d'état (query)
    * Implémenter un mode interactif avec historique des commandes
    * Ajouter des tests unitaires avec mock serial

.. _ISCP Protocol:
    https://github.com/Onkyo/onkyo-iscp-protocol

.. _pyserial documentation:
    https://pyserial.readthedocs.io/
"""

import argparse
import logging
import serial
import time
import sys
from typing import Optional, Dict, List
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / 'rs232_control.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Constantes du protocole ISCP [p.75-76]
ISCP_HEADER = b'!1'  # En-tête de commande ISCP
ISCP_END = b'\r'     # Caractère de fin de commande

# Mappage des commandes ISCP supportées
ISCP_COMMANDS: Dict[str, Dict[str, str]] = {
    'POWER': {
        'ON': '!1PWR01',
        'STANDBY': '!1PWR00',
        'QUERY': '!1PWRQSTN'
    },
    'VOLUME': {
        'UP': '!1MVLUP',
        'DOWN': '!1MVLDOWN',
        'SET': '!1MVL{:02X}',  # Format hexadécimal 00-50 (0-80 en décimal)
        'QUERY': '!1MVLQSTN'
    },
    'MUTING': {
        'ON': '!1AML01',
        'OFF': '!1AML00',
        'QUERY': '!1AMLQSTN'
    },
    'SOURCE': {
        'BD/DVD': '!1SLI00',
        'GAME': '!1SLI01',
        'CBL/SAT': '!1SLI02',
        'STRM BOX': '!1SLI03',
        'PC': '!1SLI04',
        'AUX': '!1SLI05',
        'CD': '!1SLI06',
        'TV': '!1SLI07',
        'PHONO': '!1SLI08',
        'NET': '!1SLI27',
        'USB': '!1SLI28',
        'BLUETOOTH': '!1SLI29',
        'TUNER': '!1SLI26',
        'QUERY': '!1SLIQSTN'
    },
    'LISTENING_MODE': {
        'STEREO': '!1LMST',
        'DIRECT': '!1LMDIR',
        'PURE_AUDIO': '!1LMPA',
        'DOLBY_ATMOS': '!1LMDA',
        'DTS_X': '!1LMDX',
        'THX_CINEMA': '!1LMTH',
        'QUERY': '!1LMQSTN'
    },
    'ZONE2': {
        'POWER_ON': '!1ZMT23010',
        'POWER_OFF': '!1ZMT23011',
        'SOURCE': '!1ZMT23{:02X}',  # Code source hexadécimal
        'VOLUME': '!1ZVL{:02X}',
        'QUERY': '!1ZMT23QSTN'
    }
}

# Mappage des codes source pour ZONE2 [p.108-109]
ZONE2_SOURCE_CODES: Dict[str, int] = {
    'BD/DVD': 0x00, 'GAME': 0x01, 'CBL/SAT': 0x02, 'STRM BOX': 0x03,
    'PC': 0x04, 'AUX': 0x05, 'CD': 0x06, 'TV': 0x07, 'PHONO': 0x08,
    'NET': 0x27, 'USB': 0x28, 'BLUETOOTH': 0x29, 'TUNER': 0x26
}


class RS232Controller:
    """
    Contrôleur RS-232 pour le ONKYO TX-RZ50.
    
    Cette classe encapsule la communication série avec le récepteur AV
    via le protocole ISCP. Elle gère la connexion, l'envoi de commandes,
    la réception de réponses et la gestion des erreurs.
    
    Attributes:
        port (str): Nom du port série (ex: 'COM3', '/dev/ttyUSB0').
        baudrate (int): Vitesse de transmission en bauds (par défaut: 9600).
        timeout (float): Timeout pour les opérations de lecture/écriture.
        ser (serial.Serial): Instance de la connexion série.
        
    Raises:
        serial.SerialException: Si le port série ne peut être ouvert.
        ValueError: Si les paramètres de connexion sont invalides.
        
    Example:
        >>> controller = RS232Controller(port='COM3')
        >>> controller.connect()
        >>> controller.send_command('POWER', 'ON')
        >>> controller.disconnect()
    """
    
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 5.0):
        """
        Initialise le contrôleur RS-232.
        
        Args:
            port: Nom du port série (ex: 'COM3' sous Windows, '/dev/ttyUSB0' sous Linux).
            baudrate: Vitesse de transmission en bauds (par défaut: 9600).
            timeout: Timeout en secondes pour les opérations série (par défaut: 5.0).
            
        Raises:
            ValueError: Si le port est vide ou si le baudrate est invalide.
        """
        if not port:
            raise ValueError("Le port série ne peut pas être vide")
        if baudrate not in [9600, 19200, 38400, 57600, 115200]:
            logger.warning(f"Baudrate {baudrate} non standard, utilisation de 9600")
            baudrate = 9600
            
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None
        logger.info(f"Initialisation du contrôleur RS-232: port={port}, baudrate={baudrate}")
    
    def connect(self) -> bool:
        """
        Établit la connexion série avec le TX-RZ50.
        
        Returns:
            bool: True si la connexion est réussie, False sinon.
            
        Raises:
            serial.SerialException: Si le port ne peut être ouvert.
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
                write_timeout=self.timeout
            )
            # Attendre que le port soit prêt
            time.sleep(0.1)
            logger.info(f"Connexion établie sur {self.port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Échec de connexion sur {self.port}: {e}")
            raise
    
    def disconnect(self) -> None:
        """Ferme la connexion série."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info(f"Connexion fermée sur {self.port}")
    
    def _build_command(self, category: str, action: str, value: Optional[str] = None) -> bytes:
        """
        Construit une commande ISCP à partir des paramètres.
        
        Args:
            category: Catégorie de commande (ex: 'POWER', 'VOLUME').
            action: Action à effectuer (ex: 'ON', 'SET').
            value: Valeur optionnelle pour l'action (ex: '50' pour le volume).
            
        Returns:
            bytes: La commande ISCP encodée, prête à être envoyée.
            
        Raises:
            KeyError: Si la catégorie ou l'action n'est pas supportée.
            ValueError: Si la valeur est requise mais manquante.
        """
        if category not in ISCP_COMMANDS:
            raise KeyError(f"Catégorie de commande non supportée: {category}")
        
        cmd_template = ISCP_COMMANDS[category].get(action)
        if not cmd_template:
            raise KeyError(f"Action non supportée: {category} {action}")
        
        if '{:' in cmd_template:
            if value is None:
                raise ValueError(f"Valeur requise pour l'action: {category} {action}")
            # Gestion spéciale pour ZONE2 SOURCE
            if category == 'ZONE2' and action == 'SOURCE':
                if value not in ZONE2_SOURCE_CODES:
                    raise ValueError(f"Source ZONE2 non reconnue: {value}")
                value = f"{ZONE2_SOURCE_CODES[value]:02X}"
            # Gestion du volume (décimal -> hexadécimal)
            elif category == 'VOLUME' and action == 'SET':
                try:
                    vol = int(value)
                    if not (0 <= vol <= 80):
                        raise ValueError("Volume doit être entre 0 et 80")
                    value = f"{vol:02X}"
                except ValueError:
                    raise ValueError(f"Volume invalide: {value}")
            return (cmd_template.format(value) + ISCP_END.decode()).encode('ascii')
        
        return (cmd_template + ISCP_END.decode()).encode('ascii')
    
    def send_command(self, category: str, action: str, value: Optional[str] = None) -> Optional[str]:
        """
        Envoie une commande au TX-RZ50 et retourne la réponse.
        
        Args:
            category: Catégorie de commande (ex: 'POWER', 'VOLUME').
            action: Action à effectuer (ex: 'ON', 'SET').
            value: Valeur optionnelle pour l'action.
            
        Returns:
            str: La réponse du récepteur, ou None si aucune réponse.
            
        Raises:
            RuntimeError: Si la connexion n'est pas établie.
            serial.SerialException: En cas d'erreur de communication.
        """
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Connexion série non établie. Appelez connect() d'abord.")
        
        try:
            cmd = self._build_command(category, action, value)
            logger.debug(f"Envoi commande: {cmd}")
            
            self.ser.write(cmd)
            self.ser.flush()
            
            # Attendre une réponse (optionnel, certaines commandes n'en ont pas)
            time.sleep(0.2)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('ascii', errors='ignore').strip()
                logger.debug(f"Réponse reçue: {response}")
                return response
            return None
            
        except serial.SerialException as e:
            logger.error(f"Erreur de communication: {e}")
            raise
    
    def __enter__(self):
        """Context manager: établit la connexion."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: ferme la connexion."""
        self.disconnect()
        return False


def parse_command_string(cmd_str: str) -> tuple:
    """
    Parse une chaîne de commande utilisateur en composants.
    
    Args:
        cmd_str: Chaîne de commande (ex: "POWER ON", "VOLUME SET 50").
        
    Returns:
        tuple: (category, action, value) ou (category, action, None).
        
    Raises:
        ValueError: Si la commande est mal formée.
        
    Example:
        >>> parse_command_string("POWER ON")
        ('POWER', 'ON', None)
        >>> parse_command_string("VOLUME SET 50")
        ('VOLUME', 'SET', '50')
    """
    parts = cmd_str.strip().upper().split(maxsplit=2)
    if len(parts) < 2:
        raise ValueError(f"Commande invalide: '{cmd_str}'. Format attendu: CATEGORY ACTION [VALUE]")
    
    category = parts[0]
    action = parts[1]
    value = parts[2] if len(parts) > 2 else None
    
    return category, action, value


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Contrôle RS-232 du ONKYO TX-RZ50 via le protocole ISCP [p.75-76]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s --port COM3 --command "POWER ON"
  %(prog)s --port COM3 --command "VOLUME SET 50"
  %(prog)s --port COM3 --command "SOURCE NET"
  %(prog)s --port COM3 --command "ZONE2 SOURCE BLUETOOTH" --verbose

Commandes supportées:
  POWER: ON, STANDBY
  VOLUME: UP, DOWN, SET <0-80>
  MUTING: ON, OFF
  SOURCE: BD/DVD, GAME, CBL/SAT, NET, USB, BLUETOOTH, TUNER, etc.
  LISTENING_MODE: STEREO, DIRECT, PURE_AUDIO, DOLBY_ATMOS, DTS_X, THX_CINEMA
  ZONE2: POWER_ON, POWER_OFF, SOURCE <name>, VOLUME <0-80>
        """
    )
    
    parser.add_argument(
        '--port', '-p',
        type=str,
        required=True,
        help="Port série (ex: COM3 sous Windows, /dev/ttyUSB0 sous Linux)"
    )
    parser.add_argument(
        '--command', '-c',
        type=str,
        required=True,
        help="Commande à envoyer (ex: 'POWER ON', 'VOLUME SET 50')"
    )
    parser.add_argument(
        '--baudrate', '-b',
        type=int,
        default=9600,
        choices=[9600, 19200, 38400, 57600, 115200],
        help="Vitesse de transmission en bauds (par défaut: 9600)"
    )
    parser.add_argument(
        '--timeout', '-t',
        type=float,
        default=5.0,
        help="Timeout en secondes pour les opérations série (par défaut: 5.0)"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Activer le mode verbeux (debug logging)"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        category, action, value = parse_command_string(args.command)
        logger.info(f"Commande parse: category={category}, action={action}, value={value}")
        
        with RS232Controller(port=args.port, baudrate=args.baudrate, timeout=args.timeout) as ctrl:
            response = ctrl.send_command(category, action, value)
            if response:
                print(f"Réponse: {response}")
            else:
                print("Commande envoyée avec succès (aucune réponse attendue)")
                
    except (KeyError, ValueError) as e:
        logger.error(f"Erreur de commande: {e}")
        print(f"Erreur: {e}", file=sys.stderr)
        print("Utilisez --help pour voir les commandes supportées", file=sys.stderr)
        sys.exit(1)
    except serial.SerialException as e:
        logger.error(f"Erreur série: {e}")
        print(f"Erreur de connexion série: {e}", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as e:
        logger.error(f"Erreur d'exécution: {e}")
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        logger.info("Interruption par l'utilisateur")
        sys.exit(130)


if __name__ == "__main__":
    main()
