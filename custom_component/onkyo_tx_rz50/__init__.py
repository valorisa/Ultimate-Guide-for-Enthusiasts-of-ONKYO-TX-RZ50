"""Custom Component ONKYO TX-RZ50 pour Home Assistant."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN

PLATFORMS = ["media_player"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure le composant ONKYO TX-RZ50."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_HOST: entry.data[CONF_HOST],
        CONF_USERNAME: entry.data.get(CONF_USERNAME, "admin"),
        CONF_PASSWORD: entry.data.get(CONF_PASSWORD, "admin"),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharge le composant."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
