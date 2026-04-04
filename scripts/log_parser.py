#!/usr/bin/env python3
"""
Analyseur de logs série (ISCP) et HTTP pour le ONKYO TX-RZ50.

Ce module parse les fichiers de logs bruts ou structurés générés par les scripts
de contrôle. Il identifie les événements, traduit les codes d'erreur documentés
dans le manuel officiel [p.9-10, p.171-181], et permet l'export filtré en CSV/JSON.

Fonctionnalités :
- Extraction d'événements (Power, Volume, Source, Zone, Error, Status)
- Dictionnaire de traduction des codes d'erreur Onkyo
- Filtres par type, plage horaire ou sévérité
- Export vers CSV (tableau croisé) ou JSON (données structurées)

Exemples d'utilisation :
    python log_parser.py --input rs232_control.log --format serial --output errors.json
    python log_parser.py --input http_api.log --format http --output summary.csv --filter Error
    python log_parser.py --input mixed.log --format auto --export both --timezone UTC

Attributes:
    ERROR_CODE_MAP (dict): Correspondance code d'erreur -> description (manuel TX-RZ50).
    ISCP_PATTERN (re): Regex pour capturer les commandes/réponses ISCP.
    HTTP_PATTERN (re): Regex pour capturer les requêtes/réponses HTTP.

Todo:
    * Ajouter la détection automatique du format (serial/http/mixte)
    * Support des logs syslog/Journald
    * Visualisation temporelle (matplotlib optionnel)
"""

import argparse
import csv
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Mappage des codes d'erreur documentés [p.9-10, p.171-181]
ERROR_CODE_MAP: Dict[str, str] = {
    "**-01": "Câble Ethernet introuvable ou déconnecté",
    "**-05": "Fichier de mise à jour firmware manquant sur le support USB",
    "**-10": "Périphérique USB non reconnu ou non alimenté",
    "**-13": "Fichier firmware incompatible ou corrompu",
    "CH SP WIRE": "Circuit de protection activé : court-circuit probable sur les bornes d'enceintes",
    "AMP Diag Mode": "Mode diagnostic amplificateur activé (vérification câblage enceintes)",
    "NG:": "Défaillance matérielle détectée : débrancher l'appareil et contacter le SAV",
    "Resolution Error": "Résolution vidéo d'entrée non supportée par le téléviseur",
    "Noise Error": "Bruit détecté pendant le calibrage AccuEQ : vérifier le micro et les enceintes"
}

# Patterns de parsing
ISCP_PATTERN = re.compile(r"(!1\w+|\w+QSTN|\w+\d{2,3})")
HTTP_PATTERN = re.compile(r"(GET|POST)\s+(/[^\s]+)\s+HTTP/\d\.\d")
TIMESTAMP_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})")

def load_error_map() -> Dict[str, str]:
    """Retourne le dictionnaire des codes d'erreur avec fallback."""
    return ERROR_CODE_MAP

def parse_line(line: str) -> Dict[str, Any]:
    """
    Analyse une ligne de log et retourne un dictionnaire structuré.
    
    Args:
        line: Ligne brute du fichier de log.
        
    Returns:
        Dict avec keys: timestamp, type, payload, severity, error_desc (si applicable).
    """
    result: Dict[str, Any] = {
        "timestamp": None,
        "type": "unknown",
        "payload": line.strip(),
        "severity": "info",
        "error_desc": None
    }
    
    ts_match = TIMESTAMP_PATTERN.search(line)
    if ts_match:
        result["timestamp"] = ts_match.group(1)
        
    # Détection ISCP (Série)
    if ISCP_PATTERN.search(line):
        result["type"] = "serial_iscp"
        if "QSTN" in line.upper():
            result["type"] = "query"
        elif any(cmd in line.upper() for cmd in ["PWR", "MVL", "SLI", "ZMT", "ZVL"]):
            result["type"] = "command"
            
    # Détection HTTP
    elif HTTP_PATTERN.search(line):
        result["type"] = "http_request"
        if "POST" in line:
            result["type"] = "http_action"
            
    # Détection Erreurs & Status
    line_upper = line.upper()
    error_found = False
    for code, desc in load_error_map().items():
        if code.upper() in line_upper:
            result["type"] = "error"
            result["severity"] = "critical" if "NG:" in code or "AMP Diag" in code else "warning"
            result["error_desc"] = desc
            error_found = True
            break
    if not error_found:
        if "ERROR" in line_upper or "FAIL" in line_upper:
            result["type"] = "error"
            result["severity"] = "warning"
        elif "SUCCESS" in line_upper or "COMPLETED" in line_upper:
            result["type"] = "status"
            result["severity"] = "info"
        
    return result

