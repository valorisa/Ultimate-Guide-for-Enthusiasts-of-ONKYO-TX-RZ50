"""Tests unitaires pour http_api_wrapper.py"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from http_api_wrapper import OnkyoHTTPClient, ENDPOINTS


class TestOnkyoHTTPClientInit(unittest.TestCase):

    def test_valid_host(self):
        client = OnkyoHTTPClient("192.168.1.100")
        self.assertEqual(client.base_url, "http://192.168.1.100")

    def test_host_with_schema_raises(self):
        with self.assertRaises(ValueError):
            OnkyoHTTPClient("http://192.168.1.100")

    def test_empty_host_raises(self):
        with self.assertRaises(ValueError):
            OnkyoHTTPClient("")

    def test_custom_credentials(self):
        client = OnkyoHTTPClient("192.168.1.100", username="user", password="pass")
        self.assertEqual(client.auth.username, "user")
        self.assertEqual(client.auth.password, "pass")


class TestOnkyoHTTPClientMethods(unittest.TestCase):

    def setUp(self):
        self.client = OnkyoHTTPClient("192.168.1.100")

    @patch.object(OnkyoHTTPClient, '_request')
    def test_get_status(self, mock_request):
        mock_request.return_value = {"power": "on", "volume": 40}
        result = self.client.get_status()
        mock_request.assert_called_once_with("GET", ENDPOINTS["status"])
        self.assertEqual(result["power"], "on")

    @patch.object(OnkyoHTTPClient, '_request')
    def test_get_network_info(self, mock_request):
        mock_request.return_value = {"ip": "192.168.1.100"}
        result = self.client.get_network_info()
        mock_request.assert_called_once_with("GET", ENDPOINTS["network"])

    @patch.object(OnkyoHTTPClient, '_request')
    def test_get_firmware_version(self, mock_request):
        mock_request.return_value = {"version": "1.1.0"}
        result = self.client.get_firmware_version()
        mock_request.assert_called_once_with("GET", ENDPOINTS["firmware"])

    @patch.object(OnkyoHTTPClient, '_request')
    def test_set_power_on(self, mock_request):
        mock_request.return_value = {"success": True}
        result = self.client.set_power(True)
        mock_request.assert_called_once_with(
            "POST", ENDPOINTS["power"], {"power": "on"}
        )

    @patch.object(OnkyoHTTPClient, '_request')
    def test_set_power_off(self, mock_request):
        mock_request.return_value = {"success": True}
        result = self.client.set_power(False)
        mock_request.assert_called_once_with(
            "POST", ENDPOINTS["power"], {"power": "standby"}
        )

    @patch.object(OnkyoHTTPClient, '_request')
    def test_set_volume(self, mock_request):
        mock_request.return_value = {"success": True}
        result = self.client.set_volume(50)
        mock_request.assert_called_once_with(
            "POST", ENDPOINTS["volume"], {"volume": 50}
        )

    def test_set_volume_out_of_range(self):
        with self.assertRaises(ValueError):
            self.client.set_volume(101)
        with self.assertRaises(ValueError):
            self.client.set_volume(-1)

    @patch.object(OnkyoHTTPClient, '_request')
    def test_set_source(self, mock_request):
        mock_request.return_value = {"success": True}
        result = self.client.set_source("NET")
        mock_request.assert_called_once_with(
            "POST", ENDPOINTS["source"], {"source": "NET"}
        )

    def test_context_manager(self):
        with patch.object(self.client, 'close') as mock_close:
            with self.client as c:
                pass
            mock_close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
