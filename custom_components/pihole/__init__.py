from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        await hass.config_entries.async_forward_entry_setups(config, [Platform.SWITCH])
        return True
    except ConfigEntryNotReady as ex:
        _LOGGER.error(ex)
        return False