def parse_log_file(filepath: Path, log_format: str = "auto") -> List[Dict[str, Any]]:
    """
    Parse l'intégralité d'un fichier de log.
    
    Args:
        filepath: Chemin du fichier de log.
        log_format: 'serial', 'http', ou 'auto'.
        
    Returns:
        Liste de dictionnaires d'événements parsés.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Le fichier de log n'existe pas : {filepath}")
        
    events = []
    logger.info(f"Parsing du fichier : {filepath} (format: {log_format})")
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                evt = parse_line(line)
                # Filtre basique sur le format demandé
                if log_format == "serial" and "http" in evt["type"]:
                    continue
                if log_format == "http" and "serial" in evt["type"]:
                    continue
                events.append(evt)
    except Exception as e:
        logger.error(f"Erreur de lecture du fichier : {e}")
        raise
        
    logger.info(f"{len(events)} événements extraits.")
    return events

def export_to_csv(events: List[Dict[str, Any]], output_path: Path) -> None:
    """Exporte les événements en CSV."""
    if not events:
        logger.warning("Aucune donnée à exporter.")
        return
        
    keys = ["timestamp", "type", "severity", "payload", "error_desc"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(events)
    logger.info(f"Export CSV réussi : {output_path}")

def export_to_json(events: List[Dict[str, Any]], output_path: Path) -> None:
    """Exporte les événements en JSON."""
    if not events:
        logger.warning("Aucune donnée à exporter.")
        return
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    logger.info(f"Export JSON réussi : {output_path}")

def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Analyseur de logs RS-232/HTTP pour ONKYO TX-RZ50",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s --input rs232_control.log --format serial --output report.json
  %(prog)s --input api_trace.log --format http --filter Error --output errors.csv
  %(prog)s --input mixed.log --format auto --export both
        """
    )
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier de log à analyser")
    parser.add_argument("--format", "-f", choices=["serial", "http", "auto"], default="auto", help="Format attendu du log")
    parser.add_argument("--filter", choices=["Error", "Warning", "Info", "Command"], default=None, help="Filtrer par type/sévérité")
    parser.add_argument("--output", "-o", default=None, help="Fichier de sortie (CSV ou JSON)")
    parser.add_argument("--export", choices=["csv", "json", "both"], default="csv", help="Format d'export")
    parser.add_argument("--timezone", default="local", help="Fuseau horaire pour les timestamps (non implémenté v1)")
    
    args = parser.parse_args()
    input_path = Path(args.input)
    
    try:
        events = parse_log_file(input_path, args.format)
        
        # Application du filtre
        if args.filter:
            if args.filter in ["Error", "Warning", "Info"]:
                events = [e for e in events if e.get("severity", "").lower() == args.filter.lower()]
            elif args.filter == "Command":
                events = [e for e in events if "command" in e.get("type", "")]
                
        if not events:
            print("⚠️ Aucun événement ne correspond aux critères.")
            return
            
        # Affichage console résumé
        print(f"\n📊 Résumé ({len(events)} événements) :")
        print(f"  - Erreurs : {sum(1 for e in events if e['severity']=='critical' or e['severity']=='warning')}")
        print(f"  - Commandes : {sum(1 for e in events if 'command' in e['type'])}")
        print(f"  - Statuts : {sum(1 for e in events if 'status' in e['type'])}\n")
        
        # Export
        if args.output:
            out_path = Path(args.output)
            if args.export == "csv" or args.export == "both":
                export_to_csv(events, out_path.with_suffix(".csv"))
            if args.export == "json" or args.export == "both":
                export_to_json(events, out_path.with_suffix(".json"))
        else:
            # Fallback console
            for e in events[:10]:  # Affiche les 10 premiers
                print(f"[{e['timestamp']}] {e['type'].upper()} | {e['severity']} | {e['error_desc'] or e['payload'][:80]}")
            if len(events) > 10:
                print(f"... et {len(events)-10} autres entrées (utilisez --output pour exporter)")
                
    except Exception as e:
        logger.error(f"Échec de l'analyse : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
