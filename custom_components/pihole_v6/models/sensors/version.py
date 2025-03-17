from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from uuid import uuid4
import logging, asyncio
from ...hole import PiHole
from ..version import PiHoleVersionInfo

_LOGGER = logging.getLogger(__name__)


class PiHoleVersionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, config: ConfigEntry, keyword: str, idx: int):
        self._idx = idx
        self._keyword = keyword
        self._name = keyword.upper() + " local version".title() if keyword == "ftl" else f"{keyword} local version".title()
        self._state = None
        self._config = config
        self.entity_description = SensorEntityDescription(key=keyword, translation_key=keyword)
        self._attr_available = False
        self._attr_unique_id = f"{uuid4()}-{self.entity_description.key}-Sensor"
        super().__init__(config.runtime_data.coordinator, context=self._idx)

    async def set_state(self, state: PiHoleVersionInfo):
        match self._keyword:
            case "core": self._state = state.version.core.local.version
            case "ftl": self._state = state.version.ftl.local.version
            case "web": self._state = state.version.web.local.version
            case _: raise ValueError("Incorrect index was given")
        await self.async_update_ha_state()
    
    async def async_update(self):
        device = PiHole(self.hass, self._config)
        await device.update_versions()
        data = device.data['versions']
        await self.set_state(data)

    @callback
    def _handle_coordinator_update(self) -> None:
        if 'versions' in self.coordinator.data:
            version_data = self.coordinator.data['versions']
            _LOGGER.debug(f"Received version data: {version_data}")
            asyncio.run_coroutine_threadsafe(self.set_state(version_data), self.hass.loop)
            self._attr_native_value = self._state
            self._attr_available = True
        else:
            _LOGGER.warning(f"No version data found in coordinator: {self.coordinator.data}")

    @property
    def native_value(self):
        _LOGGER.error(self._attr_native_value, stack_info=True, extra={"sensor": self.name, "unique_id": self._attr_unique_id})
        return self._attr_native_value

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self._name