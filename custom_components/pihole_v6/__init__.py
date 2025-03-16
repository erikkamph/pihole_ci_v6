from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
import logging
from .coordinator import PiHoleUpdateCoordinator
from .models.const import (
    DOMAIN
)
from .models.config import PiHoleConfig
from .data import PiHoleData
from .models.const import (CONF_SID, CONF_CSRF)
from homeassistant.const import CONF_API_KEY
from typing import Any
from homeassistant.helpers.redact import async_redact_data

_LOGGER = logging.getLogger(__name__)
platforms = [
    Platform.SWITCH,
    Platform.SENSOR
]
TO_REDACT = [
    CONF_SID,
    CONF_CSRF,
    CONF_API_KEY
]


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": entry.runtime_data.coordinator.data
    }


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        hass.data[DOMAIN][config.entry_id] = []
        coordinator = PiHoleUpdateCoordinator(hass, config)

        await coordinator.async_config_entry_first_refresh()
        config.runtime_data = PiHoleData(coordinator, PiHoleConfig(**config.data))
        

        await hass.config_entries.async_forward_entry_setups(config, platforms)
        return True
    except ConfigEntryNotReady as ex:
        _LOGGER.error(ex)
        return False


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry):
    await hass.config_entries.async_unload_platforms(config, platforms)

    entities = hass.data.get(DOMAIN, {}).get(config.entry_id, [])
    for entity in entities:
        await entity.async_remove(force_remove=True)

    return await hass.config_entries.async_unload(config.entry_id)


async def async_remove_entry(hass: HomeAssistant, config: ConfigEntry):
    await hass.config_entries.async_unload_platforms(config, platforms)

    for entity in hass.data.get(DOMAIN, {}).get(config.entry_id, []):
        await entity.async_remove(force_remove=True)

    await hass.config_entries.async_remove(config.entry_id)
    return True