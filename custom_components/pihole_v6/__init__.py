from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
import logging
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)
from homeassistant.helpers.device_registry import DeviceEntry
from .models.const import (
    MIN_TIME_BETWEEN_UPDATES,
    DOMAIN
)
from .models.config import PiHoleConfig
from .hole import PiHole
from .data import PiHoleData
from .exceptions import HoleException

_LOGGER = logging.getLogger(__name__)
platforms = [
    Platform.SWITCH
]


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    hass.states.async_set(f"{DOMAIN}.state", "initialized")
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    try:
        api = PiHole(hass, config)
        async def async_update_data() -> None:
            try:
                if not await api.verify_session():
                    await api.update_session()
                
                await api.update_blocking()
                await api.update_versions()
                await api.update_statistics()
            except HoleException as ex:
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
        config.runtime_data = PiHoleData(api, coordinator, PiHoleConfig(**config.data))

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


async def async_remove_config_entry_device(hass: HomeAssistant, config: ConfigEntry, device_entry: DeviceEntry) -> bool:
    return True