from .const import DOMAIN
import logging
from .hole import PiHole
from .switch import ToggleHole
from homeassistant.const import CONF_URL, CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        hass.data[DOMAIN][config.entry_id] = PiHole(config.data[CONF_URL], config.data[CONF_API_KEY])
        return await PiHole.async_setup(config.data)
    except Exception as ex:
        _LOGGER.exception(ex, stack_info=True)
        return False


async def async_setup_platform(hass: HomeAssistant, config: ConfigEntry, async_add_entities, discovery_info=None):
    """Set up platform."""
    device = hass.data[DOMAIN][config.entry_id]
    async_add_entities([ToggleHole(device)], update_before_add=True)