"""Tests unitaires pour mqtt_bridge.py"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mqtt_bridge import SOURCE_MAP, REVERSE_SOURCE_MAP, OnkyoMQTTBridge


class TestSourceMaps(unittest.TestCase):

    def test_source_map_not_empty(self):
        self.assertGreater(len(SOURCE_MAP), 0)

    def test_reverse_map_consistency(self):
        for code, name in SOURCE_MAP.items():
            self.assertEqual(REVERSE_SOURCE_MAP[name], code)

    def test_known_sources(self):
        self.assertEqual(SOURCE_MAP["27"], "NET")
        self.assertEqual(SOURCE_MAP["29"], "BLUETOOTH")
        self.assertEqual(SOURCE_MAP["07"], "TV")


class TestOnkyoMQTTBridgeInit(unittest.TestCase):

    @patch("mqtt_bridge.mqtt.Client")
    def test_valid_init(self, mock_client):
        bridge = OnkyoMQTTBridge(
            onkyo_host="192.168.1.100",
            mqtt_broker="192.168.1.50",
        )
        self.assertEqual(bridge.onkyo_url, "http://192.168.1.100")
        self.assertEqual(bridge.mqtt_broker, "192.168.1.50")
        self.assertEqual(bridge.mqtt_port, 1883)
        self.assertEqual(bridge.poll_interval, 30)

    @patch("mqtt_bridge.mqtt.Client")
    def test_custom_port(self, mock_client):
        bridge = OnkyoMQTTBridge(
            onkyo_host="192.168.1.100",
            mqtt_broker="192.168.1.50",
            mqtt_port=8883,
        )
        self.assertEqual(bridge.mqtt_port, 8883)

    @patch("mqtt_bridge.mqtt.Client")
    def test_mqtt_credentials(self, mock_client):
        bridge = OnkyoMQTTBridge(
            onkyo_host="192.168.1.100",
            mqtt_broker="192.168.1.50",
            mqtt_user="user",
            mqtt_password="pass",
        )
        mock_client.return_value.username_pw_set.assert_called_once_with(
            "user", "pass"
        )


class TestOnkyoMQTTBridgeHandlers(unittest.TestCase):

    @patch("mqtt_bridge.mqtt.Client")
    def setUp(self, mock_client):
        self.bridge = OnkyoMQTTBridge(
            onkyo_host="192.168.1.100",
            mqtt_broker="192.168.1.50",
        )
        self.bridge.mqtt_client = MagicMock()

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_power_on(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_power("ON")
        mock_post.assert_called_once_with("/Power/setPower", {"power": "on"})
        self.bridge.mqtt_client.publish.assert_called()

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_power_off(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_power("OFF")
        mock_post.assert_called_once_with("/Power/setPower", {"power": "standby"})

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_volume(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_volume("50")
        mock_post.assert_called_once_with("/Volume/setVolume", {"volume": 50})

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_volume_out_of_range(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_volume("99")
        mock_post.assert_called_once_with("/Volume/setVolume", {"volume": 80})

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_source(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_source("NET")
        mock_post.assert_called_once_with("/Source/setSource", {"source": "27"})

    def test_handle_source_unknown(self):
        self.bridge._handle_source("INVALID")
        self.bridge.mqtt_client.publish.assert_not_called()

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_listening_mode(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_listening_mode("DOLBY_ATMOS")
        mock_post.assert_called_once_with(
            "/ListeningMode/setListeningMode", {"mode": "LMDA"}
        )

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_mute_on(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_mute("ON")
        mock_post.assert_called_once_with("/Volume/setMute", {"mute": True})

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_zone2_power(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_zone2_power("ON")
        mock_post.assert_called_once_with("/Zone2/setPower", {"power": "on"})

    @patch.object(OnkyoMQTTBridge, '_http_post')
    def test_handle_zone2_volume(self, mock_post):
        mock_post.return_value = True
        self.bridge._handle_zone2_volume("30")
        mock_post.assert_called_once_with("/Zone2/setVolume", {"volume": 30})


if __name__ == "__main__":
    unittest.main()
