import logging
from homeassistant.const import Platform, CONF_API_KEY, CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.redact import async_redact_data
from homeassistant.components import system_health
from typing import Any
from .coordinator import PiHoleUpdateCoordinator
from .models.config import PiHoleConfig
from .models.const import (CONF_SID, CONF_CSRF, DOMAIN)
from .data import PiHoleData
from .hole import PiHole

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

@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    register.async_register_info(system_health_info)


async def system_health_info(hass: HomeAssistant) -> dict[str, Any]:
    config_entry: ConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]
    api = PiHole(hass, config_entry)
    
    return {
        "can_reach_server": system_health.async_check_can_reach_url(hass, api.config.api_url)
    }


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": entry.runtime_data.coordinator.data
    }


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        coordinator = PiHoleUpdateCoordinator(hass, config)

        await coordinator.async_config_entry_first_refresh()
        config.runtime_data = PiHoleData(coordinator, PiHoleConfig(**config.data))

        await hass.config_entries.async_forward_entry_setups(config, platforms)
        return True
    except Exception as ex:
        _LOGGER.error(ex)
        raise ConfigEntryNotReady(f"Error setting up host: {config.data[CONF_HOST]}") from ex


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry):
    for entity in config.runtime_data.entities:
        await entity.async_remove()
    return await hass.config_entries.async_unload_platforms(config, platforms)