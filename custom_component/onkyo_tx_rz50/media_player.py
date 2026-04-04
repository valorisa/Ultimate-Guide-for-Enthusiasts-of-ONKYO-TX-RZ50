"""Media Player ONKYO TX-RZ50 pour Home Assistant."""

from __future__ import annotations

import logging
from typing import Any

import requests
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from requests.auth import HTTPBasicAuth

from .const import DOMAIN, MANUFACTURER, MODEL, REVERSE_SOURCES, SOURCES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configure le media player ONKYO TX-RZ50."""
    host = entry.data["host"]
    username = entry.data.get("username", "admin")
    password = entry.data.get("password", "admin")
    async_add_entities([OnkyoTXRZ50MediaPlayer(host, username, password)])


class OnkyoTXRZ50MediaPlayer(MediaPlayerEntity):
    """Représentation du media player ONKYO TX-RZ50."""

    _attr_name = "ONKYO TX-RZ50"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._auth = HTTPBasicAuth(username, password)
        self._base_url = f"http://{host}"
        self._attr_unique_id = f"onkyo_tx_rz50_{host}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="ONKYO TX-RZ50",
        )
        self._power = "off"
        self._volume = 0
        self._source = None
        self._muted = False

    def _api_get(self, endpoint: str) -> dict | None:
        """GET vers l'API du TX-RZ50."""
        try:
            r = requests.get(
                f"{self._base_url}{endpoint}", auth=self._auth, timeout=5
            )
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            _LOGGER.error("Erreur API GET %s: %s", endpoint, e)
            return None

    def _api_post(self, endpoint: str, payload: dict) -> bool:
        """POST vers l'API du TX-RZ50."""
        try:
            r = requests.post(
                f"{self._base_url}{endpoint}",
                json=payload,
                auth=self._auth,
                timeout=5,
            )
            r.raise_for_status()
            return True
        except requests.RequestException as e:
            _LOGGER.error("Erreur API POST %s: %s", endpoint, e)
            return False

    def update(self) -> None:
        """Met à jour l'état du récepteur."""
        data = self._api_get("/Status/getStatus")
        if data is None:
            return

        self._power = data.get("power", "off")
        self._volume = data.get("volume", 0)
        src_code = str(data.get("source", "00"))
        self._source = SOURCES.get(src_code)

    @property
    def state(self) -> MediaPlayerState:
        """État actuel du media player."""
        if self._power == "on":
            return MediaPlayerState.ON
        return MediaPlayerState.OFF

    @property
    def volume_level(self) -> float:
        """Volume normalisé (0-1)."""
        return self._volume / 80

    @property
    def source(self) -> str | None:
        """Source actuelle."""
        return self._source

    @property
    def source_list(self) -> list[str]:
        """Liste des sources disponibles."""
        return list(SOURCES.values())

    @property
    def is_volume_muted(self) -> bool:
        """État du mute."""
        return self._muted

    def turn_on(self) -> None:
        """Allume le récepteur."""
        self._api_post("/Power/setPower", {"power": "on"})

    def turn_off(self) -> None:
        """Met le récepteur en veille."""
        self._api_post("/Power/setPower", {"power": "standby"})

    def set_volume_level(self, volume: float) -> None:
        """Règle le volume (0-1 -> 0-80)."""
        level = int(volume * 80)
        self._api_post("/Volume/setVolume", {"volume": level})

    def mute_volume(self, mute: bool) -> None:
        """Active/désactive le mute."""
        self._api_post("/Volume/setMute", {"mute": mute})
        self._muted = mute

    def select_source(self, source: str) -> None:
        """Sélectionne une source."""
        code = REVERSE_SOURCES.get(source)
        if code:
            self._api_post("/Source/setSource", {"source": code})
