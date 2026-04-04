"""Tests unitaires pour log_parser.py"""

import sys
import os
import json
import csv
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from log_parser import (
    parse_line,
    parse_log_file,
    export_to_csv,
    export_to_json,
    load_error_map,
    ERROR_CODE_MAP,
)


class TestLoadErrorMap(unittest.TestCase):

    def test_error_map_not_empty(self):
        err_map = load_error_map()
        self.assertGreater(len(err_map), 0)

    def test_known_errors_present(self):
        err_map = load_error_map()
        self.assertIn("NG:", err_map)
        self.assertIn("CH SP WIRE", err_map)


class TestParseLine(unittest.TestCase):

    def test_iscp_command(self):
        result = parse_line("!1PWR01")
        self.assertEqual(result["type"], "command")

    def test_iscp_query(self):
        result = parse_line("!1PWRQSTN")
        self.assertEqual(result["type"], "query")

    def test_http_get(self):
        result = parse_line("GET /Status/getStatus HTTP/1.1")
        self.assertEqual(result["type"], "http_request")

    def test_http_post(self):
        result = parse_line("POST /Power/setPower HTTP/1.1")
        self.assertEqual(result["type"], "http_action")

    def test_error_ng(self):
        result = parse_line("NG: 12345 hardware failure")
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["severity"], "critical")

    def test_error_amp_diag(self):
        result = parse_line("AMP Diag Mode activated")
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["severity"], "critical")

    def test_error_ch_sp_wire(self):
        result = parse_line("CH SP WIRE detected")
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["severity"], "warning")

    def test_generic_error(self):
        result = parse_line("Something ERROR happened")
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["severity"], "warning")

    def test_generic_fail(self):
        result = parse_line("Connection FAIL")
        self.assertEqual(result["type"], "error")

    def test_status_success(self):
        result = parse_line("Operation SUCCESS")
        self.assertEqual(result["type"], "status")

    def test_status_completed(self):
        result = parse_line("Task COMPLETED")
        self.assertEqual(result["type"], "status")

    def test_unknown_line(self):
        result = parse_line("random log line without patterns")
        self.assertEqual(result["type"], "unknown")
        self.assertEqual(result["severity"], "info")

    def test_timestamp_extraction(self):
        result = parse_line("2024-04-01 12:00:00 !1PWR01")
        self.assertEqual(result["timestamp"], "2024-04-01 12:00:00")

    def test_error_desc_populated(self):
        result = parse_line("NG: 99999 critical failure")
        self.assertIsNotNone(result["error_desc"])


class TestParseLogFile(unittest.TestCase):

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            parse_log_file(Path("/nonexistent/file.log"))

    def test_parse_serial_log(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as f:
            f.write("!1PWR01\n")
            f.write("!1MVL30\n")
            f.write("POST /api HTTP/1.1\n")
            f.flush()
            tmp = Path(f.name)

        try:
            events = parse_log_file(tmp, log_format="serial")
            serial_events = [e for e in events if "http" not in e["type"]]
            self.assertEqual(len(serial_events), 2)
        finally:
            tmp.unlink()

    def test_parse_http_log(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as f:
            f.write("GET /Status/getStatus HTTP/1.1\n")
            f.write("!1PWR01\n")
            f.flush()
            tmp = Path(f.name)

        try:
            events = parse_log_file(tmp, log_format="http")
            http_events = [e for e in events if "http" in e["type"]]
            self.assertEqual(len(http_events), 1)
        finally:
            tmp.unlink()

    def test_parse_auto(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as f:
            f.write("!1PWR01\n")
            f.write("GET /Status HTTP/1.1\n")
            f.flush()
            tmp = Path(f.name)

        try:
            events = parse_log_file(tmp, log_format="auto")
            self.assertEqual(len(events), 2)
        finally:
            tmp.unlink()


class TestExportFunctions(unittest.TestCase):

    def test_export_to_json(self):
        events = [
            {"timestamp": "2024-01-01 00:00:00", "type": "command", "severity": "info", "payload": "!1PWR01", "error_desc": None}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmp = Path(f.name)
        try:
            export_to_json(events, tmp)
            data = json.loads(tmp.read_text(encoding='utf-8'))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["type"], "command")
        finally:
            tmp.unlink()

    def test_export_to_csv(self):
        events = [
            {"timestamp": "2024-01-01 00:00:00", "type": "command", "severity": "info", "payload": "!1PWR01", "error_desc": None}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp = Path(f.name)
        try:
            export_to_csv(events, tmp)
            with open(tmp, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["type"], "command")
        finally:
            tmp.unlink()

    def test_export_empty_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmp = Path(f.name)
        try:
            export_to_json([], tmp)
            content = tmp.read_text(encoding='utf-8')
            self.assertEqual(content, '')
        finally:
            tmp.unlink()

    def test_export_empty_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            tmp = Path(f.name)
        try:
            export_to_csv([], tmp)
            content = tmp.read_text(encoding='utf-8')
            self.assertEqual(content, '')
        finally:
            tmp.unlink()


if __name__ == "__main__":
    unittest.main()
