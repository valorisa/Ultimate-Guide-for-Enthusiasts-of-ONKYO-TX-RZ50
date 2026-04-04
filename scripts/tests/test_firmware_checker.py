"""Tests unitaires pour firmware_checker.py"""

import sys
import os
import json
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from firmware_checker import FirmwareChecker, VERSION_PATTERN


class TestVersionPattern(unittest.TestCase):

    def test_valid_version(self):
        match = VERSION_PATTERN.search("Firmware version 1.2.3")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "1.2.3")

    def test_no_version(self):
        match = VERSION_PATTERN.search("No version here")
        self.assertIsNone(match)


class TestFirmwareCheckerInit(unittest.TestCase):

    def test_valid_init(self):
        checker = FirmwareChecker("192.168.1.100")
        self.assertEqual(checker.base_url, "http://192.168.1.100")

    def test_host_with_schema_raises(self):
        with self.assertRaises(ValueError):
            FirmwareChecker("http://192.168.1.100")

    def test_empty_host_raises(self):
        with self.assertRaises(ValueError):
            FirmwareChecker("")

    def test_custom_credentials(self):
        checker = FirmwareChecker("192.168.1.100", username="user", password="pass")
        self.assertEqual(checker.auth.username, "user")
        self.assertEqual(checker.auth.password, "pass")


class TestFirmwareCheckerMethods(unittest.TestCase):

    def setUp(self):
        self.checker = FirmwareChecker("192.168.1.100")

    @patch.object(FirmwareChecker, '_fetch_json')
    def test_get_current_version_json(self, mock_fetch):
        mock_fetch.return_value = {"firmware": "v1.1.0"}
        version = self.checker.get_current_version()
        self.assertEqual(version, "1.1.0")

    @patch.object(FirmwareChecker, '_fetch_json')
    @patch.object(FirmwareChecker, '_fetch_page')
    def test_get_current_version_html_fallback(self, mock_page, mock_json):
        mock_json.return_value = None
        mock_page.return_value = "<html>Firmware: 2.0.0</html>"
        version = self.checker.get_current_version()
        self.assertEqual(version, "2.0.0")

    @patch.object(FirmwareChecker, '_fetch_json')
    @patch.object(FirmwareChecker, '_fetch_page')
    def test_get_current_version_none(self, mock_page, mock_json):
        mock_json.return_value = None
        mock_page.return_value = None
        version = self.checker.get_current_version()
        self.assertIsNone(version)

    def test_get_latest_reference_local_file(self):
        tmp = Path("test_fw_version.json")
        tmp.write_text(json.dumps({"latest_version": "1.2.0"}), encoding="utf-8")
        with patch('firmware_checker.DEFAULT_VERSION_FILE', tmp):
            version = self.checker.get_latest_reference()
            self.assertEqual(version, "1.2.0")
        tmp.unlink()

    def test_get_latest_reference_no_file(self):
        with patch('firmware_checker.DEFAULT_VERSION_FILE', new_callable=PropertyMock) as mock_file:
            tmp = Path("nonexistent_fw_version.json")
            mock_file.return_value = tmp
            version = self.checker.get_latest_reference()
            self.assertIsNone(version)

    @patch.object(FirmwareChecker, 'get_current_version')
    @patch.object(FirmwareChecker, 'get_latest_reference')
    def test_check_update_available(self, mock_latest, mock_current):
        mock_current.return_value = "1.0.0"
        mock_latest.return_value = "1.1.0"
        result = self.checker.check_update()
        self.assertTrue(result["update_available"])
        self.assertEqual(result["current"], "1.0.0")
        self.assertEqual(result["latest"], "1.1.0")

    @patch.object(FirmwareChecker, 'get_current_version')
    @patch.object(FirmwareChecker, 'get_latest_reference')
    def test_check_up_to_date(self, mock_latest, mock_current):
        mock_current.return_value = "1.1.0"
        mock_latest.return_value = "1.1.0"
        result = self.checker.check_update()
        self.assertFalse(result["update_available"])

    @patch.object(FirmwareChecker, 'get_current_version')
    def test_check_current_unavailable(self, mock_current):
        mock_current.return_value = None
        result = self.checker.check_update()
        self.assertFalse(result["update_available"])
        self.assertIsNone(result["current"])

    def test_save_version(self):
        tmp = Path("test_save_version.json")
        with patch('firmware_checker.DEFAULT_VERSION_FILE', tmp):
            self.checker.save_version("1.3.0")
            data = json.loads(tmp.read_text(encoding="utf-8"))
            self.assertEqual(data["latest_version"], "1.3.0")
            tmp.unlink()


if __name__ == "__main__":
    unittest.main()
