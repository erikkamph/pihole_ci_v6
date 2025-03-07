from .const import DOMAIN
import logging
from .hole import PiHole
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform


_LOGGER = logging.getLogger(__name__)
_PLATFORMS = [
    Platform.SWITCH
]

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        hass.data[DOMAIN][config.entry_id] = PiHole(config.data)

        await hass.config_entries.async_forward_entry_setups(config, _PLATFORMS)
        return await PiHole.async_setup(config.data)
    except Exception as ex:
        _LOGGER.exception(ex, stack_info=True)
        return False


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(config.entry_id, _PLATFORMS)