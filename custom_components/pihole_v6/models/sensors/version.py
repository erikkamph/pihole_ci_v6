from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from uuid import uuid4
import logging, asyncio
from ..version import PiHoleVersionInfo
from ...entity import PiHoleEntity

_LOGGER = logging.getLogger(__name__)


class PiHoleVersionSensor(PiHoleEntity, SensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry, keyword: str, idx: int):
        self._idx = idx
        self._keyword = keyword
        self._name = keyword.upper() + " local version".title() if keyword == "ftl" else f"{keyword} local version".title()
        self._state = None
        self._config = config
        self.entity_description = SensorEntityDescription(key=keyword, translation_key=keyword)
        self._attr_available = False
        self._attr_unique_id = f"{config.entry_id}/{self.entity_description.key}"
        self._attr_has_entity_name = True
        super().__init__(config.runtime_data.coordinator, self._name, server_unique_id=config.entry_id, config_entry=config, hass=hass, context=self._idx)

    @property
    def has_entity_name(self):
        return self._attr_has_entity_name

    async def set_state(self, state: PiHoleVersionInfo):
        match self._keyword:
            case "core": self._state = state.version.core.local.version
            case "ftl": self._state = state.version.ftl.local.version
            case "web": self._state = state.version.web.local.version
            case _: raise ValueError("Incorrect index was given")
        self.async_write_ha_state()

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