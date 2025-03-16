from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from uuid import uuid4
import logging

_LOGGER = logging.getLogger(__name__)


class PiHoleVersionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry, keyword: str, name: str, idx: int):
        self._idx = idx
        self._keyword = keyword
        self._name = name
        self._native_value = None
        self._state = None
        self._hass = hass
        self._config = config
        super().__init__(config.runtime_data.coordinator, context=self._idx)

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        if 'versions' in self.coordinator.data:
            version_data = self.coordinator.data['versions']
            match self._keyword:
                case "core": self._native_value = version_data.version.core.local.version
                case "ftl": self._native_value = version_data.version.ftl.local.version
                case "web": self._native_value = version_data.version.web.local.version
                case _: raise ValueError("Incorrect index was given")
            self._state = self._native_value

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self._name
    
    @property
    def native_value(self):
        return self._native_value

    @property
    def unique_id(self):
        return f"{str(uuid4())}/Sensor"