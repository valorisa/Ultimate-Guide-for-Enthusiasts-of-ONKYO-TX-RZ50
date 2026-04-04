"""Tests unitaires pour rs232_control.py"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rs232_control import (
    ISCP_COMMANDS,
    ZONE2_SOURCE_CODES,
    RS232Controller,
    parse_command_string,
)


class TestParseCommandString(unittest.TestCase):

    def test_simple_command(self):
        cat, action, val = parse_command_string("POWER ON")
        self.assertEqual(cat, "POWER")
        self.assertEqual(action, "ON")
        self.assertIsNone(val)

    def test_command_with_value(self):
        cat, action, val = parse_command_string("VOLUME SET 50")
        self.assertEqual(cat, "VOLUME")
        self.assertEqual(action, "SET")
        self.assertEqual(val, "50")

    def test_invalid_command(self):
        with self.assertRaises(ValueError):
            parse_command_string("INVALID")

    def test_lowercase_normalized(self):
        cat, action, val = parse_command_string("power on")
        self.assertEqual(cat, "POWER")
        self.assertEqual(action, "ON")


class TestISCPCommands(unittest.TestCase):

    def test_power_on_command(self):
        self.assertEqual(ISCP_COMMANDS["POWER"]["ON"], "!1PWR01")

    def test_power_standby_command(self):
        self.assertEqual(ISCP_COMMANDS["POWER"]["STANDBY"], "!1PWR00")

    def test_volume_set_template(self):
        self.assertIn("{:", ISCP_COMMANDS["VOLUME"]["SET"])

    def test_zone2_source_codes(self):
        self.assertEqual(ZONE2_SOURCE_CODES["BLUETOOTH"], 0x29)
        self.assertEqual(ZONE2_SOURCE_CODES["NET"], 0x27)


class TestRS232ControllerInit(unittest.TestCase):

    def test_valid_init(self):
        ctrl = RS232Controller(port="COM3")
        self.assertEqual(ctrl.port, "COM3")
        self.assertEqual(ctrl.baudrate, 9600)

    def test_empty_port_raises(self):
        with self.assertRaises(ValueError):
            RS232Controller(port="")

    def test_invalid_baudrate_fallback(self):
        ctrl = RS232Controller(port="COM3", baudrate=4800)
        self.assertEqual(ctrl.baudrate, 9600)

    def test_valid_baudrate(self):
        ctrl = RS232Controller(port="COM3", baudrate=19200)
        self.assertEqual(ctrl.baudrate, 19200)


class TestRS232ControllerBuildCommand(unittest.TestCase):

    def setUp(self):
        self.ctrl = RS232Controller(port="COM3")

    def test_power_on(self):
        cmd = self.ctrl._build_command("POWER", "ON")
        self.assertEqual(cmd, b"!1PWR01\r")

    def test_volume_set(self):
        cmd = self.ctrl._build_command("VOLUME", "SET", "40")
        self.assertEqual(cmd, b"!1MVL28\r")

    def test_volume_out_of_range(self):
        with self.assertRaises(ValueError):
            self.ctrl._build_command("VOLUME", "SET", "99")

    def test_invalid_category(self):
        with self.assertRaises(KeyError):
            self.ctrl._build_command("INVALID", "ON")

    def test_invalid_action(self):
        with self.assertRaises(KeyError):
            self.ctrl._build_command("POWER", "INVALID")

    def test_zone2_source(self):
        cmd = self.ctrl._build_command("ZONE2", "SOURCE", "BLUETOOTH")
        self.assertEqual(cmd, b"!1ZMT2329\r")

    def test_zone2_source_invalid(self):
        with self.assertRaises(ValueError):
            self.ctrl._build_command("ZONE2", "SOURCE", "INVALID")

    def test_missing_value_for_set(self):
        with self.assertRaises(ValueError):
            self.ctrl._build_command("VOLUME", "SET")


class TestRS232ControllerSend(unittest.TestCase):

    def setUp(self):
        self.ctrl = RS232Controller(port="COM3")

    def test_send_without_connection_raises(self):
        with self.assertRaises(RuntimeError):
            self.ctrl.send_command("POWER", "ON")

    @patch("rs232_control.serial.Serial")
    def test_send_command_success(self, mock_serial_cls):
        mock_ser = MagicMock()
        mock_ser.is_open = True
        mock_ser.in_waiting = 0
        mock_serial_cls.return_value = mock_ser

        self.ctrl.connect()
        result = self.ctrl.send_command("POWER", "ON")
        mock_ser.write.assert_called_once()
        self.assertIsNone(result)

    @patch("rs232_control.serial.Serial")
    def test_context_manager(self, mock_serial_cls):
        mock_ser = MagicMock()
        mock_ser.is_open = True
        mock_ser.in_waiting = 0
        mock_serial_cls.return_value = mock_ser

        with RS232Controller(port="COM3") as ctrl:
            ctrl.send_command("POWER", "ON")
        mock_ser.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
