import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
import logging
from homeassistant.helpers.entity_platform import async_get_current_platform
from homeassistant.helpers import config_validation as cv
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)
from .models.const import (
    SERVICE_DISABLE,
    SERVICE_DISABLE_ATTR_DURATION,
    MIN_TIME_BETWEEN_UPDATES,
    DOMAIN
)
from .models.config import PiHoleConfig
from .hole import PiHole
from .data import PiHoleConfigData

_LOGGER = logging.getLogger(__name__)
platforms = [
    Platform.SWITCH
]


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    entry.runtime_data = PiHoleConfigData(None, None, None)
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: PiHoleConfigData):
    try:
        platform = async_get_current_platform()
        platform.async_register_entity_service(
            SERVICE_DISABLE,
            {
                vol.Required(SERVICE_DISABLE_ATTR_DURATION): vol.All(
                    cv.time_period_str, cv.positive_timedelta
                )
            },
            "async_disable"
        )

        api = PiHole(hass, config)
        async def async_update_data() -> None:
            try:
                if not await api.verify_session():
                    await api.update_session()
                
                await api.update_blocking()
                await api.update_versions()
                await api.update_statistics()
            except Exception as ex:
                raise UpdateFailed(f"Failed to communicate with the API: {ex}") from ex
            if not isinstance(api.data, dict):
                raise ConfigEntryAuthFailed

        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            config_entry=config,
            name=api.config.name,
            update_method=async_update_data,
            update_interval=MIN_TIME_BETWEEN_UPDATES
        )

        await coordinator.async_config_entry_first_refresh()
        config.runtime_data = PiHoleConfigData(api, coordinator, PiHoleConfig(**config.data))

        await hass.config_entries.async_forward_entry_setups(config, platforms)
        return True
    except ConfigEntryNotReady as ex:
        _LOGGER.error(ex)
        return False


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry):
    await hass.config_entries.async_unload_platforms(config, [Platform.SWITCH])
    return await hass.config_entries.async_unload(config.entry_id)


async def async_remove_entry(hass: HomeAssistant, config: ConfigEntry):
    await hass.config_entries.async_remove(config.entry_id)

    